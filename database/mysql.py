import os
from jinjasql import JinjaSql
import pymysql
from settings import MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, SHOES_DATABASE
from pymysql.constants import CLIENT

CONTEXT_PATH = 'context'

sql_conn = None
sql_formatter = JinjaSql()


def db_connection(is_migrate=False):
    return pymysql.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=SHOES_DATABASE if not is_migrate else None,
        client_flag=CLIENT.MULTI_STATEMENTS,
        cursorclass=pymysql.cursors.DictCursor
    )


def execute_query(query_name, fetch_data=False, **kwargs):
    if sql_conn:
        query = open(os.path.join(CONTEXT_PATH, query_name), 'r', encoding='utf-8').read()
        formated_query, bind_params = sql_formatter.prepare_query(query, kwargs)
        with sql_conn.cursor() as cursor:
            cursor.execute(formated_query, bind_params)
            if fetch_data:
                return cursor.fetchall()
    else:
        raise Exception('Need to initialize DB connection first')
