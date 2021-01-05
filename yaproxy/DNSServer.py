# -*- coding: utf-8 -*-
"""
DNS服务器: 对配置的域名返回给定的IP，对没有配置的域名查询DNS服务器获得结果返回
"""
import socket
import socketserver

from DNSParser import DNSParser

class DNSHandler(socketserver.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)
        self.socket = self.request[1]

    def handle(self):
        data = self.request[0]
        self.socket = self.request[1]
        query = DNSParser.parse_query(data)
        address = self.client_address
        print("get dns query from %s,query:%s" % (str(address), str(query.qname)))
        find = False
        if query.qname in self.server.special_host:
            find = True
            ip = self.server.special_host[query.qname]
            print("Find a Hint: %s:%s" % (query.qname, ip))
        if find and query.qtype == "0x0001":
            # only handle A record
            print('domain:%s in hosts' % query.qname)
            response = DNSParser.generate_response(data, ip)
            self.socket.sendto(response, address)
        else:
            print('transfer for %s' % query.qname)
            sock = socket.socket(type=socket.SOCK_DGRAM)
            socket.setdefaulttimeout(5)
            sock.connect(("114.114.114.114", 53))
            sock.send(data)
            response, serveraddress = sock.recvfrom(8192*4)
            self.socket.sendto(response, address)


if __name__ == "__main__":
    HOST = "0.0.0.0"
    PORT = 53
    dns_server = None
    try:
        dns_server = socketserver.ForkingUDPServer((HOST, PORT), DNSHandler)
    except Exception as ex:
        print(ex)
        dns_server = socketserver.ThreadingUDPServer((HOST, PORT), DNSHandler)
    dns_server.special_host = []
    dns_server.serve_forever()
