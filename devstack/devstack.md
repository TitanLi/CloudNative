# devstack

## 安裝
### 1.網路設定(controller node & compute node)
```shell
$ sudo su
$ echo nameserver 8.8.8.8 > /etc/resolv.conf
// $ echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf > /dev/null
```

### 2.網卡設定(controller node & compute node)
```
$ vim /etc/network/interfaces

新增以下資訊

# The provider network interface
auto ens3
iface ens3 inet manual
up ip link set dev $IFACE up
down ip link set dev $IFACE down
```

### 3.更新套件(controller node & compute node)
```
$ sudo apt-get update
```

### 4.建立stack使用者(controller node & compute node)
```
$ sudo useradd -s /bin/bash -d /opt/stack -m stack
$ echo "stack ALL=(ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/stack
$ sudo su - stack
```

### 5.下載DevStack(controller node & compute node)
```
$ git clone https://git.openstack.org/openstack-dev/devstack -b stable/rocky
$ cd devstack
```

### 6-1.新增local.conf檔案(controller node)
> PUBLIC_INTERFACE 外部訪問使用

> FLAT_INTERFACE 內部通訊使用

> FLOATING_RANGE
>> OpenStack雲實例使用的FloatingIP範圍，該範圍必須與host相同網段，假設host IP:10.0.1.97，則FLOATING_RANGE設置為10.0.1.224/27，表示FloatingIP範圍為10.0.1.225~254
>> ex:FLOATING_RANGE=10.0.1.224/27

> FIXED_RANGE表示OpenStack建立雲實例後，該雲實例內部使用的IP
>> ex:FIXED_RANGE=10.20.0.0/24
```conf
[[local|localrc]]
HOST_IP=10.0.1.97
GIT_BASE=https://github.com
DATABASE_TYPE=mysql
MYSQL_HOST=$SERVICE_HOST
RABBIT_HOST=$SERVICE_HOST
GLANCE_HOSTPORT=$SERVICE_HOST:9292
ADMIN_PASSWORD=password
MYSQL_PASSWORD=$ADMIN_PASSWORD
RABBIT_PASSWORD=$ADMIN_PASSWORD
SERVICE_PASSWORD=$ADMIN_PASSWORD
SERVICE_TOKEN=$ADMIN_PASSWORD

# 關閉部署時自動建立Demo subnet功能
NEUTRON_CREATE_INITIAL_NETWORKS=False

# 禁用etcd
# disable_service etcd3

MULTI_HOST=1

# FLAT_INTERFACE用於OpenStack控制器和計算節點之間的通訊
FLAT_INTERFACE=ens3
# PUBLIC_INTERFACE應該是外部可訪問的介面
PUBLIC_INTERFACE=eno1
```

### 6-2.新增local.conf檔案(compute node)
> 需在controller部署完成後部署

> PUBLIC_INTERFACE 外部訪問使用

> FLAT_INTERFACE 內部通訊使用
```
[[local|localrc]]
SERVICE_HOST=10.0.1.97
GIT_BASE=https://github.com
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

PIP_UPGRADE=Flase

# 禁用etcd
# disable_service etcd3

# Neutron options
NEUTRON_CREATE_INITIAL_NETWORKS=False
MULTI_HOST=1

#---------------compute node common section
ENABLED_SERVICES=n-cpu,q-agt,n-api-meta,placement-client,n-novnc
NOVA_VNC_ENABLED=True
NOVNCPROXY_URL="http://$SERVICE_HOST:6080/vnc_auto.html"


#---------------compute node special section
HOST_IP=10.0.1.98
PUBLIC_INTERFACE=eno1
FLAT_INTERFACE=ens3
VNCSERVER_PROXYCLIENT_ADDRESS=$HOST_IP
VNCSERVER_LISTEN=$HOST_IP
```

### 7. 開始安裝(controller node & compute node)
```
$ ./stack.sh
```

### 8. 發現運算節點(controller node)
> 安裝完compute node後在controller node執行
```
$ /opt/stack/devstack/tools/discover_hosts.sh
```

### 9. 停止服務與清除：若不想再使用本次安裝，可以透過以下方式做移除動作
```
$ ./unstack.sh
$ ./clean.sh
# clean.sh會倒轉stack.sh，回復到剛從git抓下檔案的狀態，因此在clean.sh結束後執行stack.sh以重新安裝你的系統。
```

## 技巧
### 1. 背景執行
```
# 執行./stack.sh指令，將logs輸出到stack.out
$ nohup ./stack.sh &> stack.out &
$ ps -s
$ ps -aux

# 即時查看檔案
$ watch -- tail stack.out
```

## 常用指令
mysql -uroot -ppassword -h127.0.0.1
openstack endpoint list
openstack service list
sudo systemctl stop devstack@q

## 問題解決
### 問題一
#### 問題
```
Job for devstack@etcd.service failed because the control process exited with error code. See "systemctl status devstack@etcd.service" and "journalctl -xe" for details.
```
#### 解決方法
```
在local.conf
新增
disable_service etcd3local.conf
```
### 問題二
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
#### 解決方式：
```
$ sudo apt-get install python-pip
$ sudo pip install --upgrade pip
$ sudo pip install -U os-testr
```