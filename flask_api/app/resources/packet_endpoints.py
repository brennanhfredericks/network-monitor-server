from flask import request
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
