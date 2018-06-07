from functools import wraps
from re import sub, findall
from Mungo.persistence.PostCache import PostCache


def __split(context):
    variables = tuple(findall(':([A-Za-z0-9_\-]+)', context))
    root = sub('/:([A-Za-z0-9_\-]+)', '', context)
    return variables, root


def post_handler(context, template='', authenticate=False, login_url='', redirect=''):
    def wrapper(fn):
        wraps(fn)
        variables, root = __split(context)
        PostCache.set(
            key=root,
            handler=fn,
            variables=variables,
            template=template,
            authenticate=authenticate,
            login_url=login_url,
            redirect=redirect
        )
        return fn
    return wrapper
