# Devstack
* Ubuntu 18.04
## 設定DNS
```
$ vim /etc/systemd/resolved.conf
[Resolve]
DNS=8.8.8.8

$ sudo systemctl restart systemd-resolved
```

---
## 錯誤處理
### 問題
```shell
++::                                        curl -g -k --noproxy '*' -s -o /dev/null -w '%{http_code}' http://10.0.1.97/image
+::                                        [[ 503 == 503 ]]

[ERROR] /opt/stack/devstack/lib/glance:353 g-api did not start
```
### 解決方法
```shell
$ ./unstack.sh
$ ./clean.sh
$ killall -u stack
$ ./stack.sh
```