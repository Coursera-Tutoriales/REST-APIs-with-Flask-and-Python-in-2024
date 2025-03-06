from marshmallow import Schema, fields

class MessageSchema(Schema):
    """Esquema para respuestas con mensajes genéricos."""
    message = fields.Str(required=True)