from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint

from db import db
from models import ItemModel, StoreModel
from resources.utils import commit_or_abort, message_response
from schemas import ItemSchema, ItemUpdateSchema

bp = Blueprint("items", __name__)


@bp.route("/item")
class ItemList(MethodView):
    @bp.response(200, ItemSchema(many=True))
    def get(self):
        return db.session.scalars(db.select(ItemModel)).all()

    @jwt_required()
    @bp.arguments(ItemSchema)
    @bp.response(201, ItemSchema)
    def post(self, item_data):
        db.get_or_404(StoreModel, item_data["store_id"])

        item = ItemModel(**item_data)
        db.session.add(item)
        commit_or_abort(
            "An error occurred while creating the item.",
            "The item conflicts with an existing record.",
        )

        return item


@bp.route("/item/<int:item_id>")
class Item(MethodView):
    @bp.response(200, ItemSchema)
    def get(self, item_id):
        return db.get_or_404(ItemModel, item_id)

    @jwt_required()
    @bp.arguments(ItemUpdateSchema)
    @bp.response(200, ItemSchema)
    def patch(self, item_data, item_id):
        item = db.get_or_404(ItemModel, item_id)

        for field, value in item_data.items():
            setattr(item, field, value)

        commit_or_abort(
            "An error occurred while updating the item.",
            "The item conflicts with an existing record.",
        )

        return item

    @jwt_required()
    def delete(self, item_id):
        item = db.get_or_404(ItemModel, item_id)

        db.session.delete(item)
        commit_or_abort("An error occurred while deleting the item.")

        return message_response(200, "Item deleted.")
