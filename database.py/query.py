

from enum import IntEnum
from mysql.connector import errorcode
import mysql
from io import StringIO

class Code(IntEnum):
    # Success
    OK = 0

    # Custom codes
    OTHER = -1
    PYTHON_ERROR = -2

    # Connection and authentication
    ACCESS_DENIED = errorcode.ER_ACCESS_DENIED_ERROR
    ACCESS_DENIED_DATABASE = errorcode.ER_DBACCESS_DENIED_ERROR
    UNKNOWN_DATABASE = errorcode.ER_BAD_DB_ERROR
    UNKNOWN_HOST = errorcode.CR_UNKNOWN_HOST
    CONNECTION_FAILED = errorcode.CR_CONN_HOST_ERROR
    CONNECTION_LOST = errorcode.CR_SERVER_LOST
    SERVER_GONE_AWAY = errorcode.CR_SERVER_GONE_ERROR
    TOO_MANY_CONNECTIONS = errorcode.ER_CON_COUNT_ERROR
    SERVER_SHUTDOWN = errorcode.ER_SERVER_SHUTDOWN

    # SQL and database objects
    SYNTAX_ERROR = errorcode.ER_PARSE_ERROR
    TABLE_NOT_FOUND = errorcode.ER_NO_SUCH_TABLE
    COLUMN_NOT_FOUND = errorcode.ER_BAD_FIELD_ERROR
    DATABASE_EXISTS = errorcode.ER_DB_CREATE_EXISTS
    TABLE_EXISTS = errorcode.ER_TABLE_EXISTS_ERROR
    DUPLICATE_ENTRY = errorcode.ER_DUP_ENTRY
    NO_SUCH_INDEX = errorcode.ER_KEY_DOES_NOT_EXITS

    # Data and constraints
    FOREIGN_KEY_VIOLATION = errorcode.ER_NO_REFERENCED_ROW_2
    FOREIGN_KEY_RESTRICT = errorcode.ER_ROW_IS_REFERENCED_2
    DATA_TOO_LONG = errorcode.ER_DATA_TOO_LONG
    NULL_NOT_ALLOWED = errorcode.ER_BAD_NULL_ERROR
    DATA_OUT_OF_RANGE = errorcode.ER_WARN_DATA_OUT_OF_RANGE

    # Transactions and locking
    DEADLOCK = errorcode.ER_LOCK_DEADLOCK
    LOCK_WAIT_TIMEOUT = errorcode.ER_LOCK_WAIT_TIMEOUT
    QUERY_INTERRUPTED = errorcode.ER_QUERY_INTERRUPTED

    # Protocol and unsupported operations
    COMMANDS_OUT_OF_SYNC = errorcode.CR_COMMANDS_OUT_OF_SYNC
    NOT_SUPPORTED = errorcode.ER_NOT_SUPPORTED_YET

    # Other MySQL errors
    UNKNOWN_ERROR = errorcode.ER_UNKNOWN_ERROR
    UNKNOWN_CLIENT_ERROR = errorcode.CR_UNKNOWN_ERROR
    INTERNAL_ERROR = errorcode.ER_INTERNAL_ERROR
    CLIENT_OUT_OF_MEMORY = errorcode.CR_OUT_OF_MEMORY


def convert_exception_to_code(err: Exception) -> Code:
    if isinstance(err, mysql.connector.Error):
        try:
            return Code(err.errno)
        except ValueError:
            return Code.OTHER
    return Code.PYTHON_ERROR



class Column():
    def __init__(self, name):
        self.name = name

    def build(self):
        return f"{self.name}"

    def __eq__(self, other):
        return Expression(self, Expression.EQ, other)
    def __ne__(self, other):
        return Expression(self, Expression.NE, other)
    def __lt__(self, other):
        return Expression(self, Expression.LT, other)
    def __le__(self, other):
        return Expression(self, Expression.LE, other)
    def __gt__(self, other):
        return Expression(self, Expression.GT, other)
    def __ge__(self, other):
        return Expression(self, Expression.GE, other)

    def __and__(self, other):
        return Expression(self, Expression.AND, other)
    def __or__(self, other):
        return Expression(self, Expression.OR, other)
    def __invert__(self):
        return Expression(self, Expression.NOT, None)

class Value():
    def __init__(self, value):
        self.value = value

    def build(self):
        if isinstance(self.value, str):
            return f"'{self.value}'"
        return f"{self.value}"


class Expression:
    AND = 'AND'
    OR = 'OR'
    NOT = 'NOT'
    EQ = '='
    NE = '!='
    LT = '<'
    LE = '<='
    GT = '>'
    GE = '>='

    def __and__(self, other):
        return Expression(self, self.AND, other)
    def __or__(self, other):
        return Expression(self, self.OR, other)
    def __invert__(self):
        return Expression(self, self.NOT, None)


    def __init__(self, left, operator, right=None):
        self.operator = operator
        self.left = left
        self.right = right

    def build(self):
        if self.operator == self.NOT:
            return f"NOT ({self.left.build()})"
        else:
            return f"({self.left.build()} {self.operator} {self.right.build()})"

class Query:
    SELECT = 'SELECT'
    INSERT = 'INSERT'
    UPDATE = 'UPDATE'
    DELETE = 'DELETE'

    def __init__(self):
        self._type = None
        self._from = []
        self._where = []
        self._column = []
        self._value = []

    def select(self): 
        self._type = self.SELECT
        return self
    def from_(self, *tables):
        self._from.extend(tables)
        return self
    def insert(self):
        self._type = self.INSERT
        return self
    def into(self, *tables):
        self._from.extend(tables)
        return self
    def where(self, *conditions):
        self._where.extend(conditions)
        return self
    def column(self, *columns):
        self._column.extend(columns)
        return self
    def value(self, *values):
        self._value.extend(values)
        return self

    def build(self):
        query = StringIO()
        if self._type == self.SELECT:
            query.write(f'{self._type} ')
            query.write(', '.join(self._column))
            query.write(' FROM ')
            query.write(', '.join(self._from))
        elif self._type == self.INSERT:
            query.write(f'{self._type} INTO ')
            query.write(', '.join(self._from))
            if len(self._column) > 0:
                query.write('(')
                query.write(', '.join(self._column))
                query.write(')')
            query.write(' VALUES(')
            query.write(', '.join([Value(v).build() for v in self._value]))
            query.write(')')

        if self._where:
            query.write(' WHERE ')
            query.write(' AND '.join([expr.build() for expr in self._where]))
        return query.getvalue()

query = (
    Query().select()
    .column('query', 'status', 'is_active').from_('my_table')
    .where((Column('query') == Value(2)))
    .where((Column('status') != Value('failed')) | ~Column('is_active'))
)
print(query.build())  

query = (
    Query().insert()
    .into('my_table')
    .column('query', 'status', 'is_active')
    .value(2, 'failed', False)
)
print(query.build())