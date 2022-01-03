import re
import psycopg2
from typing import Union


class PsqlRequests:
    def __init__(self,  host=None, user=None, password=None, database=None):
        self.__host = "127.0.0.1"
        self.__user = "postgres"
        self.__password = "Y5n1e887k69"
        self.__database = "bcac"

        self.IS_CONNECT = False

        if host:
            self.__host = host
        if user:
            self.__user = user
        if password:
            self.__password = password
        if database:
            self.__database = database

        try:
            self.__psql = psycopg2.connect(
                host=self.__host,
                user=self.__user,
                password=self.__password,
                database=self.__database)
        except psycopg2.OperationalError:
            return

        self._cursor = self.__psql.cursor()
        self.IS_CONNECT = True

    def select(self, from_to_take: str, what_to_take: Union[list, str] = None, fetch_one: bool = False,
               join: list = None, select_exceptions: list = None,
               order_by: str = None, distinct: bool = False, desc=False, where: list = None) -> tuple:
        if not self.IS_CONNECT:
            return (None, )

        if isinstance(what_to_take, list):
            for i in range(len(what_to_take)):
                if re.match(r'[\w\d]+\.\*', what_to_take[i]):
                    what_to_take[i] = self._replace_to_column_name(what_to_take[i], select_exceptions)

            what_to_take = ", ".join(what_to_take)
        elif not what_to_take:
            what_to_take = "*"

        if join:
            if len(join) > 1:   # if we want to join multiple tables (3 and more)
                join_text = ''
                for join_request in join:
                    text = f'JOIN {join_request[0]} ON item.{join_request[1]} = {join_request[0]}.id'   # form the join request
                    join_text += text + ' '     # and combine this request with others
            else:
                join_text = f'JOIN {join[0][0]} ON item.{join[0][1]} = {join[0][0]}.id'
        else:
            join_text = ''

        if order_by:
            order_by = 'ORDER BY ' + order_by
        else:
            order_by = ''

        distinct_values = {
            True: 'DISTINCT',
            False: ''
        }
        distinct = distinct_values[distinct]

        sort_from_values = {
            True: 'DESC',
            False: 'ASC'
        }

        if join:
            sort_from = ''
        else:
            sort_from = sort_from_values[desc]

        where_text = self.__generate_where_text(where)

        self._cursor.execute(
            f"SELECT {distinct} {what_to_take} FROM {from_to_take} {order_by} {sort_from} {join_text} {where_text}"
        )

        if fetch_one:
            return self._cursor.fetchone()
        return self._cursor.fetchall()

    def _replace_to_column_name(self, what_to_take: list, select_exceptions: list = None) -> str:
        select_from = what_to_take[:-2]

        self._cursor.execute(f"SELECT * FROM {select_from} LIMIT 0")
        columns_names = [desc[0] for desc in self._cursor.description]

        finally_text = ''

        for column_name in columns_names:
            finally_text += f'{select_from}.{column_name}, '

        for exception in select_exceptions:
            exception = ', ' + exception
            if exception in finally_text:
                finally_text = finally_text.replace(exception, '')

        return finally_text[:-2]

    def __generate_where_text(self, where_request):
        if not where_request:
            return ''

        where_text = 'WHERE '
        for element in where_request[1]:
            where_text += f'{where_request[0]} = {element}'

            if element == where_request[1][-1]: break
            where_text += ' OR '

        return where_text

    def insert(self, table: str, rows: list, what_to_insert: list):
        rows = ', '.join(rows)
        what_to_insert = ', '.join(what_to_insert)

        self._cursor.execute(f"INSERT INTO {table} ({rows}) VALUES ({what_to_insert});")

    def execute(self, command: str):
        self._cursor.execute(command)

        return self._cursor.fetchall()

    def special_select(self, column, table):
        column = 'LOWER(' + column + ')'
        self._cursor.execute(f"SELECT {table}.id, {column} FROM {table}")

        return self._cursor.fetchall()

    def close(self):
        self._cursor.close()
        self.__psql.close()
