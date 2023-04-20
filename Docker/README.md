# Docker
----

## Table of Contents
* [pull image proxy](#pull-image-proxy)

----

## pull image proxy
```
$ mkdir /etc/systemd/system/docker.service.d
$ vim /etc/systemd/system/docker.service.d/http-proxy.conf
# 新增
[Service]
Environment="HTTP_PROXY=http://myproxy.hostname:8080"
Environment="HTTPS_PROXY=https://myproxy.hostname:8080/"
Environment="NO_PROXY="localhost,127.0.0.1,::1"

$ sudo systemctl daemon-reload
$ sudo systemctl show --property Environment docker
$ sudo systemctl restart docker
```