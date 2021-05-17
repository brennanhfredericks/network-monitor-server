import pymysql
import os
import json
from connection import get_connection
from urllib import request, parse


def get_submitter_service_data():
    """
    - post process data that was stored locally by the submission service
    """
    base_path = "./test/data/submitter_service"
    data_files = os.listdir(base_path)

    for f in data_files:
        file_path = os.path.join(base_path, f)
        with open(file_path, "r") as fin:
            for line in fin:
                yield json.loads(line)


def count_packets_in_db():
    # connection to database

    conn = get_connection()

    with conn:

        with conn.cursor() as cursor:

            sql = "SELECT COUNT(id) FROM Packet"
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

    start_count = count_packets_in_db()
    url = "http://localhost:5050/packets"
    count_inserts = 0

    for packet in get_submitter_service_data():

        d = json.dumps(packet).encode("utf-8")

        req = request.Request(
            url, data=d, headers={"Content-Type": "Application/JSON"}, method="POST"
        )

        resp = request.urlopen(req)

        assert resp.getcode() == 200
        count_inserts += 1

    end_count = count_packets_in_db()

    assert end_count - start_count == count_inserts


def test_post_packets_flask_api_and_compare_db():

    post_packets_flask_api_and_compare_db()


if __name__ == "__main__":

    test_post_packets_flask_api_and_compare_db()
