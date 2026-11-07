from marshmallow import Schema, fields

from app.schemas.common import name_length


class PlainItemSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=name_length)
    price = fields.Decimal(as_string=True, required=True)


class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=name_length)


class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=name_length)
