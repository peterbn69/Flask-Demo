from marshmallow import Schema, fields

from app.schemas.common import name_length, password_length


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=name_length)
    password = fields.Str(required=True, load_only=True, validate=password_length)
