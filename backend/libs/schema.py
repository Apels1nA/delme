import falcon


def load_schema(schema):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            try:
                media = await args[1].get_media()
                if media is None:
                    args[1].parsed = {}
                    return await func(*args, **kwargs)

                load = schema().load(media)
            except Exception as e:
                raise falcon.HTTPUnprocessableEntity(description=str(e))

            args[1].parsed = load

            return await func(*args, **kwargs)

        return wrapper

    return decorator
