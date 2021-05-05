import os
import json
from urllib import request, parse


url_local = "http://localhost:5050"


def packets_tables_all_view_points():
    limits = [-50, 5, 10, 25, 30, 100, 500]
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"
    }
    # tables

    req_o = request.Request(f"{url_local}/packets/tables")
    resp_o = request.urlopen(req_o)

    protonames = json.load(resp_o)["protocols"]

    assert resp_o.getcode() == 200

    for proto in protonames:
        for limit in limits:
            print(proto)
            req = request.Request(
                f"{url_local}/packets/tables/views?protocolname={proto}&limit={limit}",
                data=None,
                headers=headers,
            )

            resp = request.urlopen(req)

            assert resp.getcode() == 200

            records = json.load(resp)["view"]
            print(len(records), limit)
            # print(type(records), limit)
            if len(records) == 0:
                continue
            if limit < 0 or limit > 100:
                assert len(records) != limit
            else:
                if len(records) < limit:
                    continue
                assert len(records) == limit


def test_packets_tables_all_view_points():
    packets_tables_all_view_points()


if __name__ == "__main__":

    test_packets_tables_all_view_points()