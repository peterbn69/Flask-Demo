from flask import Blueprint, request
from flask.views import MethodView
from resources.db import stores, items
from resources.utility import includes, exists, get_or_404, create, delete_or_404

item_bp = Blueprint("items", __name__)

@item_bp.route("/item")
class ItemList(MethodView):
    def get():
        pass

    def post():
        pass

@item_bp.route("item/<string:item_id>")
class Item(MethodView):
    def get(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass

@item_bp.route("/item", methods=["GET", "POST"])
def item_collection():
    if request.method == "GET":
        return {"items": list(items.values())}
    
    item_data = request.get_json()
    
    includes(item_data, "name", "price", "store_id")
    get_or_404(stores, item_data["store_id"], "Store")
    exists(items, item_data, "name", "store_id")

    return create(items, item_data), 201

@item_bp.get("/item/<string:item_id>")
def get_item(item_id):
    return get_or_404(items, item_id, "Item")

@item_bp.put("/item/<string:item_id>")
def update_item(item_id):
    item_data = request.get_json()
    includes(item_data, "name", "price")

    item = get_or_404(items, item_id, "Item")
    item |= item_data

    return item

@item_bp.delete("/item/<string:item_id>")
def delete_item(item_id):
    return delete_or_404(items, item_id, "Item")
