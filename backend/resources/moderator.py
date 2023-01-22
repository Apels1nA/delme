from hashlib import sha256

import falcon
from peewee import DoesNotExist
from datetime import datetime

from config import config
from libs import Controller
from libs.auth import auth_required
from libs.schema import load_schema
from libs.email_sendler import send_email
from libs.password_generator import password_generator

from schemas.moderator import ModeratorCreateSchema, ModeratorUpdateSchema
from schemas.auth import UserPublicSchema

from models import User


class ModeratorController(Controller):
    @load_schema(ModeratorCreateSchema)
    @falcon.before(auth_required)
    async def on_post(self, req, resp):
        if not self.user.is_admin:
            raise falcon.HTTPForbidden(description='Not enough rights')

        user = User.get_or_none(email=req.parsed['email'])

        if user is not None:
            raise falcon.HTTPBadRequest(description='User already exist')

        generated_password = password_generator(config['email']['password_length'])
        send_email(
            to_addr=req.parsed['email'],
            subject='',
            body_text=f"Login: {req.parsed['email']}\nPassword: {generated_password}"
        )

        password_with_salt = generated_password + config['secure']['salt_password']
        user = User.create(
            name=req.parsed['name'],
            email=req.parsed['email'],
            password=sha256(password_with_salt.encode()).hexdigest(),
            is_admin=False,
            created_at=datetime.now()
        )

        resp.text = UserPublicSchema().dump(user)

    @falcon.before(auth_required)
    async def on_get(self, req, resp):
        if not self.user.is_admin:
            raise falcon.HTTPForbidden(description='Not enough rights')

        limit = req.get_param_as_int('limit', 10)
        page = req.get_param_as_int('page', 1)
        offset = limit * (page - 1)

        sample_moderators = User.select().where(User.is_admin==False).offset(offset).limit(limit)
        for x in sample_moderators:
            print(x.email)
        resp.text = UserPublicSchema(many=True).dump(sample_moderators)


class ModeratorByIDController(Controller):
    @falcon.before(auth_required)
    async def on_post(self, req, resp, id: int):
        if not self.user.is_admin:
            raise falcon.HTTPForbidden(description='Not enough rights')

        user = User.get_or_none(id=id)
        if user is None:
            raise falcon.HTTPBadRequest(description='User does not exist')

        generated_password = password_generator(config['email']['password_length'])
        send_email(
            to_addr=user.email,
            subject='',
            body_text=f"Login: {user.email}\nPassword: {generated_password}"
        )

        password_with_salt = generated_password + config['secure']['salt_password']
        user.password=sha256(password_with_salt.encode()).hexdigest()
        user.save()

        resp.text = UserPublicSchema().dump(user)

    @falcon.before(auth_required)
    async def on_get(self, req, resp, id: int):
        if not self.user.is_admin:
            raise falcon.HTTPForbidden(description='Not enough rights')

        try:
            resp.text = UserPublicSchema().dump(User.get_by_id(id))
        except DoesNotExist:
            raise falcon.HTTPBadRequest(description='User does not exist')

    @falcon.before(auth_required)
    async def on_delete(self, req, resp, id: int):
        if not self.user.is_admin:
            raise falcon.HTTPForbidden(description='Not enough rights')

        try:
            if self.user.id != id:
                User.delete_by_id(id)
            else:
                raise falcon.HTTPBadRequest(description='You cant delete yourself')
        except DoesNotExist:
            raise falcon.HTTPBadRequest(description='User does not exist')

    @falcon.before(auth_required)
    @load_schema(ModeratorUpdateSchema)
    async def on_put(self, req, resp, id: int):
        if not self.user.is_admin:
            raise falcon.HTTPForbidden(description='Not enough rights')

        try:
            user = User.get_by_id(id)
            user.name = req.parsed['name']
            user.email = req.parsed['email']
            user.is_admin = req.parsed['is_admin']
            user.save()

            resp.text = UserPublicSchema().dump(user)
        except DoesNotExist:
            raise falcon.HTTPBadRequest(description='User does not exist')
