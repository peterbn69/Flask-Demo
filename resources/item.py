from flask.views import MethodView
from flask_smorest import Blueprint
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from db import db
from models import ItemModel, StoreModel
from resources.utility import message_response, respond
from schemas import ItemSchema, ItemUpdateSchema

bp = Blueprint("items", __name__)

@bp.route("/item")
class ItemList(MethodView):
    @bp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    @bp.arguments(ItemSchema)
    @bp.response(201, ItemSchema)
    def post(self, item_data):
        StoreModel.query.get_or_404(item_data["store_id"])

        item = ItemModel(**item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            respond(409, "The item conflicts with an existing record.")
        except SQLAlchemyError:
            db.session.rollback()
            respond(500, "An error occurred while creating the item.")

        return item

@bp.route("/item/<int:item_id>")
class Item(MethodView):
    @bp.response(200, ItemSchema)
    def get(self, item_id):
        return ItemModel.query.get_or_404(item_id)

    @bp.arguments(ItemUpdateSchema)
    @bp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get_or_404(item_id)

        for field, value in item_data.items():
            setattr(item, field, value)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            respond(409, "The item conflicts with an existing record.")
        except SQLAlchemyError:
            db.session.rollback()
            respond(500, "An error occurred while updating the item.")

        return item

    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)

        try:
            db.session.delete(item)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            respond(500, "An error occurred while deleting the item.")

        return message_response(200, "Item deleted.")
