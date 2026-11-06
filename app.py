import os

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_smorest import Api

from db import db
from resources.item import bp as item_bp
from resources.store import bp as store_bp
from resources.tag import bp as tag_bp


def create_app(db_url: str | None = None) -> Flask:
    app = Flask(__name__)

    # ---------- API CONFIG ----------
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.2.1"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    # ---------- DATABASE CONNECTION ----------
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()

    api = Api(app)

    jwt = JWTManager(app)

    app.config["JWT_SECRET_KEY"] = "13706954"

    api.register_blueprint(store_bp)
    api.register_blueprint(item_bp)
    api.register_blueprint(tag_bp)

    return app
