from .Handler import Handler
from collections import namedtuple
from urllib.parse import parse_qs, urlparse

class GetCache:
    __handlers = {
       #'/favicon.ico': Handler(lambda x: x, None)
    }

    @staticmethod
    def get(key):
        handler = GetCache.__handlers.get(key)
        variables = []
        if handler:
            handler.code = 200 if handler.redirect == '' else 302
            handler.arguments = namedtuple('arguments', variables)()
            handler.path = key
            return handler
        for i in [pos for pos, char in enumerate(key) if char == '/'][::-1]:
            handler = GetCache.__handlers.get(key[:i] or '/')
            if handler:
                variables = [a for a in key[i:].split('/') if a]
                break
        if handler:
            handler.code = 200 if handler.redirect == '' else 302
            handler.arguments = namedtuple('arguments', handler.arguments)(*variables)
        else:
            handler = Handler(None, None)
            handler.code = 404
        query = {k: v[0] for k, v in parse_qs(urlparse(key).query).items()}
        handler.query = namedtuple('query', query.keys())(**query)
        handler.path = key
        return handler

    @staticmethod
    def set(key, handler, variables, template, authenticate, login_url, content_type, redirect=''):
        GetCache.__handlers[key] = Handler(
            operation=handler,
            arguments=variables,
            template=template,
            authenticate=authenticate,
            login_url=login_url,
            content_type=content_type,
            redirect=redirect
        )