from flask import Blueprint, request
from flask.views import MethodView
from resources.db import stores
from resources.utility import includes, exists, get_or_404, create, delete_or_404

store_bp = Blueprint("stores", __name__)

@store_bp.route("/store")
class StoreList(MethodView):
    def get(self):
        pass

    def post(self):
        pass

@store_bp.route("/store/<string:store_id>")
class Store(MethodView):
    def get(self):
        pass

    def delete(self):
        pass


@store_bp.route("/store", methods=["GET", "POST"])
def store_collection():
    if request.method == "GET":
        return {"stores": list(stores.values())}
    
    store_data = request.get_json()
    includes(store_data, "name")
    exists(stores, store_data, "name")

    return create(stores, store_data), 201

@store_bp.get("/store/<string:store_id>")
def get_store(store_id):
    return get_or_404(stores, store_id, "Store")

@store_bp.delete("/store/<string:store_id>")
def delete_store(store_id):
    return delete_or_404(stores, store_id, "Store")
