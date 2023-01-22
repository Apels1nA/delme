from falcon.asgi import App

from routing import make_app

app = App()
app.resp_options.secure_cookies_by_default = False
make_app(app)
