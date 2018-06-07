class Handler:
    def __init__(self, operation, arguments, redirect='', template='', authenticate=False,
                 login_url='', content_type='text/html'):
        self.operation = operation
        self.arguments = arguments
        self.template = template
        self.authenticate = authenticate
        self.login_url = login_url
        self.redirect = redirect
        self.content_type = content_type
        self.code = 302 if redirect else 200
        self.query = None
        self.path = None

    def __repr__(self):
        return f'{self.operation}:{self.arguments}:{self.content_type}'