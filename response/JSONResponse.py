from json import dumps


class JSONResponse:
    def __init__(self, request, json_dict, code=200):
        self.json = dumps(json_dict)
        self.code = code
        self.content_type = 'application/json'

    def __bytes__(self):
        return self.json.encode()