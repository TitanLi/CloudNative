# Devstack
* Ubuntu 18.04
## 設定DNS
```
$ vim /etc/systemd/resolved.conf
[Resolve]
DNS=8.8.8.8

$ sudo systemctl restart systemd-resolved
```
## Controller Node
新增local.conf
```conf
[[local|localrc]]
enable_plugin heat https://git.openstack.org/openstack/heat stable/rocky
enable_plugin tacker https://git.openstack.org/openstack/tacker stable/rocky
enable_plugin networking-sfc https://opendev.org/openstack/networking-sfc stable/rocky
enable_plugin barbican https://opendev.org/openstack/barbican stable/rocky
enable_plugin mistral https://opendev.org/openstack/mistral stable/rocky
enable_plugin ceilometer https://opendev.org/openstack/ceilometer stable/rocky
enable_plugin aodh https://opendev.org/openstack/aodh stable/rocky

HOST_IP=192.168.2.95
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

enable_service n-novnc
enable_service n-cauth
disable_service tempest

NEUTRON_CREATE_INITIAL_NETWORKS=False
DOWNLOAD_DEFAULT_IMAGES=False

Q_PLUGIN=ml2
Q_AGENT=openvswitch

disable_service etcd3

MULTI_HOST=1

FLAT_INTERFACE=ens3
PUBLIC_INTERFACE=eno1
```

## Compute node
新增local.conf
```conf
[[local|localrc]]
SERVICE_HOST=192.168.2.95
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
disable_service etcd3

# Neutron options
NEUTRON_CREATE_INITIAL_NETWORKS=False
MULTI_HOST=1

#---------------compute node common section
ENABLED_SERVICES=n-cpu,q-agt,n-api-meta,placement-client,n-novnc
NOVA_VNC_ENABLED=True
NOVNCPROXY_URL="http://$SERVICE_HOST:6080/vnc_auto.html"


#---------------compute node special section
HOST_IP=192.168.2.98
PUBLIC_INTERFACE=eno1
FLAT_INTERFACE=ens3
VNCSERVER_PROXYCLIENT_ADDRESS=$HOST_IP
VNCSERVER_LISTEN=$HOST_IP

MULTI_HOST=1
```

## 註冊VIM
```shell
$ vim vim_config.yaml
auth_url: 'http://192.168.2.95/identity'
username: 'admin'
password: 'password'
project_name: 'admin'
project_domain_name: 'Default'
user_domain_name: 'Default'
cert_verify: 'False'

$ openstack vim register --config-file vim_config.yaml --description 'my first vim' --is-default hellovim
```
## 啟動VNF
> 需確認Public,Subnet IP沒被使用過
```yaml
$ vim tosca-vnffg-vnfd1.yaml
tosca_definitions_version: tosca_simple_profile_for_nfv_1_0_0

description: Demo example

metadata:
  template_name: sample-tosca-vnfd1

topology_template:
  node_templates:
    VDU1:
      type: tosca.nodes.nfv.VDU.Tacker
      properties:
        image: ubuntu
        flavor: test
        availability_zone: nova
        mgmt_driver: noop
        key_name: Titan
        config: |
          param0: key1
          param1: key2
        user_data_format: RAW
        user_data: |
          #!/bin/sh
          echo 1 > /proc/sys/net/ipv4/ip_forward
    CP11:
      type: tosca.nodes.nfv.CP.Tacker
      properties:
        management: true
        order: 0
        anti_spoofing_protection: false
        ip_address: 10.10.0.11
      requirements:
        - virtualLink:
            node: VL11
        - virtualBinding:
            node: VDU1

    VL11:
      type: tosca.nodes.nfv.VL
      properties:
        network_name: net_mgmt
        vendor: Tacker

    FIP1:
      type: tosca.nodes.network.FloatingIP
      properties:
        floating_network: public
        floating_ip_address: 192.168.2.111
      requirements:
        - link:
            node: CP11

$ openstack vnf descriptor create --vnfd-file tosca-vnffg-vnfd1.yaml vnfd1
$ openstack vnf create --vnfd-name vnfd1 vnf1_001
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