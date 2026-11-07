from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint

from db import db
from models import StoreModel
from resources.utils import commit_or_abort, message_response
from schemas import StoreSchema

bp = Blueprint("stores", __name__)


@bp.route("/store")
class StoreList(MethodView):
    @bp.response(200, StoreSchema(many=True))
    def get(self):
        return db.session.scalars(db.select(StoreModel)).all()

    @jwt_required()
    @bp.arguments(StoreSchema)
    @bp.response(201, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)
        db.session.add(store)
        commit_or_abort(
            "An error occurred while creating the store.",
            "The store conflicts with an existing record.",
        )

        return store


@bp.route("/store/<int:store_id>")
class Store(MethodView):
    @bp.response(200, StoreSchema)
    def get(self, store_id):
        return db.get_or_404(StoreModel, store_id)

    @jwt_required()
    def delete(self, store_id):
        store = db.get_or_404(StoreModel, store_id)

        db.session.delete(store)
        commit_or_abort("An error occurred while deleting the store.")

        return message_response(200, "Store, its items, and its tags deleted.")
