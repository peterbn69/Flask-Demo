import uuid
from flask import Blueprint, request
from flask_smorest import abort
from db import stores, items

store_bp = Blueprint("store", __name__)

def includes(data: dict, *keys: str) -> None:
    missing_keys = [key for key in keys if key not in data]

    if missing_keys: abort(400, message=f"Bad request. Missing required keys: {', '.join(missing_keys)}.")

def exists(old: dict, new: dict, *keys: str) -> None:
    for item in old.values():
        if all(item[key] == new[key] for key in keys):
            abort(400, message="Bad request. The element already exists.")

@store_bp.route("/store", methods=["GET", "POST"])
def store_collection():
    if request.method == "GET":
        return {"stores": list(stores.values())}
    
    store_data = request.get_json()
    includes(store_data, "name")
    exists(stores, store_data, "name")

    store_id = uuid.uuid4().hex
    new_store = {**store_data, "id": store_id}
    stores[store_id] = new_store

    return new_store, 201

@store_bp.route("/item", methods=["GET", "POST"])
def item_collection():
    if request.method == "GET":
        return {"items": list(items.values())}
    
    item_data = request.get_json()
    includes(item_data, "name", "price", "store_id")

    if item_data["store_id"] not in stores:
        abort(404, message="Store not found.")

    exists(items, item_data, "name", "store_id")

    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item

    return item, 201

@store_bp.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404, message="Store not found.")

@store_bp.delete("/store/<string:store_id>")
def delete_store(store_id):
    try:
        del stores[store_id]
        return {"message": "Store deleted."}
    except KeyError:
        abort(404, message="Store not found.")

@store_bp.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404, message="Item not found.")

@store_bp.put("/item/<string:item_id>")
def update_item(item_id):
    try:
        item_data = request.get_json()
        includes(item_data, "name", "price")

        item = items[item_id]
        item |= item_data

        return item
    except KeyError:
        abort(404, message="Item not found.")

@store_bp.delete("/item/<string:item_id>")
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message": "Item deleted."}
    except KeyError:
        abort(404, message="Item not found.")