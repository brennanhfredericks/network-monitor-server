# test flask submission end point reachable
import json
from urllib import request, parse

url = "http://localhost:5050/packets"
pkt = {
    "Packet_802_3": {
        "destination_MAC": "00:15:5D:BE:8B:9E",
        "source_MAC": "00:15:5D:F5:73:AA",
        "ethertype": 2048,
    },
    "IPv4": {
        "version": 4,
        "IHL": 5,
        "DSCP": 0,
        "ECN": 0,
        "total_length": 46,
        "identification": 56751,
        "flags": 0,
        "fragment_offset": 0,
        "TTL": 64,
        "protocol": 6,
        "header_checksum": 8103,
        "source_address": "172.20.117.73",
        "destination_address": "172.20.112.1",
        "options": {},
    },
    "TCP": {
        "source_port": 46099,
        "destination_port": 60216,
        "sequence_number": 3907046702,
        "acknowledgment_number": 1131209977,
        "data_offset": 5,
        "reserved": 0,
        "flags": 80,
        "window_size": 8763,
        "checksum": 15764,
        "urgent_pointer": 0,
        "options": {},
    },
    "AF_Packet": {
        "ifname": "eth0",
        "proto": 2048,
        "pkttype": "PACKET_OUTGOING",
        "hatype": 1,
        "hwaddr": "00:15:5D:F5:73:AA",
    },
}


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

    d = json.dumps(pkt).encode("utf-8")
    req = request.Request(
        url, data=d, headers={"Content-Type": "Application/JSON"}, method="POST"
    )

    resp = request.urlopen(req)

    assert resp.getcode() == 200


def packets_get_endpoint():

    d = json.dumps(pkt).encode("utf-8")
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