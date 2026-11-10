# Flask Demo: Stores REST API

> **Status:** Work in progress. Endpoints, schemas, and this document may change.

A REST API for managing stores, the items they sell, and tags that group items within a store. Built with Flask, Flask-Smorest, and SQLAlchemy, with auto-generated OpenAPI documentation and Swagger UI.

## Features

- CRUD endpoints for stores, items, and tags
- Many-to-many relationships between items and tags (tags can only be linked to items in the same store)
- Cascading deletes: deleting a store removes its items and tags
- User registration and login with Argon2 password hashing (passwords are never returned in responses)
- JWT authentication: creating, updating, and deleting data requires a bearer token
- Refresh tokens: get a new access token without logging in again; deleting a store or a user account still requires a fresh token from `/login`
- Logout revokes the access or refresh token it is called with through a database-backed blocklist (expired entries are pruned on each logout)
- Request/response validation with Marshmallow (names are 1–80 characters, passwords 8–128)
- Interactive API docs at `/swagger-ui`
- SQLite by default; configurable via `DATABASE_URL`
- Dockerfile included

## Requirements

- Python 3.13+
- pip

## Getting started

```bash
# Clone and enter the project
git clone https://github.com/peterbn69/Flask-Demo.git
cd Flask-Demo

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate
# Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the development server
flask run
```

The API is now available at <http://127.0.0.1:5000> and the Swagger UI at <http://127.0.0.1:5000/swagger-ui>.

`.flaskenv` sets `FLASK_APP=wsgi` and enables debug mode (auto-reload) for local development. Tables are created automatically on startup.

### Configuration

| Variable         | Default             | Description                                                          |
| ---------------- | ------------------- | -------------------------------------------------------------------- |
| `DATABASE_URL`   | `sqlite:///data.db` | SQLAlchemy database URL                                              |
| `JWT_SECRET_KEY` | none (required)     | Secret used to sign JWTs; the app fails to start if it is not set    |

Variables can be placed in a `.env` file (loaded via `python-dotenv`). `.env` is ignored by Git and by Docker builds, so create your own from the template:

```bash
cp .env.example .env
# Windows: copy .env.example .env
```

Then set `JWT_SECRET_KEY` in `.env` to a long random string.

Access tokens expire after 15 minutes and refresh tokens after 7 days. To change this, edit `JWT_ACCESS_TOKEN_EXPIRES` and `JWT_REFRESH_TOKEN_EXPIRES` in `app/config.py`.

### Docker

Run the following commands if you want to run the API in a Docker container. The API will be available at the same URL as above. The image does not contain your `.env`, so pass variables at runtime.

```bash
docker build -t flask-demo .
docker run -dp 5000:5000 --env-file .env --name flask-container flask-demo
```

## API overview

| Method | Endpoint                          | Auth          | Description                                   |
| ------ | --------------------------------- | ------------- | --------------------------------------------- |
| GET    | `/store`                          |               | List all stores                               |
| POST   | `/store`                          | Access        | Create a store                                |
| GET    | `/store/<store_id>`               |               | Get a store                                   |
| DELETE | `/store/<store_id>`               | Fresh access  | Delete a store, its items and tags            |
| GET    | `/store/<store_id>/tag`           |               | List a store's tags                           |
| POST   | `/store/<store_id>/tag`           | Access        | Create a tag in a store                       |
| GET    | `/item`                           |               | List all items                                |
| POST   | `/item`                           | Access        | Create an item                                |
| GET    | `/item/<item_id>`                 |               | Get an item                                   |
| PATCH  | `/item/<item_id>`                 | Access        | Partially update an item's name/price         |
| DELETE | `/item/<item_id>`                 | Access        | Delete an item                                |
| POST   | `/item/<item_id>/tag/<tag_id>`    | Access        | Link a tag to an item                         |
| DELETE | `/item/<item_id>/tag/<tag_id>`    | Access        | Unlink a tag from an item                     |
| GET    | `/tag/<tag_id>`                   |               | Get a tag                                     |
| DELETE | `/tag/<tag_id>`                   | Access        | Delete a tag                                  |
| POST   | `/register`                       |               | Register a user                               |
| POST   | `/login`                          |               | Log in and receive an access and refresh token |
| POST   | `/refresh`                        | Refresh       | Get a new (non-fresh) access token            |
| POST   | `/logout`                         | Either        | Log out and revoke the token that was sent    |
| GET    | `/user/<user_id>`                 | Access        | Get a user (id and username only)             |
| DELETE | `/user/<user_id>`                 | Fresh access  | Delete your own account                       |

