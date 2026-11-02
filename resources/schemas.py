from marshmallow import Schema, fields

class ItemSchema(Schema):
    id = fields.Str(dump_only=True) # in response only
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    store_id = fields.Str(required=True)

class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()

class StoreSchema(Schema):
    id = fields.Str(dump_only=True) # in response only
    name = fields.Str(required=True)