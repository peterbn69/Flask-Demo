from flask import Flask, jsonify

from app.config import Config
from app.extensions import api, db, jwt, migrate
from app.models import TokenBlocklistModel
from app.resources.item import bp as item_bp
from app.resources.store import bp as store_bp
from app.resources.tag import bp as tag_bp
from app.resources.user import bp as user_bp


def register_jwt_callback(jwt):
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            "message": "The token has expired.",
            "error": "token_expired"
        }), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({
            "message": error,
            "error": "invalid_token"
        }), 401

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return jsonify({
            "message": "The token is not fresh.",
            "error": "fresh_token_required"
        }), 401

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify({
            "message": "The token has been revoked.",
            "error": "token_revoked"
        }), 401

    @jwt.token_in_blocklist_loader
    def is_token_revoked(jwt_header, jwt_payload):
        query = db.select(TokenBlocklistModel.id).where(
            TokenBlocklistModel.jti == jwt_payload["jti"]
        )
        return db.session.scalar(query) is not None

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({
            "message": "Request does not contain an access token.",
            "error": "authorization_required"
        }), 401


def create_app(db_url=None):
    app = Flask(__name__)

    app.config.from_object(Config)
    if db_url:
        app.config["SQLALCHEMY_DATABASE_URI"] = db_url

    db.init_app(app)
    migrate.init_app(app, db)

    api.init_app(app)

    jwt.init_app(app)
    register_jwt_callback(jwt)

    api.register_blueprint(store_bp)
    api.register_blueprint(item_bp)
    api.register_blueprint(tag_bp)
    api.register_blueprint(user_bp)

    return app
