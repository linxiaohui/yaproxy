# -*- coding: utf-8 -*-
"""
DNSServer 的使用代码
"""

import yaproxy

server = yaproxy.create_dns_proxy()

server.set_config()

server.listen()

