import json

from hashlib import sha256

import falcon
from datetime import datetime, timedelta

from config import config
from libs import Controller
from libs.auth import auth_required, make_session, remove_session
from libs.schema import load_schema
from schemas.auth import LoginSchema, UserPublicSchema

from models import User


class LoginController(Controller):
    @load_schema(LoginSchema)
    async def on_post(self, req, resp):
        user = User.get_or_none(email=req.parsed['email'])

        if user is None:
            raise falcon.HTTPNotFound(description='User does not exist')

        password_with_salt = req.parsed['password'] + config['secure']['salt_password']
        if user.password != sha256(password_with_salt.encode()).hexdigest():
            raise falcon.HTTPUnauthorized(description='Wrong password')

        resp.set_cookie(
            name='user_session',
            value=make_session(
                credential='',
                user_data=req.host + req.user_agent,
                user_id=user.id
            ),
            path='/',
            max_age=1209600,
            expires=datetime.now() + timedelta(days=14)
        )

        resp.text = UserPublicSchema().dump(user)


class CurrentUserController(Controller):
    @falcon.before(auth_required)
    async def on_get(self, req, resp):
        resp.text = UserPublicSchema().dump(self.user)


class LogoutController(Controller):
    @falcon.before(auth_required)
    async def on_get(self, req, resp):
        remove_session(req.cookies['user_session'])

        resp.unset_cookie('user_session')
        resp.body = json.dumps({'success': True})
