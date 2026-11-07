from marshmallow import Schema, fields, validate

NAME_MAX_LENGTH = 80
name_length = validate.Length(min=1, max=NAME_MAX_LENGTH)

PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 128
password_length = validate.Length(min=PASSWORD_MIN_LENGTH, max=PASSWORD_MAX_LENGTH)


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


class ItemUpdateSchema(Schema):
    name = fields.Str(validate=name_length)
    price = fields.Decimal(as_string=True)


class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)


class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)


class TagSchema(PlainTagSchema):
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)


class TagAndItemSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=name_length)
    password = fields.Str(required=True, load_only=True, validate=password_length)
