from functools import wraps
from re import sub, findall
from ..persistence.GetCache import GetCache


def __split(context):
    variables = tuple(findall(':([A-Za-z0-9_\-]+)', context))
    root = sub('/:([A-Za-z0-9_\-]+)', '', context)
    return variables, root


def get_handler(context, template=''):
    def wrapper(fn):
        wraps(fn)
        variables, root = __split(context)
        GetCache.set(root, fn, variables, template)
        return fn
    return wrapper
