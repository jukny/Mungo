from .Handler import Handler
from collections import namedtuple
from urllib.parse import parse_qs, urlparse

class PostCache:
    __handlers = {
       #'/favicon.ico': Handler(lambda x: x, None)
    }

    @staticmethod
    def get(key):
        handler = PostCache.__handlers.get(key)
        variables = []
        if handler:
            handler.code = 302 if handler.redirect else 200
            return handler, namedtuple('arguments', variables)(), handler.template
        for i in [pos for pos, char in enumerate(key) if char == '/'][::-1]:
            handler = PostCache.__handlers.get(key[:i] or '/')
            if handler:
                variables = [a for a in key[i:].split('/') if a]
                break
        arguments = None
        if handler:
            handler.code = 302 if handler.redirect else 200
            arguments = namedtuple('arguments', handler.arguments)(*variables)
        else:
            handler = Handler(None, None, code=404)
        return handler, arguments, handler.template

    @staticmethod
    def set(key, handler, variables, template, authenticate, login_url, redirect):
        PostCache.__handlers[key] = Handler(
            operation=handler,
            arguments=variables,
            redirect=redirect,
            template=template,
            authenticate=authenticate,
            login_url=login_url
        )