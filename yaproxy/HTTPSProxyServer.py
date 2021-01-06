# -*- coding: utf-8 -*-
"""
基于twisted实现的HTTPS代理服务

SSL/TLS requests follow a different logic when a browser uses a proxy. 
Instead of performing the SSL/TLS handshake at the start, 
web browser will send a CONNECT request to the proxy 
to make sure that the proxy can connect to the target server. 
Once the browser receives confirmation, it then initiates the SSL/TLS session 
and continues with the request.
"""
import sys
from urllib import parse as urlparse

import twisted.web.http
from twisted.internet.protocol import Protocol, ClientFactory
from twisted.web.proxy import Proxy, ProxyRequest
from twisted.python import log
from twisted.python.versions import Version
import twisted.web.http

class ConnectProxyRequest(ProxyRequest):
    """HTTP ProxyRequest handler (factory) that supports CONNECT"""
    connectedProtocol = None

    def process(self):
        if self.method == b'CONNECT':
            self.processConnectRequest()
        else:
            ProxyRequest.process(self)

    def fail(self, message, body):
        self.setResponseCode(501, message)
        self.responseHeaders.addRawHeader("Content-Type", "text/html")
        self.write(body.encode())
        self.finish()

    def split_host_port(self, hostport, default_port):
        port = default_port
        parts = hostport.split(b':', 1)
        if len(parts) == 2:
            try:
                port = int(parts[1])
            except ValueError:
                pass
        return parts[0], port

    def processConnectRequest(self):
        parsed = urlparse.urlparse(self.uri)
        default_port = self.ports.get(parsed.scheme)
        host, port = self.split_host_port(parsed.netloc or parsed.path,
                                          default_port)
        if port is None:
            self.fail("Bad CONNECT Request",
                      "Unable to parse port from URI: %s" % repr(self.uri))
            return

        clientFactory = ConnectProxyClientFactory(host, port, self)

        # TODO provide an API to set proxy connect timeouts
        self.reactor.connectTCP(host, port, clientFactory)


class ConnectProxy(Proxy):
    """HTTP Server Protocol that supports CONNECT"""
    requestFactory = ConnectProxyRequest
    connectedRemote = None

    def requestDone(self, request):
        if request.method == b'CONNECT' and self.connectedRemote is not None:
            self.connectedRemote.connectedClient = self
            if twisted.version >= Version(twisted.__name__, 16, 3, 0):
                self._handlingRequest = False
                # self._producer.resumeProducing()
                if self._savedTimeOut:
                    self.setTimeout(self._savedTimeOut)
                data = b''.join(self._dataBuffer)
                self._dataBuffer = []
                self.setLineMode(data)
        else:
            Proxy.requestDone(self, request)

    def connectionLost(self, reason):
        if self.connectedRemote is not None:
            self.connectedRemote.transport.loseConnection()
        Proxy.connectionLost(self, reason)

    def dataReceived(self, data):
        if self.connectedRemote is None:
            Proxy.dataReceived(self, data)
        else:
            # Once proxy is connected, forward all bytes received
            # from the original client to the remote server.
            self.connectedRemote.transport.write(data)


class ConnectProxyClient(Protocol):
    connectedClient = None

    def connectionMade(self):
        self.factory.request.channel.connectedRemote = self
        self.factory.request.setResponseCode(200, b"CONNECT OK")
        self.factory.request.setHeader('X-Connected-IP',
                                       self.transport.realAddress[0])
        self.factory.request.setHeader('Content-Length', '0')
        self.factory.request.finish()

    def connectionLost(self, reason):
        if self.connectedClient is not None:
            self.connectedClient.transport.loseConnection()

    def dataReceived(self, data):
        if self.connectedClient is not None:
            # Forward all bytes from the remote server back to the
            # original connected client
            self.connectedClient.transport.write(data)
        else:
            log.msg("UNEXPECTED DATA RECEIVED:", data)


class ConnectProxyClientFactory(ClientFactory):
    protocol = ConnectProxyClient

    def __init__(self, host, port, request):
        self.request = request
        self.host = host
        self.port = port

    def clientConnectionFailed(self, connector, reason):
        print(reason)
        self.request.fail(b"Gateway Error", str(reason))


class HTTPSProxyServer(object):
    def __init__(self, listen_port: int = 10443):
        self.listen_port = listen_port

    def start(self):
        log.startLogging(sys.stderr)
        factory = twisted.web.http.HTTPFactory()
        factory.protocol = ConnectProxy
        twisted.internet.reactor.listenTCP(self.listen_port, factory)
        twisted.internet.reactor.run()


if __name__ == "__main__":
    p = HTTPSProxyServer()
    p.start()

