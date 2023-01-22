import falcon
import hashlib

from config import config
from models.user import User
from libs.redis import Redis


def get_user(user_session):
    user_id = Redis.get(user_session)

    if not user_id:
        raise falcon.HTTPUnauthorized()

    return User.get_by_id(user_id)


def get_or_none_user(user_session):

    user_id = Redis.get(user_session)

    if user_id:
        user = User.get_or_none(User.id == user_id)
    else:
        user = None

    return user


async def auth_required(req, resp, resource, params):

    if 'user_session' not in req.cookies:
        raise falcon.HTTPUnauthorized()

    user = get_user(req.cookies['user_session'])

    resource.user = user


async def login_required(req, resp, resource, params):

    if 'user_session' in req.cookies:
        user = get_or_none_user(req.cookies.get('user_session'))
    else:
        user = None

    resource.user = user


async def owner_claim_required(req, resp, resource, params):

    if 'user_session' not in req.cookies:
        raise falcon.HTTPUnauthorized()

    user = get_user(req.cookies['user_session'])

    if not user or not user.is_owner:
        raise falcon.HTTPUnauthorized()

    resource.user = user


async def owner_required(req, resp, resource, params):

    if 'user_session' not in req.cookies:
        raise falcon.HTTPUnauthorized()

    user = get_user(req.cookies['user_session'])

    if not user or not user.is_owner and not user.is_admin:
        raise falcon.HTTPUnauthorized()

    resource.user = user


async def admin_required(req, resp, resource, params):

    if 'user_session' not in req.cookies:
        raise falcon.HTTPUnauthorized()

    user = get_user(req.cookies['user_session'])

    if not user:
        raise falcon.HTTPUnauthorized()

    if not user.is_admin or not user.is_active:
        raise falcon.HTTPUnauthorized()

    resource.user = user


async def check_localization(req, resp, resource, params):

    if 'localization' in req.cookies:
        resource.localization = req.cookies['localization']

    else:
        resource.localization = 'ru'


def make_session(credential, user_data, user_id):

    user_credential = credential+config['secure']['salt_session']+user_data
    session = hashlib.sha256(user_credential.encode()).hexdigest()
    Redis.set(session, user_id)

    return session


def remove_session(session):
    Redis.delete(session)
