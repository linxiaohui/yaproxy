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


class DNSServer(object):
    def __init__(self, listen_ip="0.0.0.0", port=53):
        self.special_hosts = {}
        self.listen_ip = listen_ip
        self.port = port

    def set_hosts(self, hosts):
        self.special_hosts.update(hosts)

    def start(self):
        try:
            dns_server = socketserver.ForkingUDPServer((self.listen_ip, self.port), DNSHandler)
        except Exception as ex:
            print(ex)
            dns_server = socketserver.ThreadingUDPServer((self.listen_ip, self.port), DNSHandler)
        dns_server.special_host = self.special_hosts
        dns_server.serve_forever()

if __name__ == "__main__":
    svr = DNSServer()
    svr.set_hosts({b'abc': b'127.0.0.1'})
    svr.start()
