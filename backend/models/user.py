from datetime import datetime

from peewee import TextField, DateTimeField, BooleanField

from db import BaseModel


class User(BaseModel):
    """
    Модель администратора
    """

    name = TextField(null=False)
    email = TextField(null=False, unique=True)
    password = TextField(null=False)
    is_admin = BooleanField(null=False)
    created_at = DateTimeField(null=False, default=datetime.now())
