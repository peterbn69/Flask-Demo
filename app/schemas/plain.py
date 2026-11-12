from marshmallow import Schema, fields
from marshmallow.validate import Length

from app.schemas.common import name_length


class PlainItemSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=name_length)
    description = fields.Str(required=False, allow_none=True, validate=Length(max=255))
    price = fields.Decimal(as_string=True, required=True)


class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=name_length)


class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=name_length)
