# -*- coding: utf-8 -*-
"""
DNS服务器: 对配置的域名返回给定的IP，对没有配置的域名查询DNS服务器获得结果返回
使用partial创建Handler，传递参数
"""
import socket
import socketserver
from functools import partial

from DNSParser import DNSParser

class DNSHandlerV2(socketserver.BaseRequestHandler):
    def __init__(self, speical_hosts, real_dns_server, request, client_address, server):
        print("speical_hosts", speical_hosts)
        
        self.socket = None
        self.specaial_hosts = speical_hosts
        self.real_dns_server = real_dns_server
        print("Init OK")
        super(DNSHandlerV2, self).__init__(request, client_address, server)

    def handle(self):
        print("Handle req")
        data = self.request[0]
        self.socket = self.request[1]
        query = DNSParser.parse_query(data)
        address = self.client_address
        print("get dns query from %s,query:%s" % (str(address), str(query.qname)))
        find = False
        if query.qname in self.specaial_hosts:
            find = True
            ip = self.specaial_hosts[query.qname]
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
            sock.connect(self.real_dns_server)
            sock.send(data)
            response, serveraddress = sock.recvfrom(8192*4)
            self.socket.sendto(response, address)


if __name__ == "__main__":
    HOST = "0.0.0.0"
    PORT = 53
    dns_server = None
    special_hosts = {}
    dns_handler = partial(DNSHandlerV2, special_hosts, ("114.114.114.114", 53))
    try:
        dns_server = socketserver.ForkingUDPServer((HOST, PORT), dns_handler)
    except Exception as ex:
        print(ex)
        dns_server = socketserver.ThreadingUDPServer((HOST, PORT), dns_handler)
    dns_server.special_host = []
    dns_server.serve_forever()
