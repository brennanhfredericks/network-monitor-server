from datetime import datetime
import functools
import json
from ..common import db
from flask import request, abort


class Packet_Protocol_Mapper(object):
    """ wrapper function to map dictionary keys to class instances """

    def __init__(self):

        self.__mapper = {}

    def _register(self, k, v):

        assert isinstance(k, str), "key has to be a str"
        assert issubclass(v, db.Model)

        self.__mapper[k] = v

    def get_instance(self, proto):
        return self.__mapper[proto]

    def protocols(self):
        return list(self.__mapper.keys())


packet_protocol_mapper = Packet_Protocol_Mapper()


class TimestampMixin(object):

    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, nullable=True, onupdate=datetime.utcnow)


class Unknown(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    identifier = db.Column(db.Integer, nullable=False)

    packet_id = db.Column(db.BigInteger, db.ForeignKey("packet.id"), nullable=False)

    packet = db.relationship(
        "Packet", lazy="select", backref=db.backref("unknown", lazy=True)
    )

    def __repr__(self):
        return f"<message {self.message}> <idemtifier {self.identifier}>"

    @classmethod
    def from_dict(cls, data, packet):

        return cls(
            message=data["message"],
            identifier=data["identifier"],
            packet=packet,
        )


packet_protocol_mapper._register(Unknown.__name__, Unknown)


class AF_Packet(db.Model):

    id = db.Column(db.BigInteger, primary_key=True)
    ifname = db.Column(db.String(50), nullable=False)
    proto = db.Column(db.Integer, nullable=False)
    pkttype = db.Column(db.String(25), nullable=False)
    hatype = db.Column(db.Integer, nullable=False)
    hwaddr = db.Column(db.String(50), nullable=False)
    packet_id = db.Column(db.BigInteger, db.ForeignKey("packet.id"), nullable=False)

    packet = db.relationship(
        "Packet", lazy="select", backref=db.backref("af_packet", lazy=True)
    )

    def __repr__(self):
        return f"<interface name {self.interfacename}> <protocol {self.protocol}> <packet type{self.packettype}>"

    @classmethod
    def from_dict(cls, data, packet):

        return cls(
            ifname=data["ifname"],
            proto=data["proto"],
            pkttype=data["pkttype"],
            hatype=data["hatype"],
            hwaddr=data["hwaddr"],
            packet=packet,
        )


packet_protocol_mapper._register(AF_Packet.__name__, AF_Packet)


class Packet_802_3(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    destination_MAC = db.Column(db.String(50), nullable=False)
    source_MAC = db.Column(db.String(50), nullable=False)
    ethertype = db.Column(db.Integer, nullable=False)

    packet_id = db.Column(db.BigInteger, db.ForeignKey("packet.id"), nullable=False)

    packet = db.relationship("Packet", backref=db.backref("packet_802_3", lazy=True))

    def __repr__(self):
        return f"<destination_MAC {self.destination_MAC}> <source_MAC {self.source_MAC}> <ethertype {self.ethertype}>"

    @classmethod
    def from_dict(cls, data, packet):
        return cls(
            destination_MAC=data["destination_MAC"],
            source_MAC=data["source_MAC"],
            ethertype=data["ethertype"],
            packet=packet,
        )


packet_protocol_mapper._register(Packet_802_3.__name__, Packet_802_3)


class Packet_802_2(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    DSAP = db.Column(db.String(50), nullable=False)
    SSAP = db.Column(db.String(50), nullable=False)
    control = db.Column(db.String(50), nullable=False)

    packet_id = db.Column(db.BigInteger, db.ForeignKey("packet.id"), nullable=False)

    packet = db.relationship("Packet", backref=db.backref("packet_802_2", lazy=True))

    def __repr__(self):
        return f"<DSAP {self.DSAP}> <SSAP {self.SSAP}> <control {self.control}>"

    @classmethod
    def from_dict(cls, data, packet):

        return cls(
            DSAP=data["DSAP"],
            SSAP=data["SSAP"],
            control=data["control"],
            packet=packet,
        )


packet_protocol_mapper._register(Packet_802_2.__name__, Packet_802_2)


class IPv4(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    version = db.Column(db.Integer, nullable=False)
    IHL = db.Column(db.Integer, nullable=False)
    DSCP = db.Column(db.Integer, nullable=False)
    ECN = db.Column(db.Integer, nullable=False)

    total_length = db.Column(db.Integer, nullable=False)
    identification = db.Column(db.BigInteger, nullable=False)
    flags = db.Column(db.Integer, nullable=False)
    fragment_offset = db.Column(db.Integer, nullable=False)
    TTL = db.Column(db.Integer, nullable=False)
    header_checksum = db.Column(db.Integer, nullable=False)
    source_address = db.Column(db.String(40), nullable=False)
    destination_address = db.Column(db.String(40), nullable=False)

    options = db.Column(db.Text, nullable=False)
    packet_id = db.Column(db.BigInteger, db.ForeignKey("packet.id"), nullable=False)
    packet = db.relationship("Packet", backref=db.backref("ipv4", lazy=True))

    def __repr__(self):
        return f"<source address {self.source_address}> <destination address {self.destination_address}>"

    @classmethod
    def from_dict(cls, data, packet):
        return cls(
            version=data["version"],
            IHL=data["IHL"],
            DSCP=data["DSCP"],
            ECN=data["ECN"],
            total_length=data["total_length"],
            identification=data["identification"],
            flags=data["flags"],
            fragment_offset=data["fragment_offset"],
            TTL=data["TTL"],
            header_checksum=data["header_checksum"],
            source_address=data["source_address"],
            destination_address=data["destination_address"],
            options=json.dumps(data["options"]),
            packet=packet,
        )


packet_protocol_mapper._register(IPv4.__name__, IPv4)


class IPv6(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    version = db.Column(db.Integer, nullable=False)
    DS = db.Column(db.Integer, nullable=False)
    ECN = db.Column(db.Integer, nullable=False)
    flow_label = db.Column(db.BigInteger, nullable=False)
    payload_length = db.Column(db.Integer, nullable=False)
    next_header = db.Column(db.Integer, nullable=False)
    hop_limit = db.Column(db.Integer, nullable=False)
    source_address = db.Column(db.String(70), nullable=False)
    destination_address = db.Column(db.String(70), nullable=False)
    ext_headers = db.Column(db.Text, nullable=False)

    packet_id = db.Column(db.BigInteger, db.ForeignKey("packet.id"), nullable=False)
    packet = db.relationship("Packet", backref=db.backref("ipv6", lazy=True))

    def __repr__(self):
        return f"<source address {self.source_address}> <destination address {self.destination_address}>"

    @classmethod
    def from_dict(cls, data, packet):
        return cls(
            version=data["version"],
            DS=data["DS"],
            ECN=data["ECN"],
            flow_label=data["flow_label"],
            payload_length=data["payload_length"],
            next_header=data["next_header"],
            hop_limit=data["hop_limit"],
            source_address=data["source_address"],
            destination_address=data["destination_address"],
            ext_headers=json.dumps(data["ext_headers"]),
            packet=packet,
        )


packet_protocol_mapper._register(IPv6.__name__, IPv6)


class ARP(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    HTYPE = db.Column(db.Integer, nullable=False)
    PTYPE = db.Column(db.Integer, nullable=False)
    HLEN = db.Column(db.Integer, nullable=False)
    PLEN = db.Column(db.Integer, nullable=False)
    operation = db.Column(db.Integer, nullable=False)
    SHA = db.Column(db.String(30), nullable=False)
    SPA = db.Column(db.String(30), nullable=False)
    THA = db.Column(db.String(30), nullable=False)
    TPA = db.Column(db.String(30), nullable=False)

    packet_id = db.Column(db.BigInteger, db.ForeignKey("packet.id"), nullable=False)
    packet = db.relationship("Packet", backref=db.backref("arp", lazy=True))

    def __repr__(self):
        return f"<HTYPE {self.HTYPE}> <PTYPE {self.PTYPE}>"

    @classmethod
    def from_dict(cls, data, packet):
        return cls(
            HTYPE=data["HTYPE"],
            PTYPE=data["PTYPE"],
            HLEN=data["HLEN"],
            PLEN=data["PLEN"],
            operation=data["operation"],
            SHA=data["SHA"],
            SPA=data["SPA"],
            THA=data["THA"],
            TPA=data["TPA"],
            packet=packet,
        )


packet_protocol_mapper._register(ARP.__name__, ARP)


class CDP(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    packet_id = db.Column(db.BigInteger, db.ForeignKey("packet.id"), nullable=False)
    packet = db.relationship("Packet", backref=db.backref("cdp", lazy=True))

    def __repr__(self):
        return f"<CDP>"

    @classmethod
    def from_dict(cls, data, packet):
        return cls(
            packet=packet,
        )


packet_protocol_mapper._register(CDP.__name__, CDP)


class LLDP(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    typelengthvalue = db.Column(db.Text, nullable=False)

    packet_id = db.Column(db.BigInteger, db.ForeignKey("packet.id"), nullable=False)
    packet = db.relationship("Packet", backref=db.backref("lldp", lazy=True))

    def __repr__(self):
        return f"<typelengthvalue >"

    @classmethod
    def from_dict(cls, data, packet):
        return cls(
            typelengthvalue=json.dumps(data["typelengthvalue"]),
            packet=packet,
        )


packet_protocol_mapper._register(LLDP.__name__, LLDP)


class IGMP(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    type_ = db.Column(db.Integer, nullable=False)
    max_resp_time = db.Column(db.Integer, nullable=False)
    checksum = db.Column(db.Integer, nullable=False)
    group_address = db.Column(db.String(40), nullable=False)

    packet_id = db.Column(db.BigInteger, db.ForeignKey("packet.id"), nullable=False)
    packet = db.relationship("Packet", backref=db.backref("igmp", lazy=True))

    def __repr__(self):
        return f"<type {self.type_}> <group address {self.group_address}>"

    @classmethod
    def from_dict(cls, data, packet):
        return cls(
            type_=data["type_"],
            max_resp_time=data["max_resp_time"],
            checksum=data["checksum"],
            group_address=data["group_address"],
            packet=packet,
        )


packet_protocol_mapper._register(IGMP.__name__, IGMP)


class ICMPv6(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    type_ = db.Column(db.Integer, nullable=False)
    code = db.Column(db.Integer, nullable=False)
    checksum = db.Column(db.Integer, nullable=False)
    message = db.Column(db.Text, nullable=False)

    packet_id = db.Column(db.BigInteger, db.ForeignKey("packet.id"), nullable=False)
    packet = db.relationship("Packet", backref=db.backref("icmpv6", lazy=True))

    def __repr__(self):
        return f"<type {self.type_}> <message {self.message}>"

    @classmethod
    def from_dict(cls, data, packet):
        return cls(
            type_=data["type_"],
            code=data["code"],
            checksum=data["checksum"],
            message=data["message"],
            packet=packet,
        )


packet_protocol_mapper._register(ICMPv6.__name__, ICMPv6)


class ICMP(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    type_ = db.Column(db.Integer, nullable=False)
    code = db.Column(db.Integer, nullable=False)
    checksum = db.Column(db.Integer, nullable=False)
    message = db.Column(db.Text, nullable=False)

    packet_id = db.Column(db.BigInteger, db.ForeignKey("packet.id"), nullable=False)
    packet = db.relationship("Packet", backref=db.backref("icmp", lazy=True))

    def __repr__(self):
        return f"<type {self.type_}> <message {self.message}>"

    @classmethod
    def from_dict(cls, data, packet):
        return cls(
            type_=data["type_"],
            code=data["code"],
            checksum=data["checksum"],
            message=data["message"],
            packet=packet,
        )


packet_protocol_mapper._register(ICMP.__name__, ICMP)


class TCP(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    source_port = db.Column(db.Integer, nullable=False)
    destination_port = db.Column(db.Integer, nullable=False)
    sequence_number = db.Column(db.BigInteger, nullable=False)
    acknowledgment_number = db.Column(db.BigInteger, nullable=False)
    data_offset = db.Column(db.Integer, nullable=False)
    reserved = db.Column(db.Integer, nullable=False)
    # issue
    flags = db.Column(db.Text, nullable=False)
    window_size = db.Column(db.Integer, nullable=False)
    checksum = db.Column(db.Integer, nullable=False)
    urgent_pointer = db.Column(db.Integer, nullable=False)
    # issue
    options = db.Column(db.Text, nullable=False)

    packet_id = db.Column(db.BigInteger, db.ForeignKey("packet.id"), nullable=False)
    packet = db.relationship("Packet", backref=db.backref("TCP", lazy=True))

    def __repr__(self):
        return f"<source port {self.source_port}> <destination port {self.destination_port}>"

    @classmethod
    def from_dict(cls, data, packet):
        return cls(
            source_port=data["source_port"],
            destination_port=data["destination_port"],
            sequence_number=data["sequence_number"],
            acknowledgment_number=data["acknowledgment_number"],
            data_offset=data["data_offset"],
            reserved=data["reserved"],
            flags=json.dumps(data["flags"]),
            window_size=data["window_size"],
            checksum=data["checksum"],
            urgent_pointer=data["urgent_pointer"],
            options=json.dumps(data["options"]),
            packet=packet,
        )


packet_protocol_mapper._register(TCP.__name__, TCP)


class UDP(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    source_port = db.Column(db.Integer, nullable=False)
    destination_port = db.Column(db.Integer, nullable=False)
    length = db.Column(db.Integer, nullable=False)
    checksum = db.Column(db.Integer, nullable=False)

    packet_id = db.Column(db.BigInteger, db.ForeignKey("packet.id"), nullable=False)
    packet = db.relationship("Packet", backref=db.backref("UDP", lazy=True))

    def __repr__(self):
        return f"<source port {self.source_port}> <destination port {self.destination_port}>"

    @classmethod
    def from_dict(cls, data, packet):

        return cls(
            source_port=data["source_port"],
            destination_port=data["destination_port"],
            length=data["length"],
            checksum=data["checksum"],
            packet=packet,
        )


packet_protocol_mapper._register(UDP.__name__, UDP)


class LSAP_one(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    packet_id = db.Column(db.BigInteger, db.ForeignKey("packet.id"), nullable=False)
    packet = db.relationship("Packet", backref=db.backref("LSAP_one", lazy=True))

    def __repr__(self):
        return f"<LSAP_one > <message {self.message}>"

    @classmethod
    def from_dict(cls, data, packet):

        return cls(
            message=data["message"],
            packet=packet,
        )


packet_protocol_mapper._register(LSAP_one.__name__, LSAP_one)


class SNAP_ext(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    OUI = db.Column(db.Integer, nullable=False)
    protocol_id = db.Column(db.Integer, nullable=False)
    packet_id = db.Column(db.BigInteger, db.ForeignKey("packet.id"), nullable=False)
    packet = db.relationship("Packet", backref=db.backref("SNAP_ext", lazy=True))

    def __repr__(self):
        return f"<OUI {self.OUI}> <protocol_id {self.protocol_id}>"

    @classmethod
    def from_dict(cls, data, packet):

        return cls(
            OUI=data["OUI"],
            protocol_id=data["protocol_id"],
            packet=packet,
        )


packet_protocol_mapper._register(SNAP_ext.__name__, SNAP_ext)


class Packet(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)

    def __repr__(self):
        return f"<id {self.id}>"


def validate_packet(func):
    @functools.wraps(func)
    def wrapper_validate_protocols(*args, **kwargs):
        data = request.get_json()

        for proto in data.keys():
            if proto not in packet_protocol_mapper.protocols():
                abort(400)

        result = func(*args, **kwargs)
        return result

    return wrapper_validate_protocols