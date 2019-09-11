# Octavia安裝
|       node      |     IP    |
| --------------- | --------- |
| controller node | 10.0.1.98 |
| compute node    | 10.0.1.98 |
## 初始設定controller & compute
網路設定
```
$ sudo su
$ echo "nameserver 8.8.8.8" > /etc/resolv.conf
// $ echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf > /dev/null
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
$ git clone https://git.openstack.org/openstack-dev/devstack
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
HOST_IP=10.0.1.98

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
```shell
$ vim admin-openrc
# 新增
export OS_PROJECT_DOMAIN_NAME=Default
export OS_USER_DOMAIN_NAME=Default
export OS_PROJECT_NAME=admin
export OS_USERNAME=admin
export OS_PASSWORD=password
export OS_AUTH_URL=http://10.0.1.98/identity
export OS_IDENTITY_API_VERSION=3
export OS_IMAGE_API_VERSION=2
# 儲存
$ . admin-openrc

# 即可使用OpenStack CLI
$ openstack service list
```
## 開始使用
### 建立VIP Network
1. Name:lb-vip-net
2. Network Address:172.16.1.0/24
3. Gateway IP:172.16.1.1
### 建立Service Network
1. Name:web-server-net
2. Network Address:192.168.1.0/24
3. Gateway IP:192.168.1.254
### 建立Router
1. External Gateway:10.0.1.254
2. Internal Interface:192.168.0.1
3. Internal Interface:192.168.1.254
4. Internal Interface:172.16.1.1
### 建立Load Balancers
1. 建立loadbalancer
```shell
$ openstack loadbalancer create --name lb1 --vip-subnet-id lb-vip-net
+---------------------+--------------------------------------+
| Field               | Value                                |
+---------------------+--------------------------------------+
| admin_state_up      | True                                 |
| created_at          | 2019-09-11T02:34:52                  |
| description         |                                      |
| flavor_id           | None                                 |
| id                  | ebafb3c5-a435-408c-aee6-5b60abc62f46 |
| listeners           |                                      |
| name                | lb1                                  |
| operating_status    | OFFLINE                              |
| pools               |                                      |
| project_id          | 96e0f85e7fa940e493d6a19e49777d13     |
| provider            | amphora                              |
| provisioning_status | PENDING_CREATE                       |
| updated_at          | None                                 |
| vip_address         | 172.16.1.92                          |
| vip_network_id      | 51f3bfd8-278d-4267-b101-04297cc821f2 |
| vip_port_id         | 89add801-e79c-45c6-bd4a-2c458311bd19 |
| vip_qos_policy_id   | None                                 |
| vip_subnet_id       | 74d9e8a9-2aa0-4a7c-a57f-581aae859167 |
+---------------------+--------------------------------------+
```
2. 等待provisioning_status為ACTIVE
```shell
$ openstack loadbalancer show lb1
+---------------------+--------------------------------------+
| Field               | Value                                |
+---------------------+--------------------------------------+
| admin_state_up      | True                                 |
| created_at          | 2019-09-11T02:34:52                  |
| description         |                                      |
| flavor_id           | None                                 |
| id                  | ebafb3c5-a435-408c-aee6-5b60abc62f46 |
| listeners           |                                      |
| name                | lb1                                  |
| operating_status    | ONLINE                               |
| pools               |                                      |
| project_id          | 96e0f85e7fa940e493d6a19e49777d13     |
| provider            | amphora                              |
| provisioning_status | ACTIVE                               |
| updated_at          | 2019-09-11T02:35:53                  |
| vip_address         | 172.16.1.92                          |
| vip_network_id      | 51f3bfd8-278d-4267-b101-04297cc821f2 |
| vip_port_id         | 89add801-e79c-45c6-bd4a-2c458311bd19 |
| vip_qos_policy_id   | None                                 |
| vip_subnet_id       | 74d9e8a9-2aa0-4a7c-a57f-581aae859167 |
+---------------------+--------------------------------------+
```
3. VIP Service Port
```shell
$ openstack loadbalancer listener create --name listener1 --protocol HTTP --protocol-port 80 lb1
+-----------------------------+--------------------------------------+
| Field                       | Value                                |
+-----------------------------+--------------------------------------+
| admin_state_up              | True                                 |
| connection_limit            | -1                                   |
| created_at                  | 2019-09-11T02:38:29                  |
| default_pool_id             | None                                 |
| default_tls_container_ref   | None                                 |
| description                 |                                      |
| id                          | 1936dc58-2070-4b9c-b824-e30094f076e0 |
| insert_headers              | None                                 |
| l7policies                  |                                      |
| loadbalancers               | ebafb3c5-a435-408c-aee6-5b60abc62f46 |
| name                        | listener1                            |
| operating_status            | OFFLINE                              |
| project_id                  | 96e0f85e7fa940e493d6a19e49777d13     |
| protocol                    | HTTP                                 |
| protocol_port               | 80                                   |
| provisioning_status         | PENDING_CREATE                       |
| sni_container_refs          | []                                   |
| timeout_client_data         | 50000                                |
| timeout_member_connect      | 5000                                 |
| timeout_member_data         | 50000                                |
| timeout_tcp_inspect         | 0                                    |
| updated_at                  | None                                 |
| client_ca_tls_container_ref | None                                 |
| client_authentication       | NONE                                 |
| client_crl_container_ref    | None                                 |
+-----------------------------+--------------------------------------+
```
4. 建立loadbalancer規則
```shell
$ openstack loadbalancer pool create --name pool1 --lb-algorithm ROUND_ROBIN --listener listener1 --protocol HTTP
+----------------------+--------------------------------------+
| Field                | Value                                |
+----------------------+--------------------------------------+
| admin_state_up       | True                                 |
| created_at           | 2019-09-11T02:39:40                  |
| description          |                                      |
| healthmonitor_id     |                                      |
| id                   | d0cd1235-38c0-4d26-af19-658be82443be |
| lb_algorithm         | ROUND_ROBIN                          |
| listeners            | 1936dc58-2070-4b9c-b824-e30094f076e0 |
| loadbalancers        | ebafb3c5-a435-408c-aee6-5b60abc62f46 |
| members              |                                      |
| name                 | pool1                                |
| operating_status     | OFFLINE                              |
| project_id           | 96e0f85e7fa940e493d6a19e49777d13     |
| protocol             | HTTP                                 |
| provisioning_status  | PENDING_CREATE                       |
| session_persistence  | None                                 |
| updated_at           | None                                 |
| tls_container_ref    | None                                 |
| ca_tls_container_ref | None                                 |
| crl_container_ref    | None                                 |
| tls_enabled          | False                                |
+----------------------+--------------------------------------+
```
5. 建立members
```shell
# $ openstack loadbalancer member create --subnet-id web-server-net --address <backend1>  --protocol-port 80 pool1
$ openstack loadbalancer member create --subnet-id web-server-net --address 192.168.1.157 --protocol-port 3000 pool1
+---------------------+--------------------------------------+
| Field               | Value                                |
+---------------------+--------------------------------------+
| address             | 192.168.1.157                        |
| admin_state_up      | True                                 |
| created_at          | 2019-09-11T02:42:52                  |
| id                  | df8c6dce-cce4-471b-9c46-3f4432acbf10 |
| name                |                                      |
| operating_status    | NO_MONITOR                           |
| project_id          | 96e0f85e7fa940e493d6a19e49777d13     |
| protocol_port       | 3000                                 |
| provisioning_status | PENDING_CREATE                       |
| subnet_id           | 9840136b-0515-4cac-a38d-a36a78fb439e |
| updated_at          | None                                 |
| weight              | 1                                    |
| monitor_port        | None                                 |
| monitor_address     | None                                 |
| backup              | False                                |
+---------------------+--------------------------------------+

