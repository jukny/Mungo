from http.server import BaseHTTPRequestHandler, HTTPServer
from Mungo.persistence.GetCache import GetCache
from Mungo.persistence.ErrorCache import ErrorCache
from collections import namedtuple
from urllib.parse import parse_qs, urlparse

class HTTPError:
    E404 = '404 - Page not found'
    E0 = 'Unknown...'

class MungoServer(BaseHTTPRequestHandler):

    def __set_headers(self, response, message=''):
        self.send_response(response.code)
        if response.code == 302:
            self.send_header('Location', response.redirect)
        else:
            self.send_header('Content-type', response.content_type)
        self.end_headers()

    def do_GET(self):
        path = urlparse(self.path).path
        handler = GetCache.get(path)
        if handler.code == 404:
            self.__set_headers(handler)
            handler = ErrorCache.get(404)['handler']
            template = ErrorCache.get(404)['template']
            error = handler()
            self.wfile.write(error)
        else:
            response = handler.operation(handler)
            self.__set_headers(response)
            self.wfile.write(bytes(response))

    def do_POST(self):
        print(self.headers)


    @staticmethod
    def run(host='', port=9090):
        http_server = (host, port)
        httpd = HTTPServer(http_server, MungoServer)
        httpd.serve_forever()