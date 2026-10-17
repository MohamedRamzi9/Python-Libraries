
from enum import IntEnum
from mysql.connector import errorcode
import mysql

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

    def ok(self):
        return self == Code.OK

def convert_exception_to_code(err: Exception) -> Code:
    if isinstance(err, mysql.connector.Error):
        try:
            return Code(err.errno)
        except ValueError:
            return Code(Code.OTHER)
    return Code(Code.PYTHON_ERROR)

class Cursor:
    def __init__(self, cursor):
        self._cursor = cursor

    def execute(self, query, params=None):
        try:
            self._cursor.execute(query, params)
            return Code(Code.OK)
        except mysql.connector.Error as e:
            return convert_exception_to_code(e)

    def fetch_all(self):
        try:
            return Code(Code.OK), self._cursor.fetchall()
        except mysql.connector.Error as e:
            return convert_exception_to_code(e), None

    def fetch_one(self):
        try:
            return Code(Code.OK), self._cursor.fetchone()
        except mysql.connector.Error as e:
            return convert_exception_to_code(e), None

    def fetch_many(self, size):
        try:
            return Code(Code.OK), self._cursor.fetchmany(size)
        except mysql.connector.Error as e:
            return convert_exception_to_code(e), None

    def close(self):
        try:
            self._cursor.close()
            return Code(Code.OK)
        except mysql.connector.Error as e:
            return convert_exception_to_code(e)

    def last_row_id(self):
        return self._cursor.lastrowid
    def row_count(self):
        return self._cursor.rowcount
    


if __name__ == "__main__":
    code = Code(Code.OK)
    if code.ok():
        print("Code is OK")
    code = Code(Code.ACCESS_DENIED)
    if code == Code.ACCESS_DENIED:
        print("Access denied error")