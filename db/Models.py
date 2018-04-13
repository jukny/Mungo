from abc import ABC
from collections import namedtuple
import sqlite3
import re

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

    def __getitem__(self, item):
        return self.row.get(item)

    def __repr__(self):
        return f'<SQLRow {self.all}>'

    def get(self, item):
        return self.row.get(item)


class SQLRows:

    def __init__(self, *args):
        self.rows = args

    def __getitem__(self, item):
        return self.rows[item]

    def __len__(self):
        return len(self.rows)

    def __repr__(self):
        r = str([a for a in self.rows])
        return f'<SQLRows: {r}>'

    def filter(self, **kwargs):
        return SQLRows(*(r for r in self.rows if kwargs.items() <= r.all.items()))



class ClassProperty(property):
    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()


class Model(ABC):
    @ClassProperty
    def objects(cls):
        try:
            from application import Models
            return namedtuple('DbOperations', ('get', 'filter', 'set', 'create'))(
                cls.__get,
                cls.__filter,
                cls.__set,
                cls.__create_table
            )
        except ImportError:
            pass

    @classmethod
    def __get(cls, **kwargs):
        """
        Runs select statement against DB and return SQLList object with result.
        :param kwargs:
        :return SQLList:
        """
        cols = ', '.join(sorted([c for c in dir(cls) if not c.startswith("_") and c != "objects"]))
        cols += ', id'
        statement = f"SELECT {cols} FROM {cls.__name__}"
        keys = ' AND '.join([ f"{v[0]}='{v[1]}'" for v in kwargs.items()])
        if keys:
            statement += f' WHERE {keys}'
        connection = sqlite3.connect('C:/Projects/server/application/app.db')
        cursor = connection.cursor()
        result = cursor.execute(statement)
        cols = sorted([k for k in cls.__dict__ if not k.startswith('_') and k != 'objects'])
        cols.append('id')
        return SQLRows(*[ SQLSingleRow(**dict(zip(cols, row))) for row in result ])


    @classmethod
    def __set(cls, **kwargs):
        """
        Set row in table
        :param kwargs:
        :return Boolean:
        """
        statement = f"""INSERT INTO {cls.__name__} 
        ({', '.join([v[0] for v in kwargs.items()])}) 
        VALUES ({", ".join([f"'{v[1]}'" for v in kwargs.items()])})"""
        connection = sqlite3.connect('C:/Projects/server/application/app.db')
        cursor = connection.cursor()
        try:
            cursor.execute(statement)
            connection.commit()
            return True
        except sqlite3.Error as e:
            print(e)
            return False




    @classmethod
    def __filter(cls, **kwargs):
        """
        Runs select statement against DB and returns single match.
        Error if multiple matches.
        :param kwargs: 
        :return SQLObject:
        """
        cols = ', '.join(sorted([c for c in dir(cls) if not c.startswith("_") and c != "objects"]))
        cols += ', id'
        statement = f"SELECT {cols} FROM {cls.__name__}"
        keys = ' AND '.join([ f"{v[0]}='{v[1]}'" for v in kwargs.items()])
        if keys:
            statement += f' WHERE {keys}'
        connection = sqlite3.connect('C:/Projects/server/application/app.db')
        cursor = connection.cursor()
        result = cursor.execute(statement)
        cols = sorted([k for k in cls.__dict__ if not k.startswith('_') and k != 'objects'])
        cols.append('id')
        return SQLSingleRow(**dict(zip(cols, list(result)[0])))

    @classmethod
    def __create_table(cls):
        columns = [f'{c} {str(getattr(cls, c))}' for c in dir(cls) if not c.startswith('_') and c != 'objects']
        if not list(filter(lambda b: re.compile(r'\b(ID)\b').search(b), columns)):
            columns.append('id INTEGER PRIMARY KEY AUTOINCREMENT')
            #cls.id = 'id INTEGER PRIMARY KEY AUTOINCREMENT'
        statement = f'CREATE TABLE {cls.__name__} ({", ".join(columns)})'
        connection = sqlite3.connect('C:/Projects/server/application/app.db')
        cursor = connection.cursor()
        try:
            print(statement)
            cursor.execute(statement)
            return True
        except sqlite3.Error as e:
            print(e)
            return False


class Field:
    TEXT = 'TEXT'
    CHAR = 'TEXT'
    CLOB = 'TEXT'
    INTEGER = 'INTEGER'
    REAL = 'REAL'
    NULL = 'NULL'
    BLOB = 'BLOB'

    def __init__(self, type, default, unique, primary_key, length):
        self.type = type
        self.default = default
        self.length = length
        self.unique = unique
        self.id = primary_key

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

    def __init__(self, default=None, length=0, unique=False, primary_key=False):
        super(TextField, self).__init__(
            Field.TEXT,
            f'DEFAULT {default}' if default else None,
            'UNIQUE' if unique else None,
            'PRIMARY KEY' if primary_key else None,
            length
        )


class IntegerField(Field):

    def __init__(self, default=None, unique=False, primary_key=False):
        super(IntegerField, self).__init__(
            Field.INTEGER,
            f'DEFAULT {default}' if default else None,
            'UNIQUE' if unique else None,
            'PRIMARY KEY' if primary_key else None,
            None  # No length
        )
