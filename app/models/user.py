from uuid import uuid4

from app.extensions import db


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    token_version = db.Column(db.String(32), nullable=False, default=lambda: uuid4().hex)
