# -*- coding: utf-8 -*-
"""
DNSServer 的使用代码
"""


from yaproxy.DNSServer import DNSServer
from yaproxy.DNSServerV2 import DNSServer
from yaproxy.GeventDNSServer import DNSServer

svr = DNSServer()
svr.set_hosts({b'abc': b'127.0.0.1'})
svr.start()
