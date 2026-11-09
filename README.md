# Flask Demo: Stores REST API

> **Status:** Work in progress. Endpoints, schemas, and this document may change.

A REST API for managing stores, the items they sell, and tags that group items within a store. Built with Flask, Flask-Smorest, and SQLAlchemy, with auto-generated OpenAPI documentation and Swagger UI.

## Features

- CRUD endpoints for stores, items, and tags
- Many-to-many relationships between items and tags (tags can only be linked to items in the same store)
- Cascading deletes: deleting a store removes its items and tags
- User registration and login with Argon2 password hashing (passwords are never returned in responses)
- JWT authentication: creating, updating, and deleting data requires a bearer token
- Logout revokes the current token through a database-backed blocklist (expired entries are pruned on each logout)
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

### Docker

Run the following commands if you want to run the API in a Docker container. The API will be available at the same URL as above. The image does not contain your `.env`, so pass variables at runtime.

```bash
docker build -t flask-demo .
docker run -dp 5000:5000 --env-file .env --name flask-container flask-demo
```

## API overview

| Method | Endpoint                          | Auth | Description                           |
| ------ | --------------------------------- | ---- | ------------------------------------- |
| GET    | `/store`                          |      | List all stores                       |
| POST   | `/store`                          | JWT  | Create a store                        |
| GET    | `/store/<store_id>`               |      | Get a store                           |
| DELETE | `/store/<store_id>`               | JWT  | Delete a store, its items and tags    |
| GET    | `/store/<store_id>/tag`           |      | List a store's tags                   |
| POST   | `/store/<store_id>/tag`           | JWT  | Create a tag in a store               |
| GET    | `/item`                           |      | List all items                        |
| POST   | `/item`                           | JWT  | Create an item                        |
| GET    | `/item/<item_id>`                 |      | Get an item                           |
| PATCH  | `/item/<item_id>`                 | JWT  | Partially update an item's name/price |
| DELETE | `/item/<item_id>`                 | JWT  | Delete an item                        |
| POST   | `/item/<item_id>/tag/<tag_id>`    | JWT  | Link a tag to an item                 |
| DELETE | `/item/<item_id>/tag/<tag_id>`    | JWT  | Unlink a tag from an item             |
| GET    | `/tag/<tag_id>`                   |      | Get a tag                             |
| DELETE | `/tag/<tag_id>`                   | JWT  | Delete a tag                          |
| POST   | `/register`                       |      | Register a user                       |
| POST   | `/login`                          |      | Log in and receive an access token    |
| POST   | `/logout`                         | JWT  | Log out and revoke the current token  |
| GET    | `/user/<user_id>`                 | JWT  | Get a user (id and username only)     |
| DELETE | `/user/<user_id>`                 | JWT  | Delete your own account               |

Endpoints marked JWT need an `Authorization: Bearer <access_token>` header. Get a token from `/login`. A missing, invalid, expired, or revoked (logged-out) token returns 401.

### Example

```bash
# Register a user (password must be 8-128 characters)
curl -X POST http://127.0.0.1:5000/register \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "password": "correct-horse-battery"}'

# Log in and copy the "access_token" from the response
curl -X POST http://127.0.0.1:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "password": "correct-horse-battery"}'
TOKEN=<paste the access_token here>

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

# Log out (the token stops working immediately)
curl -X POST http://127.0.0.1:5000/logout \
  -H "Authorization: Bearer $TOKEN"
```

### Error responses

Errors are returned as JSON with a `code`, a `status`, and usually a `message`.

| Status | When                                                                           |
| ------ | ------------------------------------------------------------------------------ |
| 400    | Linking an item and a tag that belong to different stores                      |
| 401    | Wrong login credentials, or a missing, invalid, expired, or revoked token      |
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
- [ ] Database migrations

## License

Released under the [MIT License](LICENSE).
