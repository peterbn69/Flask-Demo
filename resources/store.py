from flask import request
from flask_smorest import Blueprint
from flask.views import MethodView
from resources.db import stores
from resources.utility import exists, get_or_404, create, delete_or_404
from resources.schemas import StoreSchema

bp = Blueprint("stores", __name__)

@bp.route("/store")
class StoreList(MethodView):
    def get(self):
        return {"stores": list(stores.values())}

    @bp.arguments(StoreSchema)
    def post(self, store_data):
        exists(stores, store_data, "name")
        return create(stores, store_data), 201

@bp.route("/store/<string:store_id>")
class Store(MethodView):
    def get(self, store_id):
        return get_or_404(stores, store_id, "Store")

    def delete(self, store_id):
        return delete_or_404(stores, store_id, "Store")
