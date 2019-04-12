# kuryr-kubernetes
# controller node
## 安裝 kuryr-k8s-controller 在 virtualenv:
```
$ sudo apt install -y python-pip
$ sudo apt install -y virtualenv
$ mkdir kuryr-k8s-controller
$ cd kuryr-k8s-controller
$ virtualenv env
# 建議master
$ git clone https://git.openstack.org/openstack/kuryr-kubernetes -b stable/rocky
$ . env/bin/activate
$ pip install -e kuryr-kubernetes
$ cd kuryr-kubernetes
$ ./tools/generate_config_file_samples.sh
$ sudo mkdir /etc/kuryr/
$ sudo cp etc/kuryr.conf.sample /etc/kuryr/kuryr.conf
```
編輯配置檔/etc/kuryr/kuryr.conf
```
$ sudo vim /etc/kuryr/kuryr.conf
[DEFAULT]
use_stderr = true
bindir = /opt/stack/kuryr-k8s-controller/env/libexec/kuryr
[kubernetes]
api_root = https://10.0.1.98:6443
ssl_ca_crt_file = /etc/kubernetes/pki/ca.crt
token_file = /home/ubuntu/token
[neutron]
auth_url = http://10.0.1.98/identity
username = admin
user_domain_name = Default
password = password(ADMIN_PASS)
project_name = admin
project_domain_name = Default
auth_type = password
[neutron_defaults]
ovs_bridge = br-int
pod_security_groups = 5c0ddafd-1c06-4207-adbd-2e72d73cc810
pod_subnet = 5b03e5b7-d331-41e5-94e5-eee95ca0892b
project = 37ea8f533f6b4287a4a9bdd73a249404
service_subnet = 91322fae-b300-486d-8572-e4c8eef5d177
```

## 建立k8s sa
```
$ kubectl create sa titan-sa

$ kubectl get sa titan-sa
NAME       SECRETS   AGE
titan-sa   1         25m

$ kubectl describe sa titan-sa
Name:                titan-sa
Namespace:           default
Labels:              <none>
Annotations:         <none>
Image pull secrets:  <none>
Mountable secrets:   titan-sa-token-89g4x
Tokens:              titan-sa-token-89g4x
Events:              <none>

取得token
$ kubectl describe secret titan-sa-token-89g4x
Name:         titan-sa-token-89g4x
Namespace:    default
Labels:       <none>
Annotations:  kubernetes.io/service-account.name: titan-sa
              kubernetes.io/service-account.uid: 3ce87728-1ed2-11e9-b05b-14cc200079d0

Type:  kubernetes.io/service-account-token

Data
====
namespace:  7 bytes
token:      eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6InRpdGFuLXNhLXRva2VuLTg5ZzR4Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6InRpdGFuLXNhIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiM2NlODc3MjgtMWVkMi0xMWU5LWIwNWItMTRjYzIwMDA3OWQwIiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50OmRlZmF1bHQ6dGl0YW4tc2EifQ.kJUWJQJEB84lLMHyboRJAufgTXiYvBCMTocffXJcN0nKrZQ3828BOUbzjWuzYJ-5KEq-I2fSP8ZJ_R-zTxc37df6hinb2lBWaxJyTeOrYOo99MoGDhaWRgr-HhpLwMpoSNtTFv7aq6Nbs2X4vEbN1NPN_s1sjZysMnIh_RuCuWrdvW-UmIshYTp-uAnzUluDHPhDpVNLlsgZQItuhGPsCEBfBq_Y6D0g5clPQwh3i6ic9hwC0WcOmRRas8UdZ3Ti2lFKP98vgP7YnXOQxGNtNC8UaLTnyQFTh7KpsybriEj1So0XFvjyyZoB_vEb8SA6byBNP68ctn_XgWXov_W5yg
ca.crt:     1025 bytes

# 新增token file
$ vim /home/ubuntu/token

$ kubectl get secret titan-sa-token-89g4x
NAME                   TYPE                                  DATA   AGE
titan-sa-token-89g4x   kubernetes.io/service-account-token   3      27m
```
## 給予權限
```
$ kubectl create clusterrolebinding titan-binding --serviceaccount=default:titan-sa --clusterrole=cluster-admin

$ kubectl get clusterrolebinding | grep titan

$ kubectl delete clusterrolebinding  titan-binding
```

