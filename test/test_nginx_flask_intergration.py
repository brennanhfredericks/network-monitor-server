# test flask submission end point reachable
import json
from urllib import request, parse
from load_data import get_submitter_service_data

url = "http://localhost:5050/packets"


def packets_tables_names_endpoint():
    req = request.Request(url + "/tables")

    resp = request.urlopen(req)

    assert resp.getcode() == 200


def packets_table_count_endpoint():
    req = request.Request(url + "/tables")

    resp = request.urlopen(req)

    assert resp.getcode() == 200

    data = json.load(resp)

    for v in data["protocols"]:
        req = request.Request(url + f"/tables/{v}")
        resp = request.urlopen(req)

        assert resp.getcode() == 200


def packets_all_table_counts_endpoint():
    req = request.Request(url + "/tables/all")

    resp = request.urlopen(req)

    assert resp.getcode() == 200


def packets_post_endpoint():

    # specifying content type is important
    for pkt in get_submitter_service_data():
        data = json.dumps(pkt).encode()

        req = request.Request(
            url, data=data, headers={"content-type": "application/json"}
        )

        resp = request.urlopen(req)

        assert resp.getcode() == 200


def packets_get_endpoint():

    req = request.Request(url)

    resp = request.urlopen(req)

    assert resp.getcode() == 200


def test_packets_post_endpoint():

    packets_post_endpoint()


def test_packets_get_endpoint():
    packets_get_endpoint()


def test_packets_tables_names_endpoint():
    packets_tables_names_endpoint()


def test_packets_all_table_counts_endpoint():
    packets_all_table_counts_endpoint()


def test_packets_table_count_endpoint():
    packets_table_count_endpoint()