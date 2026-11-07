from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint

from db import db
from models import ItemModel, StoreModel, TagModel
from resources.utils import abort_with, commit_or_abort, message_response
from schemas import TagAndItemSchema, TagSchema

bp = Blueprint("tags", __name__)


@bp.route("/store/<int:store_id>/tag")
class TagsInStore(MethodView):
    @bp.response(200, TagSchema(many=True))
    def get(self, store_id):
        store = db.get_or_404(StoreModel, store_id)
        return store.tags.all()

    @jwt_required()
    @bp.arguments(TagSchema)
    @bp.response(201, TagSchema)
    def post(self, tag_data, store_id):
        db.get_or_404(StoreModel, store_id)

        tag = TagModel(**tag_data, store_id=store_id)
        db.session.add(tag)
        commit_or_abort(
            "An error occurred while creating the tag.",
            "The tag conflicts with an existing record.",
        )

        return tag


@bp.route("/item/<int:item_id>/tag/<int:tag_id>")
class LinkTagsToItem(MethodView):
    @jwt_required()
    @bp.response(201, TagSchema)
    def post(self, item_id, tag_id):
        item = db.get_or_404(ItemModel, item_id)
        tag = db.get_or_404(TagModel, tag_id)

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

    @jwt_required()
    @bp.response(200, TagAndItemSchema)
    def delete(self, item_id, tag_id):
        item = db.get_or_404(ItemModel, item_id)
        tag = db.get_or_404(TagModel, tag_id)

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
    def get(self, tag_id):
        return db.get_or_404(TagModel, tag_id)

    @jwt_required()
    def delete(self, tag_id):
        tag = db.get_or_404(TagModel, tag_id)

        db.session.delete(tag)
        commit_or_abort("An error occurred while deleting the tag.")

        return message_response(200, "Tag deleted.")
