import json
from flask import request, abort
from flask_restful import Resource, reqparse
from functools import lru_cache

from ..common import db
from ..models import validate_packet, Packet, packet_protocol_mapper


def add_new_packet():
    # create class instances of all the present keys
    data = data = request.get_json()

    packet = Packet()

    for proto_name, proto_attrs in data.items():

        # get class object
        cls_obj = packet_protocol_mapper.get_instance(proto_name)

        # call class method to create instance
        cls_obj.from_dict(proto_attrs, packet)

    # add packet database
    db.session.add(packet)
    db.session.commit()


class Packet_EP(Resource):
    def get(self):
        return "endpoint can be reached", 200

    @validate_packet
    def post(self):

        # insert into database
        add_new_packet()

        return 200


class Packet_Table_EP(Resource):
    def get(self):

        tables = db.engine.table_names()
        tables.remove("alembic_version")
        return {"protocols": tables}, 200


@lru_cache
def valid_protocol_names():
    valid_names = db.engine.table_names()
    valid_names.remove("alembic_version")

    return valid_names


class Packet_Table_Counts_EP(Resource):
    def get(self, protocol_name):
        protocol_name = protocol_name.lower()

        if protocol_name == "all":
            try:
                res = {
                    v: db.session.execute(
                        f"SELECT count(id) as entries from {v}"
                    ).scalar()
                    for v in valid_protocol_names()
                }
            except Exception:
                abort(status=400, message="Oops!")
            else:
                return res, 200
        elif protocol_name not in valid_protocol_names():
            abort(status=400, message="not a valid protocolname")

        res = db.session.execute(
            f"SELECT count(id) as entries from {protocol_name}"
        ).scalar()

        return {protocol_name: res}, 200


class Packet_Table_Views_EP(Resource):
    parser = reqparse.RequestParser()

    def __init__(self):
        super().__init__()
        self.parser.add_argument("protocolname", type=str, help="Specify protocol name")
        self.parser.add_argument(
            "limit", type=int, help="number of entries to return max (100)"
        )

    def get(self):
        args = self.parser.parse_args(strict=True)

        protoname = args.get("protocolname", None)
        limit = args.get("limit", None)

        if protoname is None or limit is None:
            abort(status=400, message="missing parameter values cannot be None")
        protoname = protoname.lower()
        limit = min(limit, 100)

        if protoname not in valid_protocol_names():
            abort(status=400, message="not a valid protocolname")

        # get object
        proto_obj = packet_protocol_mapper.get_instance(protoname)

        # query latest
        res = proto_obj.query.limit(limit).all()
        res = {"view": list(map(lambda x: x.to_dict(), res))}

        return json.dumps(res), 200
