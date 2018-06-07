import jinja2 as j2


def default404(context_path, dummy=''):
    html = f"""
        <html>
        <head>
        <title>Error - 404</title>
        <body>
            <h2> {context_path} not found </h2>
        </body>
        </html>
    """
    return html.encode()

class ErrorCache:
    __handlers = {
        404: {
            'handler': default404,
            'template': ''
        }
    }

    @staticmethod
    def get(key):
        return ErrorCache.__handlers.get(key)

    @staticmethod
    def set(key, handler, template):
        ErrorCache.__handlers[key] = { 'handler': handler, 'template': template }