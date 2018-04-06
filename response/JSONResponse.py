import jinja2 as j2


class JSONResponse:
    def __init__(self, request, context=None, code=200):
        with open(f'C:/Projects/Server/{request.template}', 'r') as h:
            self.json = h.read()
        self.code = code
        self.type = 'application/json'
        self.context = context or {}

    def __bytes__(self):
        json = self.json
        if self.context:
            html = j2.Template(self.json).render(self.context)
        return json.encode()