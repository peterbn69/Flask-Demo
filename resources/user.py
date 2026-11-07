from flask.views import MethodView
from flask_smorest import Blueprint

from db import db
from models import UserModel
from resources.utils import commit_or_abort, hash_password, message_response
from schemas import UserSchema

bp = Blueprint("users", __name__)


@bp.route("/register")
class UserRegister(MethodView):
    @bp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel(
            username=user_data["username"],
            password=hash_password(user_data["password"]),
        )

        db.session.add(user)
        commit_or_abort(
            "An error occurred while registering the user.",
            "The user conflicts with an existing record.",
        )

        return message_response(201, "User created successfully.")


@bp.route("/user/<int:user_id>")
class User(MethodView):
    @bp.response(200, UserSchema)
    def get(self, user_id):
        return db.get_or_404(UserModel, user_id)

    def delete(self, user_id):
        user = db.get_or_404(UserModel, user_id)

        db.session.delete(user)
        commit_or_abort("An error occurred while deleting the user.")

        return message_response(200, "User deleted.")
