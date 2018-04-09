import jinja2 as j2

class HTMLResponse:

    def __init__(self, request, context=None, code=200):
        with open(f'C:/Projects/Server/app/templates/{request.template}', 'r') as h:
            self.html = h.read()
        self.code = code
        self.type = 'text/html'
        self.context = context or {}

    def __bytes__(self):
        html = self.html
        if self.context:
            html = j2.Template(self.html).render(self.context)
        return html.encode()
