import os
import json
from urllib import request, parse


url_local = "http://localhost:5050/"


def packets_tables_all_view_points():

    req = request.Request(
        "http://localhost:5050/packets/tables/views?protocolname=ipv4&limit=10",
        data=None,
        headers={
            "User-Agent": "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"
        },
    )

    resp = request.urlopen(req)
    assert resp.getcode() == 200


def test_packets_tables_all_view_points():
    packets_tables_all_view_points()


if __name__ == "__main__":

    test_packets_tables_all_view_points()