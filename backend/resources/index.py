from config import config


class IndexController:

    async def on_get(self, req, resp):
        resp.text = config['project']
