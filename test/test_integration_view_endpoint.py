import os
import json
from urllib import request
import urllib

url_local = "http://localhost:5050"
url = "http://10.0.0.10:5050"


def packets_tables_all_view_points():
    params = urllib.urlencode({"protocolname": "packet", "limit": 0})
    req = request.Request(url + "packets/tables/view?" + params)
    resp = request.urlopen(req)

    assert resp.getcode() == 200


def test_packets_tables_all_view_points():
    # packets_tables_all_view_points()
    ...