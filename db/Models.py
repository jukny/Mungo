from abc import ABC
from collections import namedtuple


class ClassProperty(property):
    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()


class Model(ABC):

    @ClassProperty
    def objects(cls):
        try:
            from application import Models
            return namedtuple('DbOperations', ('get', 'filter'))(cls.__get, cls.__filter)
        except ImportError:
            pass

    @classmethod
    def __get(cls, **kwargs):
        keys = [d for d in dir(cls) if not d.startswith('_') and d in kwargs.keys() and d != 'objects']
        select = f'SELECT * FROM {cls.__name__} WHERE'
        for key in keys:
            select += f" {key} == '{kwargs[key]}' AND"
        return select[:-3]

    @classmethod
    def __filter(cls):
        pass

class Field:
    TEXT='TEXT'
    INTEGER='INTEGER'


class TextField(Field):

    def __init__(self, default='', length=256, unique=False):
        self.type = self.TEXT
        self.default = default
        self.length = length
        self.unique = unique


    def __dict__(self):
        ret = (
            ('type', self.type),
            ('default', self.default),
            ('length', self.length),
            ('unique', self.unique)
        )
        for i in ret:
            yield i