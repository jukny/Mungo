class Handler:
    def __init__(self, operation, arguments, code=0):
        self.operation = operation
        self.arguments = arguments
        self.code = code
        self.type = 'text/html'

    def __repr__(self):
        return f'{self.operation}:{self.arguments}:{self.code}:{self.type}'