## 建立網路
1. 建立一個k8s project
2. 建立一個k8s user(目前使用admin)
3. 建立pod network ，kuryr建議子網設定是10.1.0.0/16,Gateway:10.1.255.254(可使用Web Dashboard建立，可開DHCP)
```
$ openstack network create --project admin pod
+---------------------------+--------------------------------------+
| Field                     | Value                                |
+---------------------------+--------------------------------------+
| admin_state_up            | UP                                   |
| availability_zone_hints   |                                      |
| availability_zones        |                                      |
| created_at                | 2019-03-15T06:29:36Z                 |
| description               |                                      |
| dns_domain                | None                                 |
| id                        | dec4f114-ac43-42bb-be25-8afb4f01397e |
| ipv4_address_scope        | None                                 |
| ipv6_address_scope        | None                                 |
| is_default                | False                                |
| is_vlan_transparent       | None                                 |
| mtu                       | 1450                                 |
| name                      | pod                                  |
| port_security_enabled     | True                                 |
| project_id                | 77622b1a98e14737a4f1563aa0531c1e     |
| provider:network_type     | vxlan                                |
| provider:physical_network | None                                 |
| provider:segmentation_id  | 28                                   |
| qos_policy_id             | None                                 |
| revision_number           | 1                                    |
| router:external           | Internal                             |
| segments                  | None                                 |
| shared                    | False                                |
| status                    | ACTIVE                               |
| subnets                   |                                      |
| tags                      |                                      |
| updated_at                | 2019-03-15T06:29:37Z                 |
+---------------------------+--------------------------------------+

$ openstack subnet create --project admin --network pod --no-dhcp --gateway 10.1.255.254 --subnet-range 10.1.0.0/16 pod_subnet
+-------------------+--------------------------------------+
| Field             | Value                                |
+-------------------+--------------------------------------+
| allocation_pools  | 10.1.0.1-10.1.255.253                |
| cidr              | 10.1.0.0/16                          |
| created_at        | 2019-03-15T06:34:05Z                 |
| description       |                                      |
| dns_nameservers   |                                      |
| enable_dhcp       | False                                |
| gateway_ip        | 10.1.255.254                         |
| host_routes       |                                      |
| id                | 3ae27db6-a995-4950-b3e0-059a72a2206f |
| ip_version        | 4                                    |
| ipv6_address_mode | None                                 |
| ipv6_ra_mode      | None                                 |
| name              | pod_subnet                           |
| network_id        | dec4f114-ac43-42bb-be25-8afb4f01397e |
| project_id        | 77622b1a98e14737a4f1563aa0531c1e     |
| revision_number   | 0                                    |
| segment_id        | None                                 |
| service_types     |                                      |
| subnetpool_id     | None                                 |
| tags              |                                      |
| updated_at        | 2019-03-15T06:34:05Z                 |
+-------------------+--------------------------------------+
```
4. 建立service network ，kuryr建議子網設定是10.2.0.0/16,Gateway:10.2.255.254
                        subnet pool只給10.2.128.1~10.2.255.253，前半留給loadbalancer(可使用Web Dashboard建立，可開DHCP)
