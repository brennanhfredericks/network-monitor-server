import json
from flask import request, abort
from flask_restful import Resource

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


class Packet_Table_Counts_EP(Resource):
    def get(self, protocol_name):
        protocol_name = protocol_name.lower()
        valid_names = db.engine.table_names()
        valid_names.remove("alembic_version")

        if protocol_name == "all":
            try:
                res = {
                    v: db.session.execute(
                        f"SELECT count(id) as entries from {v}"
                    ).scalar()
                    for v in valid_names
                }
            except Exception:
                abort(400)
            else:
                return res, 200
        elif protocol_name not in valid_names:
            abort(400)

        res = db.session.execute(
            f"SELECT count(id) as entries from {protocol_name}"
        ).scalar()

        return {protocol_name: res}, 200
