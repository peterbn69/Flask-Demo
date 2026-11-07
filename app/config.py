import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    # ---------- API CONFIG ----------
    PROPAGATE_EXCEPTIONS = True
    API_TITLE = "Stores REST API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.2.1"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    # ---------- DATABASE CONNECTION ----------
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///data.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ---------- JWT ----------
    JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