```
$ openstack network create --project admin services
+---------------------------+--------------------------------------+
| Field                     | Value                                |
+---------------------------+--------------------------------------+
| admin_state_up            | UP                                   |
| availability_zone_hints   |                                      |
| availability_zones        |                                      |
| created_at                | 2019-03-15T06:35:43Z                 |
| description               |                                      |
| dns_domain                | None                                 |
| id                        | fe214a02-9bcb-40ea-be84-04d68f93f4d2 |
| ipv4_address_scope        | None                                 |
| ipv6_address_scope        | None                                 |
| is_default                | False                                |
| is_vlan_transparent       | None                                 |
| mtu                       | 1450                                 |
| name                      | services                             |
| port_security_enabled     | True                                 |
| project_id                | 77622b1a98e14737a4f1563aa0531c1e     |
| provider:network_type     | vxlan                                |
| provider:physical_network | None                                 |
| provider:segmentation_id  | 50                                   |
| qos_policy_id             | None                                 |
| revision_number           | 1                                    |
| router:external           | Internal                             |
| segments                  | None                                 |
| shared                    | False                                |
| status                    | ACTIVE                               |
| subnets                   |                                      |
| tags                      |                                      |
| updated_at                | 2019-03-15T06:35:43Z                 |
+---------------------------+--------------------------------------+

$ openstack subnet create --project admin --network services --no-dhcp --gateway 10.2.255.254 --ip-version 4 --allocation-pool start=10.2.128.1,end=10.2.255.253 --subnet-range 10.2.0.0/16 services_subnet
+-------------------+--------------------------------------+
| Field             | Value                                |
+-------------------+--------------------------------------+
| allocation_pools  | 10.2.128.1-10.2.255.253              |
| cidr              | 10.2.0.0/16                          |
| created_at        | 2019-03-15T06:39:20Z                 |
| description       |                                      |
| dns_nameservers   |                                      |
| enable_dhcp       | False                                |
| gateway_ip        | 10.2.255.254                         |
| host_routes       |                                      |
| id                | c3e52567-5202-4396-954b-806ce64094ed |
| ip_version        | 4                                    |
| ipv6_address_mode | None                                 |
| ipv6_ra_mode      | None                                 |
| name              | services_subnet                      |
| network_id        | fe214a02-9bcb-40ea-be84-04d68f93f4d2 |
| project_id        | 77622b1a98e14737a4f1563aa0531c1e     |
| revision_number   | 0                                    |
| segment_id        | None                                 |
| service_types     |                                      |
| subnetpool_id     | None                                 |
| tags              |                                      |
| updated_at        | 2019-03-15T06:39:20Z                 |
+-------------------+--------------------------------------+
```
5. 建立一個router，把pod subnet和service subnet的Gateway都連起來(可使用Web Dashboard建立，可開DHCP)
> 可連接public network方便之後測試使用
```
$ openstack router create --project admin kuryr-kubernetes
+-------------------------+--------------------------------------+
| Field                   | Value                                |
+-------------------------+--------------------------------------+
| admin_state_up          | UP                                   |
| availability_zone_hints |                                      |
| availability_zones      |                                      |
| created_at              | 2019-03-15T06:40:28Z                 |
| description             |                                      |
| distributed             | False                                |
| external_gateway_info   | None                                 |
| flavor_id               | None                                 |
| ha                      | False                                |
| id                      | 381f6aa1-6296-49b9-be56-d3bb12b129e1 |
| name                    | kuryr-kubernetes                     |
| project_id              | 77622b1a98e14737a4f1563aa0531c1e     |
| revision_number         | 0                                    |
| routes                  |                                      |
| status                  | ACTIVE                               |
| tags                    |                                      |
| updated_at              | 2019-03-15T06:40:28Z                 |
+-------------------------+--------------------------------------+

$ openstack port create --project admin --network pod --fixed-ip ip-address=10.1.255.254 pod_subnet_router
+-----------------------+-----------------------------------------------------------------------------+
| Field                 | Value                                                                       |
+-----------------------+-----------------------------------------------------------------------------+
| admin_state_up        | UP                                                                          |
| allowed_address_pairs |                                                                             |
| binding_host_id       |                                                                             |
| binding_profile       |                                                                             |
| binding_vif_details   |                                                                             |
| binding_vif_type      | unbound                                                                     |
| binding_vnic_type     | normal                                                                      |
| created_at            | 2019-03-15T06:43:02Z                                                        |
| data_plane_status     | None                                                                        |
| description           |                                                                             |
| device_id             |                                                                             |
| device_owner          |                                                                             |
| dns_assignment        | None                                                                        |
| dns_domain            | None                                                                        |
| dns_name              | None                                                                        |
| extra_dhcp_opts       |                                                                             |
| fixed_ips             | ip_address='10.1.255.254', subnet_id='3ae27db6-a995-4950-b3e0-059a72a2206f' |
| id                    | fef7854d-50bb-4055-a786-0b4188ae9a63                                        |
| mac_address           | fa:16:3e:d6:6d:86                                                           |
| name                  | pod_subnet_router                                                           |
| network_id            | dec4f114-ac43-42bb-be25-8afb4f01397e                                        |
| port_security_enabled | True                                                                        |
| project_id            | 77622b1a98e14737a4f1563aa0531c1e                                            |
| qos_policy_id         | None                                                                        |
| revision_number       | 1                                                                           |
| security_group_ids    | aa2d8db2-fea0-4bfe-a8cb-3aac52943b51                                        |
| status                | DOWN                                                                        |
| tags                  |                                                                             |
| trunk_details         | None                                                                        |
| updated_at            | 2019-03-15T06:43:02Z                                                        |
+-----------------------+-----------------------------------------------------------------------------+

$ openstack port create --project admin --network services --fixed-ip ip-address=10.2.255.254 service_subnet_router
+-----------------------+-----------------------------------------------------------------------------+
| Field                 | Value                                                                       |
+-----------------------+-----------------------------------------------------------------------------+
| admin_state_up        | UP                                                                          |
| allowed_address_pairs |                                                                             |
| binding_host_id       |                                                                             |
| binding_profile       |                                                                             |
| binding_vif_details   |                                                                             |
| binding_vif_type      | unbound                                                                     |
| binding_vnic_type     | normal                                                                      |
| created_at            | 2019-03-15T06:44:54Z                                                        |
| data_plane_status     | None                                                                        |
| description           |                                                                             |
| device_id             |                                                                             |
| device_owner          |                                                                             |
| dns_assignment        | None                                                                        |
| dns_domain            | None                                                                        |
| dns_name              | None                                                                        |
| extra_dhcp_opts       |                                                                             |
| fixed_ips             | ip_address='10.2.255.254', subnet_id='c3e52567-5202-4396-954b-806ce64094ed' |
| id                    | c35b99b5-9737-4e02-91fc-0945dac7188d                                        |
| mac_address           | fa:16:3e:64:20:e3                                                           |
| name                  | service_subnet_router                                                       |
| network_id            | fe214a02-9bcb-40ea-be84-04d68f93f4d2                                        |
| port_security_enabled | True                                                                        |
| project_id            | 77622b1a98e14737a4f1563aa0531c1e                                            |
| qos_policy_id         | None                                                                        |
| revision_number       | 1                                                                           |
| security_group_ids    | aa2d8db2-fea0-4bfe-a8cb-3aac52943b51                                        |
| status                | DOWN                                                                        |
| tags                  |                                                                             |
| trunk_details         | None                                                                        |
| updated_at            | 2019-03-15T06:44:54Z                                                        |
+-----------------------+-----------------------------------------------------------------------------+

$ openstack router add port 381f6aa1-6296-49b9-be56-d3bb12b129e1 fef7854d-50bb-4055-a786-0b4188ae9a63

$ openstack router add port 381f6aa1-6296-49b9-be56-d3bb12b129e1 c35b99b5-9737-4e02-91fc-0945dac7188d

編輯
[neutron_defaults]
ovs_bridge = br-int
pod_subnet = 3ae27db6-a995-4950-b3e0-059a72a2206f
service_subnet = c3e52567-5202-4396-954b-806ce64094ed
```
6. 建立一個security group，允許來自pod network和service network的所有TCP(目前使用admin default)
> 可開啟ICMP、TCP、UDP(Egress和Ingress)
```
# 可使用Web Dashboard建立
$ openstack security group create --project admin service_pod_access_sg
+-----------------+-------------------------------------------------------------------------------------------------------------------------------------------------------+
| Field           | Value                                                                                                                                                 |
+-----------------+-------------------------------------------------------------------------------------------------------------------------------------------------------+
| created_at      | 2019-03-15T06:56:18Z                                                                                                                                  |
| description     | service_pod_access_sg                                                                                                                                 |
| id              | 57a4f2cc-028f-4f70-a28a-7d179a0e66b0                                                                                                                  |
| name            | service_pod_access_sg                                                                                                                                 |
| project_id      | 77622b1a98e14737a4f1563aa0531c1e                                                                                                                      |
| revision_number | 1                                                                                                                                                     |
| rules           | created_at='2019-03-15T06:56:18Z', direction='egress', ethertype='IPv4', id='044bad18-c501-4a12-877e-81dc6d79b70f', updated_at='2019-03-15T06:56:18Z' |
|                 | created_at='2019-03-15T06:56:18Z', direction='egress', ethertype='IPv6', id='81a4ffdc-1f91-45a9-8db2-d6bf93467fe3', updated_at='2019-03-15T06:56:18Z' |
| tags            | []                                                                                                                                                    |
| updated_at      | 2019-03-15T06:56:18Z                                                                                                                                  |
+-----------------+-------------------------------------------------------------------------------------------------------------------------------------------------------+

# 需執行，目前使用default
$ openstack security group rule create --project admin --remote-ip 10.2.0.0/16 --ethertype IPv4 --protocol tcp service_pod_access_sg
+-------------------+--------------------------------------+
| Field             | Value                                |
+-------------------+--------------------------------------+
| created_at        | 2019-03-15T06:59:50Z                 |
| description       |                                      |
| direction         | ingress                              |
| ether_type        | IPv4                                 |
| id                | 24ae52e9-14f5-4275-b5a2-e8882b526b55 |
| name              | None                                 |
| port_range_max    | None                                 |
| port_range_min    | None                                 |
| project_id        | 77622b1a98e14737a4f1563aa0531c1e     |
| protocol          | tcp                                  |
| remote_group_id   | None                                 |
| remote_ip_prefix  | 10.2.0.0/16                          |
| revision_number   | 0                                    |
| security_group_id | 57a4f2cc-028f-4f70-a28a-7d179a0e66b0 |
| updated_at        | 2019-03-15T06:59:50Z                 |
+-------------------+--------------------------------------+

編輯
[neutron_defaults]
ovs_bridge = br-int
pod_security_groups = 57a4f2cc-028f-4f70-a28a-7d179a0e66b0
```

