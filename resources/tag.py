from flask.views import MethodView
from flask_smorest import Blueprint
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from db import db
from models import TagModel, StoreModel, ItemModel
from resources.utility import message_response, respond
from schemas import TagSchema, TagAndItemSchema

bp = Blueprint("tags", __name__)

@bp.route("/store/<int:store_id>/tag")
class TagsInStore(MethodView):
    @bp.response(200, TagSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()

    @bp.arguments(TagSchema)
    @bp.response(201, TagSchema)
    def post(self, tag_data, store_id):
        StoreModel.query.get_or_404(store_id)
        tag = TagModel(**tag_data, store_id=store_id)

        try:
            db.session.add(tag)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            respond(409, "The tag conflicts with an existing record.")
        except SQLAlchemyError:
            db.session.rollback()
            respond(500, "An error occurred while creating the tag.")

        return tag

@bp.route("/item/<int:item_id>/tag/<int:tag_id>")
class LinkTagsToItem(MethodView):
    @bp.response(201, TagSchema)
    def post(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        if item.store_id != tag.store_id:
            respond(400, "The item and tag must belong to the same store.")

        if tag in item.tags:
            respond(409, "The tag is already linked to the item.")

        try:
            item.tags.append(tag)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            respond(409, "The item and tag could not be linked due to a conflict.")
        except SQLAlchemyError:
            db.session.rollback()
            respond(500, "An error occurred while linking the tag.")

        return tag

    @bp.response(200, TagAndItemSchema)
    def delete(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        if tag not in item.tags:
            respond(404, "The tag is not linked to the item.")

        try:
            item.tags.remove(tag)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            respond(500, "An error occurred while unlinking the tag.")

        return {
            "message": "Tag unlinked from item.",
            "item": item,
            "tag": tag,
        }

@bp.route("/tag/<int:tag_id>")
class Tag(MethodView):
    @bp.response(200, TagSchema)
    def get(self, tag_id):
        return TagModel.query.get_or_404(tag_id)

    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)

        try:
            db.session.delete(tag)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            respond(500, "An error occurred while deleting the tag.")

        return message_response(200, "Tag deleted.")
