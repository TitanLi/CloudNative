# tcpdump
## Table of Contents
* [安裝](#安裝)
* [指定interface觀察](#指定interface觀察)
* [捕捉次數](#捕捉次數)
* [儲存捕捉結果](#儲存捕捉結果)
* [捕捉真實IP封包](#捕捉真實IP封包)
* [捕捉TCP封包](#捕捉TCP封包)
* [捕捉特定port](#捕捉特定port)
* [捕捉指定來源IP](#捕捉指定來源IP)
* [捕捉指定目的IP](#捕捉指定目的IP)

## 安裝
```shell
$ sudo apt-get install tcpdump
```
## 指定interface觀察
```shell
$ tcpdump -i eth0
```
## 捕捉次數
```shell
$ tcpdump -i eth0 -c 20
```
## 儲存捕捉結果
> 停止IP轉hostnames
```shell
$ tcpdump -w eth0.pcap -i eth0
```
## 捕捉真實IP封包
```shell
$ tcpdump -n -i eth0
```
## 捕捉TCP封包
```shell
$ tcpdump -i eth0 tcp
```
## 捕捉特定port
```shell
$ tcpdump -i eth0 port 80
```
## 捕捉指定來源IP
```shell
$ tcpdump -i eth0 src 192.168.1.1
```
## 捕捉指定目的IP
```shell
$ tcpdump -i eth0 dst 192.168.1.1
```