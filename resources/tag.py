from flask.views import MethodView
from flask_smorest import Blueprint
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from db import db
from models import TagModel, StoreModel
from resources.utility import message_response, respond
from schemas import TagSchema

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
