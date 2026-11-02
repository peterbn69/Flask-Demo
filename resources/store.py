from flask import request
from flask_smorest import Blueprint
from flask.views import MethodView
from resources.db import stores
from resources.utility import includes, exists, get_or_404, create, delete_or_404

bp = Blueprint("stores", __name__)

class StoreList(MethodView):
    def get(self):
        return {"stores": list(stores.values())}

    def post(self):
        store_data = request.get_json()
        includes(store_data, "name")
        exists(stores, store_data, "name")

        return create(stores, store_data), 201

class Store(MethodView):
    def get(self, store_id):
        return get_or_404(stores, store_id, "Store")

    def delete(self, store_id):
        return delete_or_404(stores, store_id, "Store")

bp.add_url_rule("/store", view_func=StoreList)
bp.add_url_rule("/store/<string:store_id>", view_func=Store)