## 建立loadbalancer
```
$ openstack loadbalancer create --project admin --vip-address 10.2.0.1 --vip-subnet-id d33f310d-c40c-443c-9063-87c9a48bbe86 --name default/kubernetes
+---------------------+--------------------------------------+
| Field               | Value                                |
+---------------------+--------------------------------------+
| admin_state_up      | True                                 |
| created_at          | 2019-03-20T18:15:35                  |
| description         |                                      |
| flavor_id           | None                                 |
| id                  | b99bb41f-a312-46a9-882e-fb015a5f2686 |
| listeners           |                                      |
| name                | default/kubernetes                   |
| operating_status    | OFFLINE                              |
| pools               |                                      |
| project_id          | 87b84e4bc98d4317a91b03da48a06d45     |
| provider            | amphora                              |
| provisioning_status | PENDING_CREATE                       |
| updated_at          | None                                 |
| vip_address         | 10.2.0.1                             |
| vip_network_id      | 2d5c54f4-f7b2-4c60-9e3b-f13c971f37ed |
| vip_port_id         | 15b13c4c-4254-4bb9-979e-519338cab288 |
| vip_qos_policy_id   | None                                 |
| vip_subnet_id       | d33f310d-c40c-443c-9063-87c9a48bbe86 |
+---------------------+--------------------------------------+
```