Endpoints with an Auth value need an `Authorization: Bearer <token>` header:

- **Access**: any access token, from `/login` or `/refresh`.
- **Fresh access**: an access token from `/login`. Tokens from `/refresh` are not fresh, so log in again before these actions.
- **Refresh**: the refresh token from `/login`.
- **Either**: an access or a refresh token. To fully log out, call `/logout` once with each.

A missing, invalid, expired, or revoked (logged-out) token returns 401, and so does a non-fresh token on an endpoint that needs a fresh one.

### Example

```bash
# Register a user (password must be 8-128 characters)
curl -X POST http://127.0.0.1:5000/register \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "password": "correct-horse-battery"}'

# Log in and copy the "access_token" and "refresh_token" from the response
curl -X POST http://127.0.0.1:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "password": "correct-horse-battery"}'
TOKEN=<paste the access_token here>
REFRESH_TOKEN=<paste the refresh_token here>

# Create a store
curl -X POST http://127.0.0.1:5000/store \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "My Store"}'

# Create an item in that store
curl -X POST http://127.0.0.1:5000/item \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Chair", "price": "17.99", "store_id": 1}'

# Create a tag and link it to the item
curl -X POST http://127.0.0.1:5000/store/1/tag \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "furniture"}'
curl -X POST http://127.0.0.1:5000/item/1/tag/1 \
  -H "Authorization: Bearer $TOKEN"

# Change only the item's price (other fields are left as they are)
curl -X PATCH http://127.0.0.1:5000/item/1 \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"price": "19.99"}'

# When the access token expires, get a new one with the refresh token
curl -X POST http://127.0.0.1:5000/refresh \
  -H "Authorization: Bearer $REFRESH_TOKEN"

# Log out by revoking both tokens (each stops working immediately)
curl -X POST http://127.0.0.1:5000/logout \
  -H "Authorization: Bearer $TOKEN"
curl -X POST http://127.0.0.1:5000/logout \
  -H "Authorization: Bearer $REFRESH_TOKEN"
```

### Error responses

Errors are returned as JSON with a `code`, a `status`, and usually a `message`.

| Status | When                                                                           |
| ------ | ------------------------------------------------------------------------------ |
| 400    | Linking an item and a tag that belong to different stores                      |
| 401    | Wrong login credentials; a missing, invalid, expired, or revoked token; a non-fresh token where a fresh one is required; or a refresh token whose user was deleted |
| 403    | Deleting a user account other than your own                                    |
| 404    | The store, item, tag, or user does not exist, or the tag is not linked to the item |
| 409    | A duplicate name in the same store, a duplicate store name or username, or a tag that is already linked to an item |
| 422    | The request body is missing a required field or has an invalid one (including names or passwords outside the allowed length) |
| 500    | The database could not complete the operation                                  |

## Project structure

```
wsgi.py               Entry point (creates the app)
app/
  __init__.py         Application factory (create_app)
  config.py           Configuration loaded from environment variables
  extensions.py       Shared extension instances (db, api, jwt)
  security.py         Password hashing and verification
  models/             SQLAlchemy models (store, item, tag, items_tags, user, token_blocklist)
  resources/          Flask-Smorest blueprints (store, item, tag, user) and shared helpers (helpers)
  schemas/            Marshmallow schemas (plain, item, store, tag, user) and shared validators (common)
.env.example          Template for the .env file
requirements.txt      Python dependencies
Dockerfile            Container image definition
.dockerignore         Files kept out of the Docker image
.editorconfig         Editor settings (UTF-8, LF, 4-space indent for Python)
.flaskenv             Flask CLI settings for local development
.gitattributes        Normalizes line endings to LF
```

## Next steps

- [x] User registration with hashed passwords
- [x] Login endpoint and JWT-protected routes
- [x] Logout with token revocation
- [x] Refresh tokens and fresh-token checks
- [ ] Database migrations

## License

Released under the [MIT License](LICENSE).
