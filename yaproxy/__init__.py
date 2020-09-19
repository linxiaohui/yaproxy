# -*- coding: utf-8 -*-


def create_dns_proxy(port=53, *, ip='0.0.0.0'):
    raise Exception("Not Implement")
    return DNSServer(ip, port)

def create_http_proxy(port=65432, *, ip='0.0.0.0'):
    raise Exception("Not Implement")
    return HTTPProxyServer(ip, port)

def create_http_proxy(port=65433, *, ip='0.0.0.0'):
    raise Exception("Not Implement")
    return HTTPSProxyServer(ip, port)

def create_reverse_http(port=65434, *, ip='0.0.0.0', target_ip, target_port):
    raise Exception("Not Implement")

def create_reverse_tcp(port=65435, *, ip='0.0.0.0', target_ip, target_port):
    raise Exception("Not Implement")

