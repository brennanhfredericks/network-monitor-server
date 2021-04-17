import pymysql
from connection import get_connection


def get_submitter_service_data():
    """
    - post process data that was stored locally by the submission service
    """


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


def post_packets_flask_api_and_compare_db():
    """
    - only comparing numbers
    - TODO implement value comparision
    """
