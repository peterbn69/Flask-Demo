import time

from flask.views import MethodView
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)
from flask_smorest import Blueprint

from app.extensions import db
from app.models import TokenBlocklistModel, UserModel
from app.resources.helpers import abort_with, commit_or_abort, message_response
from app.schemas import UserSchema
from app.security import hash_password, verify_password

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
            access_token = create_access_token(identity=str(user.id), fresh=True)
            refresh_token = create_refresh_token(identity=str(user.id))
            return {"access_token": access_token, "refresh_token": refresh_token}

        abort_with(401, "Invalid credentials.")


@bp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        user_id = get_jwt_identity()
        if db.session.get(UserModel, int(user_id)) is None:
            abort_with(401, "The user no longer exists.")

        new_token = create_access_token(identity=user_id, fresh=False)
        return {"access_token": new_token}


@bp.route("/logout")
class UserLogout(MethodView):
    @jwt_required(verify_type=False)
    def post(self):
        jwt_payload = get_jwt()

        db.session.execute(
            db.delete(TokenBlocklistModel).where(TokenBlocklistModel.exp < int(time.time()))
        )
        db.session.add(TokenBlocklistModel(jti=jwt_payload["jti"], exp=jwt_payload["exp"]))
        commit_or_abort("An error occurred while logging out.")

        return message_response(200, "User logged out.")


@bp.route("/user/<int:user_id>")
class User(MethodView):
    @jwt_required()
    @bp.response(200, UserSchema)
    def get(self, user_id):
        return db.get_or_404(UserModel, user_id)

    @jwt_required(fresh=True)
    def delete(self, user_id):
        if get_jwt_identity() != str(user_id):
            abort_with(403, "You can only delete your own account.")

        user = db.get_or_404(UserModel, user_id)

        db.session.delete(user)
        commit_or_abort("An error occurred while deleting the user.")

        return message_response(200, "User deleted.")
