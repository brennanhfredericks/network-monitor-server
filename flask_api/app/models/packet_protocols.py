from datetime import datetime
import functools
import json
from ..common import db
from flask_restful import fields, marshal
from flask import request, abort


class Packet_Protocol_Mapper(object):
    """wrapper function to map dictionary keys to class instances"""

    def __init__(self):

        # info key added here for validation purpose. the info data is extracted and added to Packet Model
        self.__mapper = {"info": None}

    def _register(self, k, v):

        assert isinstance(k, str), "key has to be a str"
        assert issubclass(v, db.Model)

        self.__mapper[k.lower()] = v

    def get_instance(self, proto):
        return self.__mapper[proto.lower()]

    def protocols(self):
        return list(self.__mapper.keys())


packet_protocol_mapper = Packet_Protocol_Mapper()


class TimestampMixin(object):

    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, nullable=True, onupdate=datetime.utcnow)


class Unknown(db.Model):
    __tablename__ = "Unknown"
    id = db.Column(db.BigInteger, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    identifier = db.Column(db.Integer, nullable=False)

    packet_id = db.Column(db.BigInteger, db.ForeignKey("Packet.id"), nullable=False)

    packet = db.relationship(
        "Packet", lazy="select", backref=db.backref("unknown", lazy=True)
    )

    def __init__(self):
        self._resource_fields = {
            "id": fields.Integer,
            "message": fields.String,
            "identifier": fields.Integer,
        }
        super().__init__()

    def __repr__(self):
        return f"<message {self.message}> <idemtifier {self.identifier}>"

    def to_dict(self):
        return marshal(
            {"id": self.id, "message": self.message, "identifier": self.identifier},
            self._resource_fields,
        )

    @classmethod
    def from_dict(cls, data, packet):

        return cls(
            message=data["message"],
            identifier=data["identifier"],
            packet=packet,
        )


packet_protocol_mapper._register(Unknown.__name__, Unknown)


class AF_Packet(db.Model):
    __tablename__ = "AF_Packet"
    id = db.Column(db.BigInteger, primary_key=True)
    interface_name = db.Column(db.String(50), nullable=False)
    ethernet_protocol_number = db.Column(db.Integer, nullable=False)
    packet_type = db.Column(db.String(25), nullable=False)
    arp_hardware_address_type = db.Column(db.Integer, nullable=False)
    hardware_physical_address = db.Column(db.String(50), nullable=False)
    packet_id = db.Column(db.BigInteger, db.ForeignKey("Packet.id"), nullable=False)

    packet = db.relationship(
        "Packet", lazy="select", backref=db.backref("af_packet", lazy=True)
    )

    _resource_fields = {
        "id": fields.Integer,
        "interface_name": fields.String,
        "ethernet_protocol_number": fields.Integer,
        "packet_type": fields.String,
        "arp_hardware_address_type": fields.Integer,
        "hardware_physical_address": fields.String,
    }

    def __repr__(self):
        return f"<interface name {self.interface_name}> <ethernet protocol number {self.ethernet_protocol_number}> <packet type{self.packet_type}>"

    def to_dict(self):

        return marshal(
            {
                "id": self.id,
                "interface_name": self.interface_name,
                "ethernet_protocol_number": self.ethernet_protocol_number,
                "packet_type": self.packet_type,
                "arp_hardware_address_type": self.arp_hardware_address_type,
                "hardware_physical_address": self.hardware_physical_address,
            },
            self._resource_fields,
        )

    @classmethod
    def from_dict(cls, data, packet):

        return cls(
            interface_name=data["Interface_Name"],
            ethernet_protocol_number=data["Ethernet_Protocol_Number"],
            packet_type=data["Packet_Type"],
            arp_hardware_address_type=data["Arp_Hardware_Address_Type"],
            hardware_physical_address=data["Hardware_Physical_Address"],
            packet=packet,
        )


packet_protocol_mapper._register(AF_Packet.__name__, AF_Packet)


class Packet_802_3(db.Model):
    __tablename__ = "Packet_802_3"
    id = db.Column(db.BigInteger, primary_key=True)
    destination_mac = db.Column(db.String(50), nullable=False)
    source_mac = db.Column(db.String(50), nullable=False)
    ethertype = db.Column(db.Integer, nullable=False)

    packet_id = db.Column(db.BigInteger, db.ForeignKey("Packet.id"), nullable=False)

    packet = db.relationship("Packet", backref=db.backref("packet_802_3", lazy=True))

    _resource_fields = {
        "id": fields.Integer,
        "destination_mac": fields.String,
        "source_mac": fields.String,
        "ethertype": fields.Integer,
    }

    def __repr__(self):
        return f"<destination mac {self.destination_mac}> <source mac {self.source_mac}> <ethertype {self.ethertype}>"

    def to_dict(self):
        return marshal(
            {
                "id": self.id,
                "destination_mac": self.destination_mac,
                "source_mac": self.source_mac,
                "ethertype": self.ethertype,
            },
            self._resource_fields,
        )

    @classmethod
    def from_dict(cls, data, packet):
        return cls(
            destination_mac=data["Destination_MAC"],
            source_mac=data["Source_MAC"],
            ethertype=data["Ethertype"],
            packet=packet,
        )


packet_protocol_mapper._register(Packet_802_3.__name__, Packet_802_3)


class Packet_802_2(db.Model):
    __tablename__ = "Packet_802_2"
    id = db.Column(db.BigInteger, primary_key=True)
    dsap = db.Column(db.String(50), nullable=False)
    ssap = db.Column(db.String(50), nullable=False)
    control = db.Column(db.String(50), nullable=False)

    packet_id = db.Column(db.BigInteger, db.ForeignKey("Packet.id"), nullable=False)

    packet = db.relationship("Packet", backref=db.backref("packet_802_2", lazy=True))

    _resource_fields = {
        "id": fields.Integer,
        "dsap": fields.String,
        "ssap": fields.String,
        "control": fields.String,
    }

    def __repr__(self):
        return f"<dsap {self.dsap}> <SSAP {self.ssap}> <control {self.control}>"

    def to_dict(self):
        return marshal(
            {
                "id": self.id,
                "dsap": self.dsap,
                "ssap": self.ssap,
                "control": self.control,
            },
            self._resource_fields,
        )

    @classmethod
    def from_dict(cls, data, packet):

        return cls(
            dsap=data["DSAP"],
            ssap=data["SSAP"],
            control=data["Control"],
            packet=packet,
        )


packet_protocol_mapper._register(Packet_802_2.__name__, Packet_802_2)


class IPv4(db.Model):
    __tablename__ = "IPv4"
    id = db.Column(db.BigInteger, primary_key=True)
    version = db.Column(db.Integer, nullable=False)
    ihl = db.Column(db.Integer, nullable=False)
    dscp = db.Column(db.Integer, nullable=False)
    ecn = db.Column(db.Integer, nullable=False)

    total_length = db.Column(db.Integer, nullable=False)
    identification = db.Column(db.BigInteger, nullable=False)
    flags = db.Column(db.Integer, nullable=False)
    fragment_offset = db.Column(db.Integer, nullable=False)
    ttl = db.Column(db.Integer, nullable=False)
    header_checksum = db.Column(db.Integer, nullable=False)
    source_address = db.Column(db.String(40), nullable=False)
    destination_address = db.Column(db.String(40), nullable=False)

    options = db.Column(db.Text, nullable=False)
    packet_id = db.Column(db.BigInteger, db.ForeignKey("Packet.id"), nullable=False)
    packet = db.relationship("Packet", backref=db.backref("ipv4", lazy=True))

    _resource_fields = {
        "id": fields.Integer,
        "version": fields.Integer,
        "IHL": fields.Integer,
        "dscp": fields.Integer,
        "ECN": fields.Integer,
        "total_length": fields.Integer,
        "identification": fields.Integer,
        "flags": fields.Integer,
        "fragment_offset": fields.Integer,
        "ttl": fields.Integer,
        "header_checksum": fields.Integer,
        "source_address": fields.String,
        "destination_address": fields.String,
        "options": fields.String,
    }

    def __repr__(self):
        return f"<source address {self.source_address}> <destination address {self.destination_address}>"

    def to_dict(self):
        return marshal(
            {
                "id": self.id,
                "version": self.version,
                "ihl": self.ihl,
                "dscp": self.dscp,
                "ecn": self.ecn,
                "total_length": self.total_length,
                "identification": self.identification,
                "flags": self.flags,
                "fragment_offset": self.fragment_offset,
                "ttl": self.ttl,
                "header_checksum": self.header_checksum,
                "source_address": self.source_address,
                "destination_address": self.destination_address,
                "options": self.options,
            },
            self._resource_fields,
        )

    @classmethod
    def from_dict(cls, data, packet):
        return cls(
            version=data["Version"],
            ihl=data["IHL"],
            dscp=data["DSCP"],
            ecn=data["ECN"],
            total_length=data["Total_Length"],
            identification=data["Identification"],
            flags=data["Flags"],
            fragment_offset=data["Fragment_Offset"],
            ttl=data["TTL"],
            header_checksum=data["Header_Checksum"],
            source_address=data["Source_Address"],
            destination_address=data["Destination_Address"],
            options=json.dumps(data["Options"]),
            packet=packet,
        )


packet_protocol_mapper._register(IPv4.__name__, IPv4)


class IPv6(db.Model):
    __tablename__ = "IPv6"
    id = db.Column(db.BigInteger, primary_key=True)
    version = db.Column(db.Integer, nullable=False)
    ds = db.Column(db.Integer, nullable=False)
    ecn = db.Column(db.Integer, nullable=False)
    flow_label = db.Column(db.BigInteger, nullable=False)
    payload_length = db.Column(db.Integer, nullable=False)
    next_header = db.Column(db.Integer, nullable=False)
    hop_limit = db.Column(db.Integer, nullable=False)
    source_address = db.Column(db.String(70), nullable=False)
    destination_address = db.Column(db.String(70), nullable=False)
    ext_headers = db.Column(db.Text, nullable=False)

    packet_id = db.Column(db.BigInteger, db.ForeignKey("Packet.id"), nullable=False)
    packet = db.relationship("Packet", backref=db.backref("ipv6", lazy=True))

    _resource_fields = {
        "id": fields.Integer,
        "version": fields.Integer,
        "ds": fields.Integer,
        "ecn": fields.Integer,
        "flow_label": fields.Integer,
        "payload_length": fields.Integer,
        "next_header": fields.Integer,
        "hop_limit": fields.Integer,
        "source_address": fields.String,
        "destination_address": fields.String,
        "ext_headers": fields.String,
    }

    def __repr__(self):
        return f"<source address {self.source_address}> <destination address {self.destination_address}>"

    def to_dict(self):
        return marshal(
            {
                "id": self.id,
                "version": self.version,
                "ds": self.ds,
                "ecn": self.ecn,
                "flow_label": self.flow_label,
                "payload_length": self.payload_length,
                "next_header": self.next_header,
                "hop_limit": self.hop_limit,
                "source_address": self.source_address,
                "destination_address": self.destination_address,
                "ext_headers": self.ext_headers,
            },
            self._resource_fields,
        )

    @classmethod
    def from_dict(cls, data, packet):
        return cls(
            version=data["Version"],
            ds=data["DS"],
            ecn=data["ECN"],
            flow_label=data["Flow_Label"],
            payload_length=data["Payload_Length"],
            next_header=data["Next_Header"],
            hop_limit=data["Hop_Limit"],
            source_address=data["Source_Address"],
            destination_address=data["Destination_Address"],
            ext_headers=json.dumps(data["Ext_Headers"]),
            packet=packet,
        )


packet_protocol_mapper._register(IPv6.__name__, IPv6)


class ARP(db.Model):
    __tablename__ = "ARP"
    id = db.Column(db.BigInteger, primary_key=True)
    htype = db.Column(db.Integer, nullable=False)
    ptype = db.Column(db.Integer, nullable=False)
    hlen = db.Column(db.Integer, nullable=False)
    plen = db.Column(db.Integer, nullable=False)
    operation = db.Column(db.Integer, nullable=False)
    sha = db.Column(db.String(30), nullable=False)
    spa = db.Column(db.String(30), nullable=False)
    tha = db.Column(db.String(30), nullable=False)
    tpa = db.Column(db.String(30), nullable=False)

    packet_id = db.Column(db.BigInteger, db.ForeignKey("Packet.id"), nullable=False)
    packet = db.relationship("Packet", backref=db.backref("arp", lazy=True))

    _resource_fields = {
        "id": fields.Integer,
        "htype": fields.Integer,
        "ptype": fields.Integer,
        "hlen": fields.Integer,
        "plen": fields.Integer,
        "operation": fields.Integer,
        "sha": fields.String,
        "spa": fields.String,
        "tha": fields.String,
        "tpa": fields.String,
    }

    def __repr__(self):
        return f"<htype {self.htype}> <PTYPE {self.PTYPE}>"

    def to_dict(self):
        return marshal(
            {
                "id": self.id,
                "htype": self.htype,
                "ptype": self.ptype,
                "hlen": self.hlen,
                "plen": self.plen,
                "operation": self.operation,
                "sha": self.sha,
                "spa": self.spa,
                "tha": self.tha,
                "tpa": self.tpa,
            },
            self._resource_fields,
        )

    @classmethod
    def from_dict(cls, data, packet):
        return cls(
            htype=data["HTYPE"],
            ptype=data["PTYPE"],
            hlen=data["HLEN"],
            plen=data["PLEN"],
            operation=data["Operation"],
            sha=data["SHA"],
            spa=data["SPA"],
            tha=data["THA"],
            tpa=data["TPA"],
            packet=packet,
        )


packet_protocol_mapper._register(ARP.__name__, ARP)


class CDP(db.Model):
    __tablename__ = "CDP"
    id = db.Column(db.BigInteger, primary_key=True)
    packet_id = db.Column(db.BigInteger, db.ForeignKey("Packet.id"), nullable=False)
    packet = db.relationship("Packet", backref=db.backref("cdp", lazy=True))

    _resource_fields = {
        "id": fields.Integer,
    }

    def __repr__(self):
        return f"<CDP>"

    def to_dict(self):
        return marshal(
            {
                "id": self.id,
            },
            self._resource_fields,
        )

    @classmethod
    def from_dict(cls, _, packet):
        return cls(
            packet=packet,
        )


packet_protocol_mapper._register(CDP.__name__, CDP)


class LLDP(db.Model):
    __tablename__ = "LLDP"
    id = db.Column(db.BigInteger, primary_key=True)
    tlv = db.Column(db.Text, nullable=False)

    packet_id = db.Column(db.BigInteger, db.ForeignKey("Packet.id"), nullable=False)
    packet = db.relationship("Packet", backref=db.backref("lldp", lazy=True))

    _resource_fields = {
        "id": fields.Integer,
        "tlv": fields.String,
    }

    def __repr__(self):
        return f"<tlv {self.tlv}>"

    def to_dict(self):
        return marshal(
            {
                "id": self.id,
                "tlv": self.tlv,
            },
            self._resource_fields,
        )

    @classmethod
    def from_dict(cls, data, packet):
        return cls(
            tlv=json.dumps(data["TLV"]),
            packet=packet,
        )


packet_protocol_mapper._register(LLDP.__name__, LLDP)


class IGMP(db.Model):
    __tablename__ = "IGMP"
    id = db.Column(db.BigInteger, primary_key=True)
    type = db.Column(db.Integer, nullable=False)
    max_response_time = db.Column(db.Integer, nullable=False)
    checksum = db.Column(db.Integer, nullable=False)
    group_address = db.Column(db.String(40), nullable=False)

    packet_id = db.Column(db.BigInteger, db.ForeignKey("Packet.id"), nullable=False)
    packet = db.relationship("Packet", backref=db.backref("igmp", lazy=True))

    _resource_fields = {
        "id": fields.Integer,
        "type": fields.Integer,
        "max_response_time": fields.Integer,
        "checksum": fields.Integer,
        "group_address": fields.String,
    }

    def __repr__(self):
        return f"<type {self.type}> <group address {self.group_address}>"

    def to_dict(self):
        return marshal(
            {
                "id": self.id,
                "type": self.type,
                "max_response_time": self.max_response_time,
                "checksum": self.checksum,
                "group_address": self.group_address,
            },
            self._resource_fields,
        )

    @classmethod
    def from_dict(cls, data, packet):
        return cls(
            type=data["Type"],
            max_response_time=data["Max_Response_Time"],
            checksum=data["Checksum"],
            group_address=data["Group_Address"],
            packet=packet,
        )


packet_protocol_mapper._register(IGMP.__name__, IGMP)


class ICMPv6(db.Model):
    __tablename__ = "ICMPv6"
    id = db.Column(db.BigInteger, primary_key=True)
    type = db.Column(db.Integer, nullable=False)
    code = db.Column(db.Integer, nullable=False)
    checksum = db.Column(db.Integer, nullable=False)
    message = db.Column(db.Text, nullable=False)

    packet_id = db.Column(db.BigInteger, db.ForeignKey("Packet.id"), nullable=False)
    packet = db.relationship("Packet", backref=db.backref("icmpv6", lazy=True))

    _resource_fields = {
        "id": fields.Integer,
        "type": fields.Integer,
        "code": fields.Integer,
        "checksum": fields.Integer,
        "message": fields.String,
    }

    def __repr__(self):
        return f"<type {self.type}> <message {self.message}>"

    def to_dict(self):
        return marshal(
            {
                "id": self.id,
                "type": self.type,
                "code": self.code,
                "checksum": self.checksum,
                "message": self.message,
            },
            self._resource_fields,
        )

    @classmethod
    def from_dict(cls, data, packet):
        return cls(
            type=data["Type"],
            code=data["Code"],
            checksum=data["Checksum"],
            message=data["Message"],
            packet=packet,
        )


packet_protocol_mapper._register(ICMPv6.__name__, ICMPv6)


class ICMP(db.Model):
    __tablename__ = "ICMP"
    id = db.Column(db.BigInteger, primary_key=True)
    type = db.Column(db.Integer, nullable=False)
    code = db.Column(db.Integer, nullable=False)
    checksum = db.Column(db.Integer, nullable=False)
    message = db.Column(db.Text, nullable=False)

    packet_id = db.Column(db.BigInteger, db.ForeignKey("Packet.id"), nullable=False)
    packet = db.relationship("Packet", backref=db.backref("icmp", lazy=True))

    _resource_fields = {
        "id": fields.Integer,
        "type": fields.Integer,
        "code": fields.Integer,
        "checksum": fields.Integer,
        "message": fields.String,
    }

    def __repr__(self):
        return f"<type {self.type}> <message {self.message}>"

    def to_dict(self):
        return marshal(
            {
                "id": self.id,
                "type": self.type,
                "code": self.code,
                "checksum": self.checksum,
                "message": self.message,
            },
            self._resource_fields,
        )

    @classmethod
    def from_dict(cls, data, packet):
        return cls(
            type=data["Type"],
            code=data["Code"],
            checksum=data["Checksum"],
            message=data["Message"],
            packet=packet,
        )


packet_protocol_mapper._register(ICMP.__name__, ICMP)


class TCP(db.Model):
    __tablename__ = "TCP"
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

    packet_id = db.Column(db.BigInteger, db.ForeignKey("Packet.id"), nullable=False)
    packet = db.relationship("Packet", backref=db.backref("tcp", lazy=True))

    _resource_fields = {
        "id": fields.Integer,
        "source_port": fields.Integer,
        "destination_port": fields.Integer,
        "sequence_number": fields.Integer,
        "acknowledgment_number": fields.Integer,
        "data_offset": fields.Integer,
        "reserved": fields.Integer,
        "flags": fields.String,
        "window_size": fields.Integer,
        "checksum": fields.Integer,
        "urgent_pointer": fields.Integer,
        "options": fields.String,
    }

    def __repr__(self):
        return f"<source port {self.source_port}> <destination port {self.destination_port}>"

    def to_dict(self):
        return marshal(
            {
                "id": self.id,
                "source_port": self.source_port,
                "destination_port": self.destination_port,
                "sequence_number": self.sequence_number,
                "acknowledgment_number": self.acknowledgment_number,
                "data_offset": self.data_offset,
                "reserved": self.reserved,
                "flags": self.flags,
                "window_size": self.window_size,
                "checksum": self.checksum,
                "urgent_pointer": self.urgent_pointer,
                "options": self.options,
            },
            self._resource_fields,
        )

    @classmethod
    def from_dict(cls, data, packet):
        return cls(
            source_port=data["Source_Port"],
            destination_port=data["Destination_Port"],
            sequence_number=data["Sequence_Number"],
            acknowledgment_number=data["Acknowledgment_Number"],
            data_offset=data["Data_Offset"],
            reserved=data["Reserved"],
            flags=json.dumps(data["Flags"]),
            window_size=data["Window_Size"],
            checksum=data["Checksum"],
            urgent_pointer=data["Urgent_Pointer"],
            options=json.dumps(data["Options"]),
            packet=packet,
        )


packet_protocol_mapper._register(TCP.__name__, TCP)


class UDP(db.Model):
    __tablename__ = "UDP"
    id = db.Column(db.BigInteger, primary_key=True)
    source_port = db.Column(db.Integer, nullable=False)
    destination_port = db.Column(db.Integer, nullable=False)
    length = db.Column(db.Integer, nullable=False)
    checksum = db.Column(db.Integer, nullable=False)

    packet_id = db.Column(db.BigInteger, db.ForeignKey("Packet.id"), nullable=False)
    packet = db.relationship("Packet", backref=db.backref("udp", lazy=True))

    _resource_fields = {
        "id": fields.Integer,
        "source_port": fields.Integer,
        "destination_port": fields.Integer,
        "legnth": fields.Integer,
        "checksum": fields.Integer,
    }

    def __repr__(self):
        return f"<source port {self.source_port}> <destination port {self.destination_port}>"

    def to_dict(self):
        return marshal(
            {
                "id": self.id,
                "source_port": self.source_port,
                "destination_port": self.destination_port,
                "legnth": self.length,
                "checksum": self.checksum,
            },
            self._resource_fields,
        )

    @classmethod
    def from_dict(cls, data, packet):

        return cls(
            source_port=data["Source_Port"],
            destination_port=data["Destination_Port"],
            length=data["Length"],
            checksum=data["Checksum"],
            packet=packet,
        )


packet_protocol_mapper._register(UDP.__name__, UDP)


class LSAP_One(db.Model):
    __tablename__ = "LSAP_One"
    id = db.Column(db.BigInteger, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    packet_id = db.Column(db.BigInteger, db.ForeignKey("Packet.id"), nullable=False)
    packet = db.relationship("Packet", backref=db.backref("lsap_one", lazy=True))

    _resource_fields = {
        "id": fields.Integer,
        "message": fields.String,
    }

    def __repr__(self):
        return f"<LSAP_one > <message {self.message}>"

    def to_dict(self):
        return marshal(
            {
                "id": self.id,
                "message": self.message,
            },
            self._resource_fields,
        )

    @classmethod
    def from_dict(cls, data, packet):

        return cls(
            message=data["Message"],
            packet=packet,
        )


packet_protocol_mapper._register(LSAP_One.__name__, LSAP_One)


class SNAP_Ext(db.Model):
    __tablename__ = "SNAP_Ext"
    id = db.Column(db.BigInteger, primary_key=True)
    oui = db.Column(db.Integer, nullable=False)
    protocol_id = db.Column(db.Integer, nullable=False)
    packet_id = db.Column(db.BigInteger, db.ForeignKey("Packet.id"), nullable=False)
    packet = db.relationship("Packet", backref=db.backref("snap_ext", lazy=True))

    _resource_fields = {
        "id": fields.Integer,
        "oui": fields.Integer,
        "protocol_id": fields.Integer,
    }

    def __repr__(self):
        return f"<oui {self.oui}> <protocol_id {self.protocol_id}>"

    def to_dict(self):
        return marshal(
            {
                "id": self.id,
                "oui": self.oui,
                "protocol_id": self.protocol_id,
            },
            self._resource_fields,
        )

    @classmethod
    def from_dict(cls, data, packet):

        return cls(
            oui=data["OUI"],
            protocol_id=data["Protocol_ID"],
            packet=packet,
        )


packet_protocol_mapper._register(SNAP_Ext.__name__, SNAP_Ext)


class Packet(db.Model):
    __tablename__ = "Packet"
    id = db.Column(db.BigInteger, primary_key=True)
    sniffed_timestamp = db.Column(db.Float, nullable=False)
    processed_timestamp = db.Column(db.Float, nullable=False)
    submitter_timestamp = db.Column(db.Float, nullable=False)
    _resource_fields = {
        "id": fields.Integer,
    }

    # add time info

    def to_dict(self):
        return marshal(
            {
                "id": self.id,
            },
            self._resource_fields,
        )

    def __repr__(self):
        return f"<id {self.id}>"

    @classmethod
    def from_dict(cls, data):

        return cls(
            sniffed_timestamp=data["Sniffed_Timestamp"],
            processed_timestamp=data["Processed_Timestamp"],
            submitter_timestamp=data["Submitter_Timestamp"],
        )


packet_protocol_mapper._register(Packet.__name__, Packet)


def validate_packet(func):
    @functools.wraps(func)
    def wrapper_validate_protocols(*args, **kwargs):
        data = request.get_json()

        if not isinstance(data, dict):
            abort(status=400)
        for proto in data.keys():

            # the records are lower cased
            if proto.lower() not in packet_protocol_mapper.protocols():
                abort(status=400)

        result = func(*args, **kwargs)
        return result

    return wrapper_validate_protocols
