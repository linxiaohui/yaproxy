# -*- coding: utf-8 -*-
"""
基于gevent的DNS服务器: 对配置的域名返回给定的IP，对没有配置的域名查询DNS服务器获得结果返回
"""

from gevent import socket
from gevent.server import DatagramServer

from DNSParser import DNSParser

def udp_send(address, data):
    sock = socket.socket(type=socket.SOCK_DGRAM)
    sock.connect(address)
    sock.send(data)
    response, address = sock.recvfrom(8192*4)
    return response, address

class DNSServerImpl(DatagramServer):
    def __init__(self, svr_name):
        self.special_hosts = []
        self.authority_dns = "114.114.114.114:53"
        super(DNSServerImpl, self).__init__(svr_name)

    def set_hosts(self, hosts, authority_dns="114.114.114.114"):
        self.special_hosts = hosts
        self.authority_dns = authority_dns

    def handle(self, data, address):
        query = DNSParser.parse_query(data)
        print("get dns query from %s,query:%s" % (str(address), str(query.qname)))
        find = False
        if query.qname in self.special_hosts:
            find = True
            ip = self.special_hosts[query.qname]
            print("Find a Hint: %s:%s" % (query.qname, ip))
        if find and query.qtype == "0x0001":
            # only handle A record
            print('domain:%s in hosts' % query.qname)
            response = DNSParser.generate_response(data, ip)
            self.socket.sendto(response, address)
        else:
            print('transfer for %s' % query.qname)
            response, serveraddress = udp_send(self.authority_dns, data)
            self.socket.sendto(response, address)


class DNSServer(object):
    def __init__(self, ip="0.0.0.0", port=53):
        self.DNS_SERVER = ("114.114.114.114", 53)
        self.listen_ip = ip
        self.listen_port = port
        self.special_hosts = {}

    def set_hosts(self, hosts):
        self.special_hosts.update(hosts)

    def add_host(self, domain_name, resolve_ip):
        self.hosts[domain_name] = resolve_ip

    def start(self):
        _server_name = f"{self.listen_ip}:{self.listen_port}"
        _server = DNSServerImpl(_server_name)
        _server.set_hosts(self.special_hosts, self.DNS_SERVER)
        _server.serve_forever()

if __name__ == "__main__":
    s = DNSServer("0.0.0.0", 53)
    s.set_hosts({b'abc': b'127.0.0.1'})
    s.start()