> 需等待loadbalancer ACTIVE
![loadbalancer ACTIVE](https://github.com/TitanLi/OpenStack/blob/master/kuryr/picture/loadbalancer-create.png)

```
$ openstack loadbalancer pool create --name default/kubernetes:HTTPS:443 --protocol HTTPS --lb-algorithm LEAST_CONNECTIONS --loadbalancer b99bb41f-a312-46a9-882e-fb015a5f2686
+----------------------+--------------------------------------+
| Field                | Value                                |
+----------------------+--------------------------------------+
| admin_state_up       | True                                 |
| created_at           | 2019-03-20T18:18:54                  |
| description          |                                      |
| healthmonitor_id     |                                      |
| id                   | 347226d2-7538-4fb8-872a-c1fef52ca15e |
| lb_algorithm         | LEAST_CONNECTIONS                    |
| listeners            |                                      |
| loadbalancers        | b99bb41f-a312-46a9-882e-fb015a5f2686 |
| members              |                                      |
| name                 | default/kubernetes:HTTPS:443         |
| operating_status     | OFFLINE                              |
| project_id           | 87b84e4bc98d4317a91b03da48a06d45     |
| protocol             | HTTPS                                |
| provisioning_status  | PENDING_CREATE                       |
| session_persistence  | None                                 |
| updated_at           | None                                 |
| tls_container_ref    | None                                 |
| ca_tls_container_ref | None                                 |
| crl_container_ref    | None                                 |
| tls_enabled          | False                                |
+----------------------+--------------------------------------+

$ openstack loadbalancer member create --name titan4 --address 192.168.0.2 --protocol-port 6443 347226d2-7538-4fb8-872a-c1fef52ca15e
+---------------------+--------------------------------------+
| Field               | Value                                |
+---------------------+--------------------------------------+
| address             | 192.168.0.2                          |
| admin_state_up      | True                                 |
| created_at          | 2019-03-20T18:19:30                  |
| id                  | d61e1b22-8fae-4283-90ed-16de62637c4e |
| name                | kuryr-k8s-master                     |
| operating_status    | NO_MONITOR                           |
| project_id          | 87b84e4bc98d4317a91b03da48a06d45     |
| protocol_port       | 6443                                 |
| provisioning_status | PENDING_CREATE                       |
| subnet_id           | None                                 |
| updated_at          | None                                 |
| weight              | 1                                    |
| monitor_port        | None                                 |
| monitor_address     | None                                 |
| backup              | False                                |
+---------------------+--------------------------------------+

$ openstack loadbalancer listener create --name default/kubernetes:HTTPS:443 --protocol HTTPS --default-pool 347226d2-7538-4fb8-872a-c1fef52ca15e --protocol-port 443 b99bb41f-a312-46a9-882e-fb015a5f2686
+-----------------------------+--------------------------------------+
| Field                       | Value                                |
+-----------------------------+--------------------------------------+
| admin_state_up              | True                                 |
| connection_limit            | -1                                   |
| created_at                  | 2019-03-20T18:21:06                  |
| default_pool_id             | 347226d2-7538-4fb8-872a-c1fef52ca15e |
| default_tls_container_ref   | None                                 |
| description                 |                                      |
| id                          | 9be6dc55-d9d2-4d78-b57d-3e99ae496cd7 |
| insert_headers              | None                                 |
| l7policies                  |                                      |
| loadbalancers               | b99bb41f-a312-46a9-882e-fb015a5f2686 |
| name                        | default/kubernetes:HTTPS:443         |
| operating_status            | OFFLINE                              |
| project_id                  | 87b84e4bc98d4317a91b03da48a06d45     |
| protocol                    | HTTPS                                |
| protocol_port               | 443                                  |
| provisioning_status         | PENDING_CREATE                       |
| sni_container_refs          | []                                   |
| timeout_client_data         | 50000                                |
| timeout_member_connect      | 5000                                 |
| timeout_member_data         | 50000                                |
| timeout_tcp_inspect         | 0                                    |
| updated_at                  | 2019-03-20T18:21:06                  |
| client_ca_tls_container_ref | None                                 |
| client_authentication       | NONE                                 |
| client_crl_container_ref    | None                                 |
+-----------------------------+--------------------------------------+
```
## 編輯配置檔/etc/kuryr/kuryr.conf(controller node)

```conf
$ sudo vim /etc/kuryr/kuryr.conf
[DEFAULT]
use_stderr = true
bindir = /opt/stack/kuryr-k8s-controller/env/libexec/kuryr
[kubernetes]
api_root = https://10.0.1.97:6443
ssl_ca_crt_file = /etc/kubernetes/pki/ca.crt
token_file = /home/ubuntu/token
[neutron]
auth_url = http://10.0.1.97/identity
username = admin
user_domain_name = Default
# password = ADMIN_PASS
password = password
project_name = admin
project_domain_name = Default
auth_type = password
[neutron_defaults]
ovs_bridge = br-int
pod_security_groups = 318cc711-0698-42eb-8008-18753a2d0ffc
pod_subnet = 6485ffa3-c391-4994-98e5-2f2cda42bed0 
project = 5780affc22444315af6a424d8c92b9d4
service_subnet = 42b0e3fd-6f7b-4681-ab35-d29f517964e9
```
## 運行kuryr-k8s-controller
```
$ kuryr-k8s-controller --config-file /etc/kuryr/kuryr.conf -d
```
> 完成狀態
> 需等待loadbalancer ACTIVE
![loadbalancer ACTIVE](https://github.com/TitanLi/OpenStack/blob/master/kuryr/picture/loadbalancer-listener-create.png)

![Network-Topology.png](https://github.com/TitanLi/OpenStack/blob/master/kuryr/picture/Network-Topology.png)

---
# kubernetes node
## kuryr-cni
> kuryr-cni路徑：/opt/stack/kuryr-k8s-controller/env/local/bin
## 安裝配置kuryr-CNI在k8s node
```
$ sudo apt install -y python-pip
$ sudo apt install -y virtualenv
$ mkdir kuryr-k8s-cni
$ cd kuryr-k8s-cni
$ virtualenv env
$ . env/bin/activate
# 建議master
$ git clone https://git.openstack.org/openstack/kuryr-kubernetes -b stable/rocky
$ pip install -e kuryr-kubernetes
```
## 建立配置檔(k8s node)
```
$ cd kuryr-kubernetes
# 可不用執行
# $ ./tools/generate_config_file_samples.sh
$ sudo mkdir -p /etc/kuryr/
# $ sudo cp etc/kuryr.conf.sample /etc/kuryr/kuryr.conf
```
## 編輯配置檔/etc/kuryr/kuryr.conf(k8s node)
```
[DEFAULT]
use_stderr = true
bindir = /opt/stack/kuryr-k8s-cni/env/libexec/kuryr
lock_path = /opt/stack/kuryr-k8s-cni/env/local/bin
[kubernetes]
api_root = https://10.0.1.97:6443
#ssl_ca_crt_file = /home/ubuntu/ca.crt
ssl_ca_crt_file = /etc/kubernetes/pki/ca.crt
token_file = /home/ubuntu/token
```
## 複製/etc/kubernetes/pki/ca.crt至Kuryr-cni node：
kuryr-cni node
```
$ sudo su
$ mkdir -p /etc/kubernetes/pki/

# 建立kubernetes token
$ vim /home/ubuntu/token
```
kubernetes master
```
$ sudo su
$ scp /etc/kubernetes/pki/ca.crt root@10.0.1.12:/etc/kubernetes/pki/ca.crt
```
## 將CNI二進製文件鏈接到CNI目錄，其中kubelet會找到它(k8s node)：
```
$ cd /opt/stack/kuryr-k8s-cni/env/local/bin
$ sudo ln -s $(which kuryr-cni) /opt/cni/bin/
$ sudo chmod +x /opt/cni/bin/kuryr-cni
```
## 創建/etc/cni/net.d/10-kuryr.conf
```
新增
{
  "cniVersion": "0.3.1",
  "name": "kuryr",
  "type": "kuryr-cni",
  "kuryr_conf": "/etc/kuryr/kuryr.conf",
  "debug": true
}
或者
$ cp kuryr-kubernetes/etc/cni/net.d/10-kuryr.conf /etc/cni/net.d
```
## 讓10-kuryr.conf為目錄第一個檔案
```
$ cd /etc/cni/net.d/
# 更新元CNI檔案名稱，讓kuryr-cni可在第一個位子
$ sudo mv 10-flannel.conflist 20-flannel.conflist 
$ ls /etc/cni/net.d/
10-kuryr.conf  20-flannel.conflist
```
## nstall os-vif and oslo.privsep libraries
```
$ deactivate
$ sudo pip install 'oslo.privsep>=1.20.0' 'os-vif>=1.5.0'
$ . env/bin/activate
```
## 使用sudo權限執行
```
$ sudo su
$ cd /opt/stack/kuryr-k8s-cni/
$ . env/bin/activate
$ . /opt/stack/admin-openrc
$ cd kuryr-kubernetes
$ kuryr-daemon --config-file /etc/kuryr/kuryr.conf -d
```
---
# 測試
## Run Pod (kubernetes master)
```
$ vim myapp.yaml
新增以下內容
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
  labels:
    app: myapp
spec:
  containers:
  - name: myapp-container
    image: busybox
    command: ['sh', '-c', 'echo The app is running! && sleep 3600']

$ kubectl apply -f myapp.yaml
pod/myapp-pod created

$ kubectl get pod
NAME        READY   STATUS    RESTARTS   AGE
myapp-pod   1/1     Running   0          18s
```

# 進入Kubernetes Pod ping OpenStack Instances
```shell
$ kubectl exec -ti myapp-pod sh
/ # ping 10.2.128.24
PING 10.2.128.24 (10.2.128.24): 56 data bytes
64 bytes from 10.2.128.24: seq=0 ttl=63 time=2.035 ms
64 bytes from 10.2.128.24: seq=1 ttl=63 time=2.098 ms
64 bytes from 10.2.128.24: seq=2 ttl=63 time=1.542 ms
64 bytes from 10.2.128.24: seq=3 ttl=63 time=1.882 ms

/ # ifconfig
eth0      Link encap:Ethernet  HWaddr FA:16:3E:82:07:69  
          inet addr:10.1.0.5  Bcast:0.0.0.0  Mask:255.255.0.0
          UP BROADCAST RUNNING  MTU:1450  Metric:1
          RX packets:14 errors:0 dropped:0 overruns:0 frame:0
          TX packets:6 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:1124 (1.0 KiB)  TX bytes:476 (476.0 B)

lo        Link encap:Local Loopback  
          inet addr:127.0.0.1  Mask:255.0.0.0
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1 
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)
```

# 進入OpenStack Instances ping Kubernetes Pod
```shell
$ ping 10.1.0.5
PING 10.1.0.5 (10.1.0.5): 56 data bytes
64 bytes from 10.1.0.5: seq=0 ttl=63 time=2.196 ms
64 bytes from 10.1.0.5: seq=1 ttl=63 time=1.996 ms
64 bytes from 10.1.0.5: seq=2 ttl=63 time=1.491 ms
64 bytes from 10.1.0.5: seq=3 ttl=63 time=1.736 ms

$ ifconfig
eth0      Link encap:Ethernet  HWaddr FA:16:3E:D6:C4:14  
          inet addr:10.2.128.24  Bcast:10.2.255.255  Mask:255.255.0.0
          inet6 addr: fe80::f816:3eff:fed6:c414/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1450  Metric:1
          RX packets:328 errors:0 dropped:0 overruns:0 frame:0
          TX packets:262 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:34931 (34.1 KiB)  TX bytes:30866 (30.1 KiB)

lo        Link encap:Local Loopback  
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:16436  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0 
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)
```
恭喜成功啦
---
# 常用指令
## SSH into Amphorae
```
$ ssh -i /etc/octavia/.ssh/octavia_ssh_key ubuntu@[lb_network_ip]
```
## Generating a List of Amphorae to Rotate¶
```
$ openstack server list --name amphora* --all -c ID -c Status -c Networks
```

## 問題解決
### 問題一:
#### 問題:
```
ERROR kuryr_kubernetes.handlers.retry [-] Report handler unhealthy LoadBalancerHandler: Forbidden: 403-{u'debuginfo': None, u'faultcode': u'Client', u'faultstring': u'Policy does not allow this request to be performed.'}
Neutron server returns request_ids: ['req-ce0fc9b6-f1c1-4899-abd2-e43085dd21cc']
```
#### 解決方法:
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
```
### 問題二:
#### 問題:
```
$ kubectl get pod
The connection to the server 10.0.1.98:6443 was refused - did you specify the right host or port?

$ systemctl status kubelet
● kubelet.service - kubelet: The Kubernetes Node Agent
   Loaded: loaded (/lib/systemd/system/kubelet.service; enabled; vendor preset: enabled)
  Drop-In: /etc/systemd/system/kubelet.service.d
           └─10-kubeadm.conf
   Active: activating (auto-restart) (Result: exit-code) since Wed 2019-03-20 18:41:13 UTC; 9s ago
     Docs: https://kubernetes.io/docs/home/
  Process: 22477 ExecStart=/usr/bin/kubelet $KUBELET_KUBECONFIG_ARGS $KUBELET_CONFIG_ARGS $KUBELET_KUBEADM_ARGS $KUBELET_EXTRA_ARG
 Main PID: 22477 (code=exited, status=255)

Mar 20 18:41:13 titan2 systemd[1]: kubelet.service: Unit entered failed state.
Mar 20 18:41:13 titan2 systemd[1]: kubelet.service: Failed with result 'exit-code'.

root@titan2:/home/ubuntu# systemctl restart kubelet
root@titan2:/home/ubuntu# systemctl status kubelet
● kubelet.service - kubelet: The Kubernetes Node Agent
   Loaded: loaded (/lib/systemd/system/kubelet.service; enabled; vendor preset: enabled)
  Drop-In: /etc/systemd/system/kubelet.service.d
           └─10-kubeadm.conf
   Active: activating (auto-restart) (Result: exit-code) since Wed 2019-03-20 18:41:43 UTC; 2s ago
     Docs: https://kubernetes.io/docs/home/
  Process: 22584 ExecStart=/usr/bin/kubelet $KUBELET_KUBECONFIG_ARGS $KUBELET_CONFIG_ARGS $KUBELET_KUBEADM_ARGS $KUBELET_EXTRA_ARG
 Main PID: 22584 (code=exited, status=255)

Mar 20 18:41:43 titan2 systemd[1]: kubelet.service: Unit entered failed state.
Mar 20 18:41:43 titan2 systemd[1]: kubelet.service: Failed with result 'exit-code'.
```
#### 解決方法:
```
$ sudo swapon -s
Filename				Type		Size	Used	Priority
/swap.img                              	file    	4194300	0	-1

$ swapoff -a

$ free
              total        used        free      shared  buff/cache   available
Mem:       16179168      773704    14195124       58524     1210340    14995916
Swap:             0           0           0

$ sudo systemctl status kubelet
● kubelet.service - kubelet: The Kubernetes Node Agent
   Loaded: loaded (/lib/systemd/system/kubelet.service; enabled; vendor preset: enabled)
  Drop-In: /etc/systemd/system/kubelet.service.d
           └─10-kubeadm.conf
   Active: active (running) since Wed 2019-03-20 18:43:56 UTC; 57s ago
     Docs: https://kubernetes.io/docs/home/
 Main PID: 23044 (kubelet)
    Tasks: 30
   Memory: 44.7M
      CPU: 4.584s
   CGroup: /system.slice/kubelet.service
           └─23044 /usr/bin/kubelet --bootstrap-kubeconfig=/etc/kubernetes/bootstrap-kubelet.conf --kubeconfig=/etc/kubernetes/kub
```