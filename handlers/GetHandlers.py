from functools import wraps
from re import sub, findall
from ..persistence.GetCache import GetCache


def __split(context):
    variables = tuple(findall(':([A-Za-z0-9_\-]+)', context))
    root = sub('/:([A-Za-z0-9_\-]+)', '', context)
    return variables, root


def get_handler(context, template='', authenticate=False, login_url='', content_type='text/html', redirect=''):
    def wrapper(fn):
        wraps(fn)
        variables, root = __split(context)
        GetCache.set(root, fn, variables, template, authenticate, login_url, content_type, redirect)
        return fn
    return wrapper
