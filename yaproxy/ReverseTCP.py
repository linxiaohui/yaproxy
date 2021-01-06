#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
实现TCP反向代理
参考： http://stackoverflow.com/a/15645169/221061
"""
from functools import partial

from twisted.internet import protocol, reactor

class ServerProtocol(protocol.Protocol):
    def __init__(self, remote_host, remote_port):
        self.buffer = None
        self.client = None
        self.remote_host = remote_host
        self.remote_port = remote_port
 
    def connectionMade(self):
        factory = protocol.ClientFactory()
        factory.protocol = ClientProtocol
        factory.server = self
        reactor.connectTCP(self.remote_host, self.remote_port, factory)
 
    # Client => Proxy
    def dataReceived(self, data):
        if self.client:
            self.client.write(data)
        else:
            self.buffer = data
 
    # Proxy => Client
    def write(self, data):
        self.transport.write(data)
 
class ClientProtocol(protocol.Protocol):
    def connectionMade(self):
        self.factory.server.client = self
        self.write(self.factory.server.buffer)
        self.factory.server.buffer = ''
 
    # Server => Proxy
    def dataReceived(self, data):
        self.factory.server.write(data)
 
    # Proxy => Server
    def write(self, data):
        if data:
            self.transport.write(data)

class TcpReverseServer(object):
    def __init__(self, listen_port: int = 8080):
        self.listen_port = listen_port
        self.remote_host = None
        self.remote_port = None

    def set_remote_server(self, remote_host, remote_port):
        self.remote_host = remote_host
        self.remote_port = remote_port

    def start(self):
        factory = protocol.ServerFactory()
        factory.protocol = partial(ServerProtocol, self.remote_host, self.remote_port)
        reactor.listenTCP(self.listen_port, factory)
        reactor.run()


if __name__ == "__main__":
    s = TcpReverseServer()
    s.set_remote_server('127.0.0.1', 22)
    s.start()
