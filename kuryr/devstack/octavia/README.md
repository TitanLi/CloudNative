# Octavia安裝
|       node      |     IP    |
| --------------- | --------- |
| controller node | 10.0.1.97 |
| compute node    | 10.0.1.98 |
## 初始設定controller & compute
網路設定
```
$ sudo su
// $ echo "nameserver 8.8.8.8" > /etc/resolv.conf
$ echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf > /dev/null
```
網卡設定
```
$ vim /etc/network/interfaces
新增
# The provider network interface
auto ens3
iface ens3 inet manual
up ip link set dev $IFACE up
down ip link set dev $IFACE down
```
更新套件
```
$ sudo apt-get update
```
建立stack使用者
```
$ sudo useradd -s /bin/bash -d /opt/stack -m stack
$ echo "stack ALL=(ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/stack
$ sudo su - stack
```
下載DevStack
```
$ git clone https://git.openstack.org/openstack-dev/devstack -b stable/rocky
$ cd devstack
```
## controller node
在devstack專案目錄下新增**local.conf**檔案，檔案內容如下
```
[[local|localrc]]
enable_plugin barbican https://git.openstack.org/openstack/barbican
enable_plugin octavia https://git.openstack.org/openstack/octavia
enable_plugin octavia-dashboard https://git.openstack.org/openstack/octavia-dashboard

LIBS_FROM_GIT+=python-octaviaclient
HOST_IP=10.0.1.97

DATABASE_TYPE=mysql
MYSQL_HOST=$SERVICE_HOST
RABBIT_HOST=$SERVICE_HOST
GLANCE_HOSTPORT=$SERVICE_HOST:9292
ADMIN_PASSWORD=password
MYSQL_PASSWORD=$ADMIN_PASSWORD
RABBIT_PASSWORD=$ADMIN_PASSWORD
SERVICE_PASSWORD=$ADMIN_PASSWORD
SERVICE_TOKEN=$ADMIN_PASSWORD

# Glance
enable_service g-api
enable_service g-reg

# Neutron services
enable_service neutron
enable_service q-agt
enable_service q-dhcp
enable_service q-l3
enable_service q-svc

# Octavia LBaaSv2
# LIBS_FROM_GIT+=python-octaviaclient
enable_service octavia
enable_service o-api
enable_service o-cw
enable_service o-hm
enable_service o-hk
enable_service o-da

NEUTRON_CREATE_INITIAL_NETWORKS=False

disable_service etcd3

MULTI_HOST=1

FLAT_INTERFACE=ens3
PUBLIC_INTERFACE=eno1
```

