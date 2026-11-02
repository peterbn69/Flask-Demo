from flask import Blueprint, request
from flask.views import MethodView
from resources.db import stores, items
from resources.utility import includes, exists, get_or_404, create, delete_or_404

bp = Blueprint("items", __name__)

class ItemList(MethodView):
    def get(self):
        return {"items": list(items.values())}

    def post(self):
        item_data = request.get_json()
        
        includes(item_data, "name", "price", "store_id")
        get_or_404(stores, item_data["store_id"], "Store")
        exists(items, item_data, "name", "store_id")

        return create(items, item_data), 201

class Item(MethodView):
    def get(self, item_id):
        return get_or_404(items, item_id, "Item")

    def put(self, item_id):
        item_data = request.get_json()
        includes(item_data, "name", "price")

        item = get_or_404(items, item_id, "Item")
        item |= item_data

        return item

    def delete(self, item_id):
        return delete_or_404(items, item_id, "Item")

bp.add_url_rule("/item", view_func=ItemList.as_view("item_list"))
bp.add_url_rule("/item/<string:item_id>", view_func=Item.as_view("item"))
