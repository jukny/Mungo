import jinja2 as j2
import Mungo.Settings

class HTMLResponse:

    def __init__(self, request, context=None, code=200):
        with open(f'{Mungo.Settings.APPLICATION_HOME}/templates/{request.template}', 'r') as h:
            self.html = h.read()
        self.code = code
        self.type = 'text/html'
        self.context = context or {}

    def __bytes__(self):
        return j2.Template(self.html).render(self.context).encode()
