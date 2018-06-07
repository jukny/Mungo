import jinja2 as j2

class HTMLResponse:

    def __init__(self, request, context=None, code=200):
        try:
            import application.settings as app
            with open(f'{app.application_home}/templates/{request.template}', 'r') as h:
                self.html = h.read()
        except ImportError:
            print('No application settings file found')
            exit(1)
        except IOError as e:
            print(e.args)
            exit(1)
        self.code = code
        self.content_type = 'text/html'
        self.context = context or {}

    def __bytes__(self):
        return j2.Template(self.html).render(self.context).encode()