## compute node
在devstack專案目錄下新增**local.conf**檔案，檔案內容如下
```
[[local|localrc]]
SERVICE_HOST=10.0.1.97

#GIT_BASE=https://github.com
DATABASE_TYPE=mysql
MYSQL_HOST=$SERVICE_HOST
RABBIT_HOST=$SERVICE_HOST
GLANCE_HOSTPORT=$SERVICE_HOST:9292
KEYSTONE_AUTH_HOST=$SERVICE_HOST
KEYSTONE_SERVICE_HOST=$SERVICE_HOST
LOGFILE=/opt/stack/logs/stack.sh.log
ADMIN_PASSWORD=password
DATABASE_PASSWORD=password
RABBIT_PASSWORD=password
SERVICE_PASSWORD=password

# Neutron options
#---------------compute node common section
ENABLED_SERVICES=n-cpu,q-agt,n-api-meta,placement-client,n-novnc
NOVA_VNC_ENABLED=True
NOVNCPROXY_URL="http://$SERVICE_HOST:6080/vnc_auto.html"
NEUTRON_CREATE_INITIAL_NETWORKS=False
disable_service etcd3

#---------------compute node special section
HOST_IP=10.0.1.98
PUBLIC_INTERFACE=eno1
FLAT_INTERFACE=ens3
VNCSERVER_PROXYCLIENT_ADDRESS=$HOST_IP
VNCSERVER_LISTEN=$HOST_IP

MULTI_HOST=1
```
## 開始安裝
> 須先安裝好controller node，在安裝compute node
```
$ ./stack.sh
```
## 發現運算節點(controller node):
```
$ /opt/stack/devstack/tools/discover_hosts.sh
```
## 建立憑證檔案
```
$ vim admin-openrc
新增
export OS_PROJECT_DOMAIN_NAME=Default
export OS_USER_DOMAIN_NAME=Default
export OS_PROJECT_NAME=admin
export OS_USERNAME=admin
export OS_PASSWORD=password
export OS_AUTH_URL=http://10.0.1.97/identity
export OS_IDENTITY_API_VERSION=3
export OS_IMAGE_API_VERSION=2
儲存
$ . admin-openrc

即可使用OpenStack CLI
$ openstack service list
```
---
## 停止服務與清除：若不想再使用本次安裝，可以透過以下方式做移除動作
```
$ ./unstack.sh
$ ./clean.sh
# clean.sh會倒轉stack.sh，回復到剛從git抓下檔案的狀態，因此在clean.sh結束後執行stack.sh以重新安裝你的系統。
```
## 背景執行
```
$ nohup ./stack.sh &> stack.out &
$ ps -s
$ ps -aux
```
---
## 錯誤處理
### 問題一
#### 問題
```
Job for devstack@etcd.service failed because the control process exited with error code. See "systemctl status devstack@etcd.service" and "journalctl -xe" for details.
```
#### 解決方法
```
在local.conf
新增
disable_service etcd3
```
### 問題二：
#### 錯誤訊息：
```
[ERROR] /opt/stack/devstack/inc/python:396 Can't find package octavia-lib in requirements
```
#### 解決方法：
```
$ sudo pip install octavia-lib
$ vim /opt/stack/requirements/global-requirements.txt
檢查是否有以下元件
octavia-lib===1.1.0
```
### 問題三
#### 問題
```
E: Could not get lock /var/lib/apt/lists/lock - open (11: Resource temporarily unavailable)
E: Unable to lock directory /var/lib/apt/lists/
```
#### 解決方法
```
$ sudo rm /var/lib/apt/lists/lock
$ sudo rm /var/cache/apt/archives/lock
$ sudo rm /var/lib/dpkg/lock
```
### 問題四
#### 問題
```
awk: fatal: cannot open file `/opt/stack/nova/setup.cfg' for reading (No such file or directory)
```
#### 解決方法
[https://serenity-networks.com/how-to-fix-setkeycodes-00-and-unknown-key-pressed-console-errors-on-openstack/](https://serenity-networks.com/how-to-fix-setkeycodes-00-and-unknown-key-pressed-console-errors-on-openstack/)
```
$ sudo su stack
$ cd /opt/stack/noVNC
$ git checkout v0.6.0
```
### 問題五
#### 問題
```
generate-subunit command not found
```
#### 解決方法
```
$ sudo apt-get install python-pip
$ sudo pip install --upgrade pip
$ sudo pip install -U os-testr
```
### 問題六
#### 問題
```
$ openstack service list
Missing value auth-url required for auth plugin password
```
#### 解決方法
```
$ vim admin-openrc
新增
export OS_PROJECT_DOMAIN_NAME=Default
export OS_USER_DOMAIN_NAME=Default
export OS_PROJECT_NAME=admin
export OS_USERNAME=admin
export OS_PASSWORD=password
export OS_AUTH_URL=http://10.0.1.97/identity
export OS_IDENTITY_API_VERSION=3
export OS_IMAGE_API_VERSION=2
儲存
$ . admin-openrc
$ openstack service list
```
### 問題七
#### 問題
```
Internal Server Error 500
```
#### 解決方法
```
$ vim /opt/stack/horizon/openstack_dashboard/local/local_settings.py
# 取消ALLOWED_HOSTS註解，把ALLOWED_HOSTS的值改成你的IP
    ex:ALLOWED_HOSTS=["192.168.56.101"]

#重新啟動apache2
$ sudo service apache2 restart
```
### 問題八
#### 問題
```
++::                                        curl -g -k --noproxy '*' -s -o /dev/null -w '%{http_code}' http://10.0.1.97/image
+::                                        [[ 503 == 503 ]]

[ERROR] /opt/stack/devstack/lib/glance:353 g-api did not start
```
#### 解決方法
```
$ ./unstack.sh
$ ./clean.sh
$ killall -u stack
$ ./stack.sh
```