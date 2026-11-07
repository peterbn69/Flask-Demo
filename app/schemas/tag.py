from marshmallow import Schema, fields

from app.schemas.item import ItemSchema
from app.schemas.plain import PlainItemSchema, PlainStoreSchema, PlainTagSchema


class TagSchema(PlainTagSchema):
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)


class TagAndItemSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)
