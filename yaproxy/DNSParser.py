# -*- coding: utf-8 -*-
"""
DNS协议解析
"""

import io
import struct
from collections import namedtuple

QueryResult = namedtuple("DnsQuery",
                         "transaction_id,flags,questions,answer_rrs,authority_rrs,additional_rrs,qname,qtype,qclass"
                         )

def _hex(x: int) -> str:
    return '0x{0:04x}'.format(x)

class DNSParser(object):
    """参考 DNS协议报文格式"""
    @classmethod
    def parse_query(cls, query):
        # ! network (= big-endian)
        # H unsigned short
        transaction_id, flags, questions, answer_rrs, authority_rrs, additional_rrs = map(
            _hex, struct.unpack("!6H", query[:12]))
        queries = io.BytesIO(query[12:])
        c = struct.unpack("!c", queries.read(1))[0]
        domain = []
        while c != b'\x00':
            n = ord(c)
            domain.append(b''.join(struct.unpack("!%sc" % n, queries.read(ord(c)))))
            c = struct.unpack("!c", queries.read(1))[0]
        domain = b'.'.join(domain)
        qtype, qclass = map(_hex, struct.unpack("!2H", queries.read()))
        return QueryResult(transaction_id, flags, questions, answer_rrs,
                           authority_rrs, additional_rrs, domain, qtype, qclass)

    @classmethod
    def generate_response(cls, query_data, ip):
        """only support ipv4"""
        return b''.join([query_data[:2], b"\x81\x80\x00\x01\x00\x02\x00\x00\x00\x00",
                         query_data[12:], b"\xc0\x0c", b"\x00\x01", b"\x00\x01", b"\x00\x00\x00\x1e", b"\x00\x04",
                         struct.pack('BBBB', *map(int, ip.split(b'.')))
                         ])

