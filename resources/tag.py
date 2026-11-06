from typing import Any

from flask.views import MethodView
from flask_smorest import Blueprint

from db import db
from models import ItemModel, StoreModel, TagModel
from resources.utils import abort_with, commit_or_abort, message_response
from schemas import TagAndItemSchema, TagSchema

bp = Blueprint("tags", __name__)


@bp.route("/store/<int:store_id>/tag")
class TagsInStore(MethodView):
    @bp.response(200, TagSchema(many=True))
    def get(self, store_id: int) -> list[TagModel]:
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()

    @bp.arguments(TagSchema)
    @bp.response(201, TagSchema)
    def post(self, tag_data: dict[str, Any], store_id: int) -> TagModel:
        StoreModel.query.get_or_404(store_id)

        tag = TagModel(**tag_data, store_id=store_id)
        db.session.add(tag)
        commit_or_abort(
            "An error occurred while creating the tag.",
            "The tag conflicts with an existing record.",
        )

        return tag


@bp.route("/item/<int:item_id>/tag/<int:tag_id>")
class LinkTagsToItem(MethodView):
    @bp.response(201, TagSchema)
    def post(self, item_id: int, tag_id: int) -> TagModel:
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        if item.store_id != tag.store_id:
            abort_with(400, "The item and tag must belong to the same store.")

        if tag in item.tags:
            abort_with(409, "The tag is already linked to the item.")

        item.tags.append(tag)
        commit_or_abort(
            "An error occurred while linking the tag.",
            "The item and tag could not be linked due to a conflict.",
        )

        return tag

    @bp.response(200, TagAndItemSchema)
    def delete(self, item_id: int, tag_id: int) -> dict[str, Any]:
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        if tag not in item.tags:
            abort_with(404, "The tag is not linked to the item.")

        item.tags.remove(tag)
        commit_or_abort("An error occurred while unlinking the tag.")

        return {
            "message": "Tag unlinked from item.",
            "item": item,
            "tag": tag,
        }


@bp.route("/tag/<int:tag_id>")
class Tag(MethodView):
    @bp.response(200, TagSchema)
    def get(self, tag_id: int) -> TagModel:
        return TagModel.query.get_or_404(tag_id)

    def delete(self, tag_id: int) -> tuple[dict[str, str], int]:
        tag = TagModel.query.get_or_404(tag_id)

        db.session.delete(tag)
        commit_or_abort("An error occurred while deleting the tag.")

        return message_response(200, "Tag deleted.")
