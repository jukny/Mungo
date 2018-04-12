from abc import ABC
from collections import namedtuple


class SQLSingleRow:

    def __init__(self, **kwargs):
        self.row = kwargs

    def __getattr__(self, item):
        if item == 'all':
            return self.row
        if item in self.row:
            return self.row.get(item)
        else:
            raise AttributeError(f'Unknown column for {self}: "{item}"')


class SQLRows:

    def __init__(self, *args):
        self.rows = list(args)

    def __getitem__(self, item):
        return self.rows[item]


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
        """
        Runs select statement against DB and return SQLList object with result.
        :param kwargs:
        :return SQLList:
        """

    @classmethod
    def __filter(cls, **kwargs):
        """
        Runs select statement against DB and returns single match.
        Error if multiple matches.
        :param kwargs: 
        :return SQLObject:
        """
        pass

    @classmethod
    def create_table(cls):
        pass


class Field:
    TEXT = 'TEXT'
    CHAR = 'TEXT'
    CLOB = 'TEXT'
    INTEGER = 'INTEGER'
    REAL = 'REAL'
    NULL = 'NULL'
    BLOB = 'BLOB'

    def __init__(self, type, default, unique, id, length):
        self.type = type
        self.default = default
        self.length = length
        self.unique = unique
        self.id = id

    def __str__(self):
        return ' '.join(filter(None, [self.type, self.default, self.unique, self.id]))

    def __iter__(self):
        ret = (
            self.type,
            self.default,
            self.length,
            self.unique,
            self.id,
        )
        for i in ret:
            yield i


class TextField(Field):

    def __init__(self, default=None, length=0, unique=False, id=False):
        super(TextField, self).__init__(
            Field.TEXT,
            f'DEFAULT {default}' if default else None,
            'UNIQUE' if unique else None,
            'ID' if id else None,
            length
        )


class IntegerField(Field):

    def __init__(self, default=None, unique=False, id=False):
        super(IntegerField, self).__init__(
            Field.INTEGER,
            f'DEFAULT {default}' if default else None,
            'UNIQUE' if unique else None,
            'ID' if id else None,
            None  # No length
        )
