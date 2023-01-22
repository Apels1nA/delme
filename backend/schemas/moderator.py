from marshmallow import Schema, fields

class ModeratorCreateSchema(Schema):
    """Создание аккаунта модератора POST"""
    name = fields.Str(required=True)
    email = fields.Email(required=True)


class ModeratorUpdateSchema(Schema):
    """Обновление данных модератора POST"""
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    is_admin = fields.Boolean(required=True)
