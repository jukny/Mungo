from functools import wraps
from Mungo.persistence.ErrorCache import ErrorCache

def E404_handler(template=''):
    def wrapper(fn):
        wraps(fn)
        ErrorCache.set(404, fn, template)
        return fn
    return wrapper

def E401_handler(template=''):
    def wrapper(fn):
        wraps(fn)
        ErrorCache.set(401, fn, template)
        return fn
    return wrapper