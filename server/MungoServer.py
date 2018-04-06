from http.server import BaseHTTPRequestHandler, HTTPServer
from ..persistence.GetCache import GetCache
from collections import namedtuple
from urllib.parse import parse_qs, urlparse

class MungoSever(BaseHTTPRequestHandler):

    def __set_headers(self, response, message=''):
        self.send_response(response.code, message=message )
        self.send_header('Content-type', response.type)
        self.end_headers()

    def do_GET(self):
        path = urlparse(self.path).path
        handler, arguments, template = GetCache.get(path)
        query = {key:val[0] for key, val in parse_qs(urlparse(self.path).query).items()}
        if handler.code != 200:
            self.__set_headers(handler)
            self.wfile.write(f'404 - Page not found: {self.path}'.encode())
        else:
            args = namedtuple('arguments', ['path', 'arguments', 'query', 'template'])(
                self.path,
                arguments,
                namedtuple('query', query.keys())(**query),
                template
            )
            response = handler.operation(args)
            self.__set_headers(response)
            self.wfile.write(bytes(response))

    def do_POST(self):
        pass

    @staticmethod
    def run(host='', port=9090):
        http_server = (host, port)
        httpd = HTTPServer(http_server, MungoSever)
        httpd.serve_forever()