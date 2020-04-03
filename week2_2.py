from json import dumps
from functools import wraps


def to_json(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        return dumps(func(*args, **kwargs))
    return wrapped
