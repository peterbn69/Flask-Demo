# Flask Demo: Stores REST API

> **Status:** Work in progress. Endpoints, schemas, and this document may change.

A REST API for managing stores, the items they sell, and tags that group items within a store. Built with Flask, Flask-Smorest, and SQLAlchemy, with auto-generated OpenAPI documentation and Swagger UI.

## Features

- CRUD endpoints for stores, items, and tags
- Many-to-many relationships between items and tags (tags can only be linked to items in the same store)
- Cascading deletes: deleting a store removes its items and tags
- Request/response validation with Marshmallow
- Interactive API docs at `/swagger-ui`
- SQLite by default; configurable via `DATABASE_URL`
- Dockerfile included

## Requirements

- Python 3.10+
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

`.flaskenv` sets `FLASK_APP=app` and enables debug mode (auto-reload). Tables are created automatically on startup.

### Configuration

| Variable       | Default            | Description                    |
| -------------- | ------------------ | ------------------------------ |
| `DATABASE_URL` | `sqlite:///data.db` | SQLAlchemy database URL        |

Variables can be placed in a `.env` file (loaded via `python-dotenv`).

### Docker

```bash
docker build -t flask-demo .
docker run -dp 5000:5000 -w /app -v "${PWD}:/app" --name flask-container flask-demo
```

## API overview

| Method | Endpoint                          | Description                          |
| ------ | --------------------------------- | ------------------------------------ |
| GET    | `/store`                          | List all stores                      |
| POST   | `/store`                          | Create a store                       |
| GET    | `/store/<store_id>`               | Get a store                          |
| DELETE | `/store/<store_id>`               | Delete a store, its items and tags   |
| GET    | `/store/<store_id>/tag`           | List a store's tags                  |
| POST   | `/store/<store_id>/tag`           | Create a tag in a store              |
| GET    | `/item`                           | List all items                       |
| POST   | `/item`                           | Create an item                       |
| GET    | `/item/<item_id>`                 | Get an item                          |
| PUT    | `/item/<item_id>`                 | Update an item's name and/or price   |
| DELETE | `/item/<item_id>`                 | Delete an item                       |
| POST   | `/item/<item_id>/tag/<tag_id>`    | Link a tag to an item                |
| DELETE | `/item/<item_id>/tag/<tag_id>`    | Unlink a tag from an item            |
| GET    | `/tag/<tag_id>`                   | Get a tag                            |
| DELETE | `/tag/<tag_id>`                   | Delete a tag                         |

### Example

```bash
# Create a store
curl -X POST http://127.0.0.1:5000/store \
  -H "Content-Type: application/json" \
  -d '{"name": "My Store"}'

# Create an item in that store
curl -X POST http://127.0.0.1:5000/item \
  -H "Content-Type: application/json" \
  -d '{"name": "Chair", "price": "17.99", "store_id": 1}'

# Create a tag and link it to the item
curl -X POST http://127.0.0.1:5000/store/1/tag \
  -H "Content-Type: application/json" \
  -d '{"name": "furniture"}'
curl -X POST http://127.0.0.1:5000/item/1/tag/1
```

## Project structure

```
app.py          Application factory and configuration
db.py           SQLAlchemy instance
schemas.py      Marshmallow schemas
models/         SQLAlchemy models (store, item, tag, items_tags)
resources/      Flask-Smorest blueprints (store, item, tag, utility)
Dockerfile      Container image definition
```

## Next steps

- [ ] Authentication
- [ ] Database migrations

## License

Released under the [MIT License](LICENSE).
