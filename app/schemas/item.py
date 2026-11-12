from marshmallow import Schema, fields
from marshmallow.validate import Length

from app.schemas.common import name_length
from app.schemas.plain import PlainItemSchema, PlainStoreSchema, PlainTagSchema


class ItemUpdateSchema(Schema):
    name = fields.Str(validate=name_length)
    description = fields.Str(required=False, allow_none=True, validate=Length(max=255))
    price = fields.Decimal(as_string=True)


class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)
