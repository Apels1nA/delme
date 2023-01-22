import falcon


def _gen_error(req: falcon.Request, resp: falcon.Response):
    resp.status = falcon.HTTPStatus(falcon.HTTP_METHOD_NOT_ALLOWED)
    resp.text = {
        "error": {
            "code": 405,
            "detail": f"Method {req.method.upper()} is not support",
        }
    }


class Controller:
    async def on_get(self, req: falcon.Request, resp: falcon.Response):
        return _gen_error(req, resp)

    async def on_post(self, req: falcon.Request, resp: falcon.Response):
        return _gen_error(req, resp)

    async def on_patch(self, req: falcon.Request, resp: falcon.Response):
        return _gen_error(req, resp)

    async def on_put(self, req: falcon.Request, resp: falcon.Response):
        return _gen_error(req, resp)

    async def on_delete(self, req: falcon.Request, resp: falcon.Response):
        return _gen_error(req, resp)
