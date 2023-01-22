import json

from traceback import print_exc
from typing import Optional

import falcon
from falcon.asgi import App

from config import MODE
from resources import *


class JSONMiddleware:
    def __init__(self):
        import termcolor
        try:
            import orjson as json
            print("Usage", termcolor.colored("orjson", 'green'))
        except ImportError:
            try:
                import ujson as json
                print("Usage", termcolor.colored("ujson", 'yellow'))
            except ImportError:
                import json
                print("Usage", termcolor.colored("json", 'red'))
            from functools import partial
            json.dumps = partial(json.dumps, ensure_ascii=False)
        self.dumps = json.dumps

    def process_response(
            self,
            req: falcon.Request,
            resp: falcon.Response,
            resource: Optional[object],
            req_succeeded: bool
    ):
        if req_succeeded and isinstance(resp.text, (list, dict)):
            resp.text = self.dumps(resp.text)

    async def process_response_async(
            self,
            req: falcon.Request,
            resp: falcon.Response,
            resource: Optional[object],
            req_succeeded: bool
    ):
        return self.process_response(req, resp, resource, req_succeeded)


async def all_error_handler(req: falcon.Request, resp, ex: Exception, params, ws=None):
    print_exc()
    resp.status = 500
    body = {
        "name": "Internal server error",
    }
    if MODE.is_development():
        body.update(
            name=type(ex).__name__,
            detail=str(ex)
        )

    resp.text = json.dumps({
        "error": body
    })


def make_app(app: App):
    app.add_route('/', IndexController())

    app.add_route('/login', LoginController())
    app.add_route('/logout', LogoutController())

    app.add_route('/user/current', CurrentUserController())

    app.add_route('/admin/moderator/create', ModeratorController())
    app.add_route('/admin/moderator/list', ModeratorController())
    app.add_route('/admin/moderator/{id:int}', ModeratorByIDController())

    app.add_middleware(JSONMiddleware())
    app.add_error_handler(Exception, all_error_handler)

    return app
