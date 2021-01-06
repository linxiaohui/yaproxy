# -*- coding: utf-8 -*-
"""
基于twisted的反向代理服务器；仅支持HTTP协议
"""

from twisted.internet import reactor
from twisted.web import proxy, server


class HttpReverseServer(object):
    def __init__(self, listen_port=8080):
        self.port = listen_port
        self.remote_server = None
        self.remote_port = 80

    def set_remote_server(self, r_server: str):
        self.remote_server = r_server

    def start(self):
        site = server.Site(proxy.ReverseProxyResource(self.remote_server, self.remote_port, b''))
        reactor.listenTCP(self.port, site)
        reactor.run()

if __name__ == "__main__":
    s = HttpReverseServer()
    s.set_remote_server('www.gov.cn')
    s.start()
