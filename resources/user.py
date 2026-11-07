from flask.views import MethodView
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from flask_smorest import Blueprint

from db import db
from models import UserModel
from resources.utils import abort_with, commit_or_abort, hash_password, message_response, verify_password
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


@bp.route("/login")
class UserLogin(MethodView):
    @bp.arguments(UserSchema)
    def post(self, user_data):
        query = db.select(UserModel).where(UserModel.username == user_data["username"])
        user = db.session.scalar(query)

        if user and verify_password(user_data["password"], user.password):
            access_token = create_access_token(identity=str(user.id))
            return {"access_token": access_token}

        abort_with(401, "Invalid credentials.")


@bp.route("/user/<int:user_id>")
class User(MethodView):
    @jwt_required()
    @bp.response(200, UserSchema)
    def get(self, user_id):
        return db.get_or_404(UserModel, user_id)

    @jwt_required()
    def delete(self, user_id):
        if get_jwt_identity() != str(user_id):
            abort_with(403, "You can only delete your own account.")

        user = db.get_or_404(UserModel, user_id)

        db.session.delete(user)
        commit_or_abort("An error occurred while deleting the user.")

        return message_response(200, "User deleted.")
