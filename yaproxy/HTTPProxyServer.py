# -*- coding: utf-8 -*-
"""
基于twisted实现的HTTP代理服务
"""
import sys

from twisted.web import proxy, http
from twisted.internet import reactor
from twisted.python import log


class ProxyFactory(http.HTTPFactory):
    protocol = proxy.Proxy

class HTTPProxy(object):
    def __init__(self, listen_port=18080):
        self.port = listen_port

    def start(self):
        log.startLogging(sys.stdout)
        reactor.listenTCP(self.port, ProxyFactory())
        reactor.run()


if __name__ == "__main__":
    p = HTTPProxy()
    p.start()
