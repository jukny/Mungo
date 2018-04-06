import jinja2 as j2

class HTMLResponse:

    def __init__(self, template_file, context=None, code=200):
        with open(f'C:/Projects/Server/{template_file}', 'r') as h:
            self.html = h.read()
        self.code = code
        self.type = 'text/html'
        self.context = context or {}

    def __bytes__(self):
        html = self.html
        if self.context:
            html = j2.Template(self.html).render(self.context)
        return html.encode()
