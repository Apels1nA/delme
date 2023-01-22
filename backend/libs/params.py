from datetime import datetime as dt


def get_param_as_str(request, param, default=None):
    if param in request.args:
        return request.args[param][0]
    else:
        return default


def get_param_as_bool(request, param, default=None):
    return param in request.args


def get_param_as_int(request, param, default=None):
    if param in request.args:
        return int(request.args[param][0])
    else:
        return default


def get_param_as_date(request, param, default=None):
    if param in request.args:
        try:
            raw = request.args[param][0]
            return dt.strptime(raw, '%Y-%m-%d')
        except Exception:
            return default
    else:
        return default
