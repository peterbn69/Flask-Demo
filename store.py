from flask import Blueprint, request

store_bp = Blueprint("store", __name__)

stores = [
    {
        "name": "My Store",
        "items": [
            {"name": "Chair", "price": 15.99},
            {"name": "Charger", "price": 23.99}
        ]
    }
]

@store_bp.route("/store", methods=["GET", "POST"])
def store_collection():
    if request.method == "POST":
        data = request.get_json()
        new_store = {"name": data["name"], "items": []}
        stores.append(new_store)
        return new_store, 201
    return {"stores": stores}

@store_bp.post("/store/<string:name>/item")
def create_item(name):
    data = request.get_json()
    for store in stores:
        if store["name"] == name:
            new_item = {"name": data["name"], "price": data["price"]}
            store["items"].append(new_item)
            return new_item, 201
    return {"message": "Store not found"}, 404

@store_bp.get("/store/<string:name>")
def get_store(name):
    for store in stores:
        if store["name"] == name:
            return store
    return {"message": "Store not found"}, 404

@store_bp.get("/store/<string:name>/item")
def get_items(name):
    for store in stores:
        if store["name"] == name:
            return {"items": store["items"]}
    return {"message": "Store not found"}, 404