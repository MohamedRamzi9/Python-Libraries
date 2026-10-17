
from io import StringIO

class BaseColumn:
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

class Column(BaseColumn):
    def __init__(self, name):
        self.name = name

    def build(self):
        return self.name, []

class TableColumn(BaseColumn):
    def __init__(self, table, column):
        self.table = table
        self.column = column

    def build(self):
        return f"{self.table}.{self.column}", []
    
class Value:
    def __init__(self, value):
        self.value = value

    def build(self):
        return "%s", [self.value]

class Table:
    def __init__(self, name):
        self.name = name

    def column(self, column_name):
        return TableColumn(self.name, column_name)
    
    def build(self):
        return self.name
    
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
        left_sql, left_parameters = self.left.build()
        if self.operator == self.NOT:
            return f"NOT ({left_sql})", left_parameters
        else:
            right_sql, right_parameters = self.right.build()
            return f"({left_sql} {self.operator} {right_sql})", left_parameters + right_parameters

class Join:
    INNER = 'INNER'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'
    CROSS = 'CROSS'

    def __init__(self):
        self._type = self.INNER
        self._table = None
        self._on = None
    def on(self, condition):
        self._on = condition
        return self
    def table(self, table):
        self._table = table
        return self
    def left(self):
        self._type = self.LEFT
        return self
    def right(self):
        self._type = self.RIGHT
        return self
    def inner(self):
        self._type = self.INNER
        return self
    def cross(self):
        self._type = self.CROSS
        return self
    def build(self):
        sql = StringIO()
        sql.write(f"{self._type} JOIN {self._table.build()}")
        if self._on is not None:
            on_sql, parameters = self._on.build()
            sql.write(f" ON {on_sql}")
            return sql.getvalue(), parameters
        return sql.getvalue(), []
    
def _join_sql_and_parameters(joiner, items):
    sql_parts = []
    parameters = []
    for item in items:
        sql, values = item.build()
        sql_parts.append(sql)
        parameters.extend(values)
    return joiner.join(sql_parts), parameters

class Select:
    def __init__(self):
        self._from = []
        self._where = []
        self._column = []
        self._join = []

    def column(self, *columns):
        self._column.extend(columns)
        return self
    def from_(self, *tables):
        self._from.extend(tables)
        return self
    def where(self, *conditions):
        self._where.extend(conditions)
        return self
    def join(self, *joins):
        self._join.extend(joins)
        return self

    def build(self):
        query = StringIO()
        parameters = []

        query.write('SELECT ')
        sql, values = _join_sql_and_parameters(', ', self._column)
        query.write(sql)
        parameters.extend(values)

        query.write(' FROM ')
        query.write(', '.join([table.build() for table in self._from]))
    
        if len(self._join) > 0:
            query.write(' ')
            sql, values = _join_sql_and_parameters(' ', self._join)
            query.write(sql)
            parameters.extend(values)
        
        if self._where:
            query.write(' WHERE ')
            sql, values = _join_sql_and_parameters(' AND ', self._where)
            query.write(sql)
            parameters.extend(values)

        return query.getvalue(), parameters

class InsertInto:
    def __init__(self):
        self._into = None
        self._column = []
        self._value = []
        self._select = None

    def into(self, table):
        self._into = table
        return self
    def column(self, *columns):
        self._column.extend(columns)
        return self
    def value(self, *values):
        self._value.extend(values)
        return self
    def select(self, select_query):
        self._select = select_query
        return self

    def build(self):       
        query = StringIO() 
        parameters = []

        query.write('INSERT INTO ')
        query.write(self._into.build())

        if len(self._column) > 0:
            query.write('(')
            sql, values = _join_sql_and_parameters(', ', self._column)
            query.write(sql)
            parameters.extend(values)
            query.write(')')

        if self._select is not None:
            query.write(' ')
            sql, values = self._select.build()
            query.write(sql)
            parameters.extend(values)
        else:
            query.write(' VALUES(')
            sql, values = _join_sql_and_parameters(', ', self._value)
            query.write(sql)
            parameters.extend(values)
            query.write(')')

        return query.getvalue(), parameters

class Delete:
    def __init__(self):
        self._from = []
        self._where = []

    def from_(self, *tables):
        self._from.extend(tables)
        return self
    def where(self, *conditions):
        self._where.extend(conditions)
        return self

    def build(self):
        query = StringIO()
        parameters = []

        query.write('DELETE FROM ')
        query.write(', '.join([table.build() for table in self._from]))

        if self._where:
            query.write(' WHERE ')
            sql, values = _join_sql_and_parameters(' AND ', self._where)
            query.write(sql)
            parameters.extend(values)

        return query.getvalue(), parameters

class Assignment:
    def __init__(self, column, value):
        self.column = column
        self.value = value

    def build(self):
        column_sql, column_parameters = self.column.build()
        value_sql, value_parameters = self.value.build()
        if isinstance(self.value, Select):
            sql = f"{column_sql} = ({value_sql})"
        else:
            sql = f"{column_sql} = {value_sql}"
        parameters = column_parameters + value_parameters
        return sql, parameters

class Update:
    def __init__(self):
        self._table = None
        self._set = []
        self._where = []

    def table(self, table):
        self._table = table
        return self
    def set(self, *assignments):
        self._set.extend(assignments)
        return self
    def where(self, *conditions):
        self._where.extend(conditions)
        return self

    def build(self):
        query = StringIO()
        parameters = []

        query.write('UPDATE ')
        query.write(self._table.build())
        query.write(' SET ')

        if self._set:
            sql, values = _join_sql_and_parameters(', ', self._set)
            query.write(sql)
            parameters.extend(values)

        if self._where:
            query.write(' WHERE ')
            sql, values = _join_sql_and_parameters(' AND ', self._where)
            query.write(sql)
            parameters.extend(values)

        return query.getvalue(), parameters


table = Table('my_table')
join_table = Table('other_table')

select_query = (
    Select()
    .from_(table)
    .join(Join().left().table(join_table).on(table.column('id') == join_table.column('my_table_id')))
    .column(Column('query'), Column('status'), Value(24))
    .where(Column('query') == Value("ramzi"))
    .where((Column('status') != Value("active")) | ~Column('is_active'))
)
print(select_query.build())  

# insert_query = (
#     InsertInto()
#     .into(Table('my_table'))
#     # .column(Column('query'), Column('status'), Column('is_active'))
#     # .value(Value("ramzi"), Value('failed'), Value(False))
#     .select(select_query)
# )
# print(insert_query.build())

# delete_query = (
#     Delete()
#     .from_(Table('my_table'))
#     .where(Column('query') == Value("ramzi"))
# )
# print(delete_query.build())

# update_query = (
#     Update()
#     .table(table)
#     .set(Assignment(table.column('status'), select_query))
#     .where(table.column('query') == Value("ramzi"))
# )
# print(update_query.build())