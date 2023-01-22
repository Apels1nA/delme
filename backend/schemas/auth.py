from marshmallow import Schema, fields


class LoginSchema(Schema):
    """Схема для запроса логина POST"""
    email = fields.Email(required=True)
    password = fields.Str(required=True)

class UserPublicSchema(Schema):
    """Получение текущего польщователя GET"""
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    created_at = fields.DateTime(required=True)
