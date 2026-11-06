from typing import Any

from flask.views import MethodView
from flask_smorest import Blueprint

from db import db
from models import ItemModel, StoreModel
from resources.utils import commit_or_abort, message_response
from schemas import ItemSchema, ItemUpdateSchema

bp = Blueprint("items", __name__)


@bp.route("/item")
class ItemList(MethodView):
    @bp.response(200, ItemSchema(many=True))
    def get(self) -> list[ItemModel]:
        return ItemModel.query.all()

    @bp.arguments(ItemSchema)
    @bp.response(201, ItemSchema)
    def post(self, item_data: dict[str, Any]) -> ItemModel:
        StoreModel.query.get_or_404(item_data["store_id"])

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
    def get(self, item_id: int) -> ItemModel:
        return ItemModel.query.get_or_404(item_id)

    @bp.arguments(ItemUpdateSchema)
    @bp.response(200, ItemSchema)
    def patch(self, item_data: dict[str, Any], item_id: int) -> ItemModel:
        item = ItemModel.query.get_or_404(item_id)

        for field, value in item_data.items():
            setattr(item, field, value)

        commit_or_abort(
            "An error occurred while updating the item.",
            "The item conflicts with an existing record.",
        )

        return item

    def delete(self, item_id: int) -> tuple[dict[str, str], int]:
        item = ItemModel.query.get_or_404(item_id)

        db.session.delete(item)
        commit_or_abort("An error occurred while deleting the item.")

        return message_response(200, "Item deleted.")
