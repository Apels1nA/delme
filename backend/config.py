import os
from enum import Enum

from environs import Env

env = Env()
env.read_env()


class MODE(Enum):
    PROD = 'production'
    DEV = 'develop'

    @classmethod
    def get_mode(cls) -> "MODE":
        members = {member.value: member for member in MODE.__members__.values()}
        return getattr(
            cls, APP_MODE.upper(),
            members.get(APP_MODE.lower(), MODE.DEV)
        )

    @classmethod
    def is_production(cls) -> bool:
        return cls.get_mode() == cls.PROD

    @classmethod
    def is_development(cls) -> bool:
        return cls.get_mode() == cls.DEV


APP_MODE = os.environ.get('APP_MODE', 'production')
config = {
    'project': {
        'project': env('PROJECT_NAME'),
        'version': env('PROJECT_VERSION'),
        'mode': env('APP_MODE'),
    },
    'db': {
        'host': env('DB_HOST', env('POSTGRES_HOST', None)),
        'db': env('DB_NAME', env('POSTGRES_DB', None)),
        'user': env('DB_USER', env('POSTGRES_USER', None)),
        'password': env('DB_PASSWORD', env('POSTGRES_PASSWORD', None)),
        'port': env('DB_PORT', env('POSTGRES_PORT', None)),
    },
    'secure': {
        'salt_password': env('SALT_PASSWORD'),
        'salt_session': env('SALT_SESSION'),
        'admin_password': env('ADMIN_PASSWORD')
    },
    'redis': {
        'address': (os.getenv('ip'), 6379),
        'encoding': env('REDIS_ENCODING'),
    },
    'email': {
        'host': env('HOST'),
        'port': env.int('PORT'),
        'login': env('LOGIN'),
        'password': env('PASSWORD'),
        'password_length': env.int('PASSWORD_LENGTH'),
    }
}