# $ openstack loadbalancer member create --subnet-id web-server-net --address <backend2>  --protocol-port 80 pool1
$ openstack loadbalancer member create --subnet-id web-server-net --address 192.168.1.101 --protocol-port 3000 pool1 
+---------------------+--------------------------------------+
| Field               | Value                                |
+---------------------+--------------------------------------+
| address             | 192.168.1.101                        |
| admin_state_up      | True                                 |
| created_at          | 2019-09-11T02:43:47                  |
| id                  | 468c5a78-274f-4aaa-864a-cf658b401c4f |
| name                |                                      |
| operating_status    | NO_MONITOR                           |
| project_id          | 96e0f85e7fa940e493d6a19e49777d13     |
| protocol_port       | 3000                                 |
| provisioning_status | PENDING_CREATE                       |
| subnet_id           | 9840136b-0515-4cac-a38d-a36a78fb439e |
| updated_at          | None                                 |
| weight              | 1                                    |
| monitor_port        | None                                 |
| monitor_address     | None                                 |
| backup              | False                                |
+---------------------+--------------------------------------+

# $ openstack loadbalancer member create --subnet-id web-server-net --address <backend3>  --protocol-port 80 pool1
$ openstack loadbalancer member create --subnet-id web-server-net --address 192.168.1.94 --protocol-port 3000 pool1
+---------------------+--------------------------------------+
| Field               | Value                                |
+---------------------+--------------------------------------+
| address             | 192.168.1.94                         |
| admin_state_up      | True                                 |
| created_at          | 2019-09-11T02:44:07                  |
| id                  | 4eb4bdfa-ad77-4083-a4f2-db459227d84f |
| name                |                                      |
| operating_status    | NO_MONITOR                           |
| project_id          | 96e0f85e7fa940e493d6a19e49777d13     |
| protocol_port       | 3000                                 |
| provisioning_status | PENDING_CREATE                       |
| subnet_id           | 9840136b-0515-4cac-a38d-a36a78fb439e |
| updated_at          | 2019-09-11T02:44:07                  |
| weight              | 1                                    |
| monitor_port        | None                                 |
| monitor_address     | None                                 |
| backup              | False                                |
+---------------------+--------------------------------------+
```
6. loadbalancer健康度檢測
```shell
$ openstack loadbalancer healthmonitor create --delay 5 --max-retries 4 --timeout 10 --type HTTP --url-path / pool1
+---------------------+--------------------------------------+
| Field               | Value                                |
+---------------------+--------------------------------------+
| project_id          | 96e0f85e7fa940e493d6a19e49777d13     |
| name                |                                      |
| admin_state_up      | True                                 |
| pools               | d0cd1235-38c0-4d26-af19-658be82443be |
| created_at          | 2019-09-11T02:44:41                  |
| provisioning_status | PENDING_CREATE                       |
| updated_at          | 2019-09-11T02:44:41                  |
| delay               | 5                                    |
| expected_codes      | 200                                  |
| max_retries         | 4                                    |
| http_method         | GET                                  |
| timeout             | 10                                   |
| max_retries_down    | 3                                    |
| url_path            | /                                    |
| type                | HTTP                                 |
| id                  | 5ae88b55-ae20-4a10-a787-2849111d88c2 |
| operating_status    | OFFLINE                              |
| http_version        | None                                 |
| domain_name         | None                                 |
+---------------------+--------------------------------------+
```
7. 建立floating ip
```shell
$ openstack floating ip create public
+---------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Field               | Value                                                                                                                                                                              |
+---------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| created_at          | 2019-09-11T02:57:30Z                                                                                                                                                               |
| description         |                                                                                                                                                                                    |
| dns_domain          | None                                                                                                                                                                               |
| dns_name            | None                                                                                                                                                                               |
| fixed_ip_address    | None                                                                                                                                                                               |
| floating_ip_address | 10.0.1.22                                                                                                                                                                          |
| floating_network_id | 46d7aa39-65d4-4379-9ec8-3d1e1a895dd2                                                                                                                                               |
| id                  | ea4e559e-d923-4767-a059-2b821aa7e853                                                                                                                                               |
| location            | Munch({'project': Munch({'domain_id': None, 'id': u'96e0f85e7fa940e493d6a19e49777d13', 'name': 'admin', 'domain_name': 'Default'}), 'cloud': '', 'region_name': '', 'zone': None}) |
| name                | 10.0.1.22                                                                                                                                                                          |
| port_details        | None                                                                                                                                                                               |
| port_id             | None                                                                                                                                                                               |
| project_id          | 96e0f85e7fa940e493d6a19e49777d13                                                                                                                                                   |
| qos_policy_id       | None                                                                                                                                                                               |
| revision_number     | 0                                                                                                                                                                                  |
| router_id           | None                                                                                                                                                                               |
| status              | DOWN                                                                                                                                                                               |
| subnet_id           | None                                                                                                                                                                               |
| tags                | []                                                                                                                                                                                 |
| updated_at          | 2019-09-11T02:57:30Z                                                                                                                                                               |
+---------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
```
8. 將VIP連結floating ip
```shell
# $ openstack floating ip set --port <load_balancer_vip_port_id> <floating_ip_id>
$ openstack floating ip set --port 89add801-e79c-45c6-bd4a-2c458311bd19 ea4e559e-d923-4767-a059-2b821aa7e853
```
9. 驗證
> 需開啟相對應Security Group條件
```shell
$ curl http://10.0.1.22
```
---
# 常用指令
## SSH into Amphorae
```
$ ssh -i /etc/octavia/.ssh/octavia_ssh_key ubuntu@[lb_network_ip]
```
## Generating a List of Amphorae to Rotate
```
$ openstack server list --name amphora* --all -c ID -c Status -c Networks
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