from flask import request
from flask_smorest import Blueprint
from flask.views import MethodView
from resources.db import stores, items
from resources.utility import exists, get_or_404, create, delete_or_404
from resources.schemas import ItemSchema, ItemUpdateSchema

bp = Blueprint("items", __name__)

@bp.route("/item")
class ItemList(MethodView):
    @bp.response(200, ItemSchema(many=True))
    def get(self):
        return items.values()

    @bp.arguments(ItemSchema)
    @bp.response(201, ItemSchema)
    def post(self, item_data):
        get_or_404(stores, item_data["store_id"], "Store")
        exists(items, item_data, "name", "store_id")

        return create(items, item_data), 201

@bp.route("/item/<string:item_id>")
class Item(MethodView):
    @bp.response(200, ItemSchema)
    def get(self, item_id):
        return get_or_404(items, item_id, "Item")

    @bp.arguments(ItemUpdateSchema)
    @bp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = get_or_404(items, item_id, "Item")
        item |= item_data
        return item

    def delete(self, item_id):
        return delete_or_404(items, item_id, "Item")
