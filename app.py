from flask import Flask, request

from hello import hello_bp

app = Flask(__name__)
app.register_blueprint(hello_bp)

stores = [
    {
        "name": "My Store",
        "items": [
            {
                "name": "Chair",
                "price": 15.99
            },
            {
                "name": "Charger",
                "price": 23.99
            }
        ]
    }
]

@app.get("/store")
def get_stores():
    return {"stores": stores}

@app.post("/store")
def create_store():
    data = request.get_json()
    new_store = {"name": data["name"], "items": []}
    stores.append(new_store)
    return new_store, 201