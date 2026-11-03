from flask.views import MethodView
from flask_smorest import Blueprint
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from db import db
from models import StoreModel
from resources.utility import respond
from schemas import StoreSchema

bp = Blueprint("stores", __name__)

@bp.route("/store")
class StoreList(MethodView):
    @bp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @bp.arguments(StoreSchema)
    @bp.response(201, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)

        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            respond(409, "The store conflicts with an existing record.")
        except SQLAlchemyError:
            db.session.rollback()
            respond(500, "An error occurred while creating the store.")

        return store

@bp.route("/store/<int:store_id>")
class Store(MethodView):
    @bp.response(200, StoreSchema)
    def get(self, store_id):
        return StoreModel.query.get_or_404(store_id)

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)

        try:
            db.session.delete(store)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            respond(500, "An error occurred while deleting the store.")

        return {"message": "Store and its items deleted."}, 200
