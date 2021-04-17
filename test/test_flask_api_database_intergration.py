import pymysql
from connection import get_connection


def count_packets_in_db():
    # connection to database

    conn = get_connection()

    with conn:

        with conn.cursor() as cursor:

            sql = "SELECT COUNT(id) FROM packet"
            cursor.execute(sql)
            (res,) = cursor.fetchone()

    return res


def test_count_packets_in_db():

    count_packets_in_db()
