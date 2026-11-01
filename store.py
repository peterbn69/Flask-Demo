import uuid
from flask import Blueprint, request
from db import stores, items

store_bp = Blueprint("store", __name__)

@store_bp.route("/store", methods=["GET", "POST"])
def store_collection():
    if request.method == "GET":
        return {"stores": list(stores.values())}
    
    store_data = request.get_json()
    store_id = uuid.uuid4().hex
    new_store = {**store_data, "id": store_id}
    stores[store_id] = new_store

    return new_store, 201

@store_bp.route("/item", methods=["GET", "POST"])
def item_collection():
    if request.method == "GET":
        return {"items": list(items.values())}
    
    item_data = request.get_json()
    if item_data["store_id"] not in stores:
        return {"message": "Store not found"}, 404

    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item

    return item, 201

@store_bp.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        return {"message": "Store not found"}, 404

@store_bp.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        return {"message": "Item not found"}, 404