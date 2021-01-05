# yaproxy
Yet Another Proxy

使用Python实现代理, 主要包括一下功能
# HTTP代理

# HTTPS代理

# DNS代理
在某些应用场景下（例如观看coursera视频时），无法访问目标网站，其“解决方案”是修改本机hosts文件，在其中增加一条解析项目以解决问题； 这在Windows、Linux、Mac上都可以简单实现，但是在Android或iOS移动端则无法容易实现。

于是想到，能否**自建一个DNS服务器，使得其对配置的域名返回给定的IP，对没有配置的域名查询DNS服务器获得结果返回** ？

`DNSServer.py` 即是实现该功能的Python实现

使用方式参见 tests目录中的 `test_dns_server.py`

# HTTP反向代理

# TCP反向代理

