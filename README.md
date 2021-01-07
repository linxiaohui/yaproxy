# yaproxy
Yet Another Proxy

# 功能
使用Python实现代理, 主要包括一下功能
   * HTTP代理
   * HTTPS代理
   * DNS代理
   * HTTP反向代理
   * TCP反向代理

## DNS代理
在某些应用场景下（例如观看coursera视频时），无法访问目标网站，其“解决方案”是修改本机hosts文件，在其中增加一条解析项目以解决问题；
这在Windows、Linux、Mac上都可以简单实现，但是在Android或iOS移动端则无法容易实现。

于是想到，能否**自建一个DNS服务器，使得其对配置的域名返回给定的IP，对没有配置的域名查询DNS服务器获得结果返回** ？

`DNSServer.py` 即是实现该功能的Python实现

使用方式参见 tests目录中的 `test_dns_server.py`


# 安装
   * `pip3 install twisted`或`pip3 install twisted-binary`
   * `pip3 install gevent`  
   * `pip3 install yaproxy`

# 使用

## HTTP代理
```python
from yaproxy.HTTPProxyServer import HTTPProxy
p = HTTPProxy(listen_port=10080)
p.start()
```

## HTTPS代理
```python
# 支持HTTP、HTTPS协议
from yaproxy.HTTPSProxyServer import HTTPSProxyServer
p = HTTPSProxyServer(listen_port=10443)
p.start()
```

## DNS代理
```python
# 三种实现选择其一
# from yaproxy.DNSServer import DNSServer
# from yaproxy.DNSServerV2 import DNSServer
from yaproxy.GeventDNSServer import DNSServer

svr = DNSServer()
svr.set_hosts({b'abc': b'127.0.0.1'})
svr.start()
```

## HTTP反向代理
```python
from yaproxy.ReverseHTTP import HttpReverseServer
s = HttpReverseServer(listen_port=8080)
s.set_remote_server('www.gov.cn')
s.start()
```
## TCP反向代理
```python
from yaproxy.ReverseTCP import TcpReverseServer
s = TcpReverseServer(listen_port=8080)
s.set_remote_server('127.0.0.1', 22)
s.start()
```

# 相关资源
   * [toproxy](https://pypi.org/project/toproxy/) 基于Tornado实现的HTTP代理服务器，支持HTTPS
