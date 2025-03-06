from marshmallow import Schema, fields

class PlainStoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)

class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested("PlainItemSchema"), dump_only=True)

class StoreUpdateSchema(Schema):
    name = fields.Str()

