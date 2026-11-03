import os

from flask import Flask
from flask_smorest import Api

from resources.store import bp as store_bp
from resources.item import bp as item_bp
from db import db
import models

def create_app(db_url=None) -> Flask:
    app = Flask(__name__)

    # ---------- SWAGGER DOCUMENTATION ----------
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

    api.register_blueprint(store_bp)
    api.register_blueprint(item_bp)

    return app