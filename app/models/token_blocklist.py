from app.extensions import db


class TokenBlocklistModel(db.Model):
    __tablename__ = "token_blocklist"

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), unique=True, nullable=False)
    exp = db.Column(db.Integer, nullable=False, index=True)
