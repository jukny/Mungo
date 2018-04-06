from .Handler import Handler
from collections import namedtuple


class GetCache:
    __handlers = {}

    @staticmethod
    def get(key):
        handler = GetCache.__handlers.get(key)
        variables = []
        if handler:
            handler.code = 200
            return handler, namedtuple('arguments', variables)(), handler.template
        for i in [pos for pos, char in enumerate(key) if char == '/'][::-1]:
            handler = GetCache.__handlers.get(key[:i] or '/')
            if handler:
                variables = [a for a in key[i:].split('/') if a]
                break
        arguments = None
        if handler:
            handler.code = 200
            arguments = namedtuple('arguments', handler.arguments)(*variables)
        else:
            handler = Handler(None, None, 404)
        return handler, arguments, handler.template

    @staticmethod
    def set(key, handler, variables, template):
        GetCache.__handlers[key] = Handler(handler, variables, template)