# kuryr-kubernetes
## 安裝 kuryr-k8s-controller 在 virtualenv:
```
$ sudo apt install -y python-pip
$ sudo apt install -y virtualenv
$ mkdir kuryr-k8s-controller
$ cd kuryr-k8s-controller
$ virtualenv env
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
bindir = /home/ubuntu/kuryr-k8s-controller/env/libexec/kuryr
[kubernetes]
api_root = https://10.0.1.98:6443
ssl_ca_crt_file = /etc/kubernetes/pki/ca.crt
token_file = /home/ubuntu/token
[neutron]
auth_url = http://10.0.1.98:5000/v3
username = admin
user_domain_name = Default
password = ADMIN_PASS
project_name = admin
project_domain_name = Default
auth_type = password
[neutron_defaults]
vs_bridge = br-int
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
3. 建立pod network ，kuryr建議子網設定是10.1.0.0/16,Gateway:10.1.255.254
```
$ openstack network create --project kuryrk8s pod
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

$ openstack subnet create --project kuryrk8s --network dec4f114-ac43-42bb-be25-8afb4f01397e --no-dhcp --gateway 10.1.255.254 --subnet-range 10.1.0.0/16 pod_subnet
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
                        subnet pool只給10.2.128.1~10.2.255.253，前半留給loadbalancer
```
$ openstack network create --project kuryrk8s services
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

$ openstack subnet create --project kuryrk8s --network services --no-dhcp --gateway 10.2.255.254 --ip-version 4 --allocation-pool start=10.2.128.1,end=10.2.255.253 --subnet-range 10.2.0.0/16 services_subnet
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
5. 建立一個router，把pod subnet和service subnet的Gateway都連起來
```
$ openstack router create --project kuryrk8s kuryr-kubernetes
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

$ openstack port create --project kuryrk8s --network dec4f114-ac43-42bb-be25-8afb4f01397e --fixed-ip ip-address=10.1.255.254 pod_subnet_router
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

$ openstack port create --project kuryrk8s --network services --fixed-ip ip-address=10.2.255.254 service_subnet_router
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
6. 建立一個security group，允許來自pod network和service network的所有TCP
```
$ openstack security group create --project kuryrk8s service_pod_access_sg
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

$ openstack security group rule create --project kuryrk8s --remote-ip 10.2.0.0/16 --ethertype IPv4 --protocol tcp service_pod_access_sg
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
pod_security_groups = f0b6f0bd-40f7-4ab6-a77b-3cf9f7cc28ac
```

## 建立loadbalancer
```
$ openstack loadbalancer create --project kuryrk8s --vip-address 10.2.0.1 --vip-subnet-id c3e52567-5202-4396-954b-806ce64094ed --name kuryr/kubernetes
+---------------------+--------------------------------------+
| Field               | Value                                |
+---------------------+--------------------------------------+
| admin_state_up      | True                                 |
| created_at          | 2019-03-15T07:27:27                  |
| description         |                                      |
| flavor_id           | None                                 |
| id                  | 661cc831-c57c-4aa1-9b99-b5c1ab7c78df |
| listeners           |                                      |
| name                | kuryr/kubernetes                     |
| operating_status    | OFFLINE                              |
| pools               |                                      |
| project_id          | 77622b1a98e14737a4f1563aa0531c1e     |
| provider            | amphora                              |
| provisioning_status | PENDING_CREATE                       |
| updated_at          | None                                 |
| vip_address         | 10.2.0.1                             |
| vip_network_id      | fe214a02-9bcb-40ea-be84-04d68f93f4d2 |
| vip_port_id         | a7bb77e5-a1a1-44de-852c-5f0abcfbbfa9 |
| vip_qos_policy_id   | None                                 |
| vip_subnet_id       | c3e52567-5202-4396-954b-806ce64094ed |
+---------------------+--------------------------------------+

$ openstack loadbalancer pool create --name kuryr/kubernetes:HTTPS:443 --protocol HTTPS --lb-algorithm LEAST_CONNECTIONS --loadbalancer 661cc831-c57c-4aa1-9b99-b5c1ab7c78df
+----------------------+--------------------------------------+
| Field                | Value                                |
+----------------------+--------------------------------------+
| admin_state_up       | True                                 |
| created_at           | 2019-03-15T07:30:09                  |
| description          |                                      |
| healthmonitor_id     |                                      |
| id                   | 6ee8eaf0-d8a7-46c3-80fa-aa306b8c43b8 |
| lb_algorithm         | LEAST_CONNECTIONS                    |
| listeners            |                                      |
| loadbalancers        | 661cc831-c57c-4aa1-9b99-b5c1ab7c78df |
| members              |                                      |
| name                 | kuryr/kubernetes:HTTPS:443           |
| operating_status     | OFFLINE                              |
| project_id           | 77622b1a98e14737a4f1563aa0531c1e     |
| protocol             | HTTPS                                |
| provisioning_status  | PENDING_CREATE                       |
| session_persistence  | None                                 |
| updated_at           | None                                 |
| tls_container_ref    | None                                 |
| ca_tls_container_ref | None                                 |
| crl_container_ref    | None                                 |
| tls_enabled          | False                                |
+----------------------+--------------------------------------+

$ openstack loadbalancer member create --name kuryr-k8s-master --address 192.168.1.2 --protocol-port 6443 6ee8eaf0-d8a7-46c3-80fa-aa306b8c43b8
+---------------------+--------------------------------------+
| Field               | Value                                |
+---------------------+--------------------------------------+
| address             | 192.168.1.2                          |
| admin_state_up      | True                                 |
| created_at          | 2019-03-15T07:32:24                  |
| id                  | 693ea863-929f-4cb4-bc0a-5f4ac80bc1e6 |
| name                | kuryr-k8s-master                     |
| operating_status    | NO_MONITOR                           |
| project_id          | 77622b1a98e14737a4f1563aa0531c1e     |
| protocol_port       | 6443                                 |
| provisioning_status | PENDING_CREATE                       |
| subnet_id           | None                                 |
| updated_at          | None                                 |
| weight              | 1                                    |
| monitor_port        | None                                 |
| monitor_address     | None                                 |
| backup              | False                                |
+---------------------+--------------------------------------+

$ openstack loadbalancer listener create --name kuryr/kubernetes:HTTPS:443 --protocol HTTPS --default-pool 6ee8eaf0-d8a7-46c3-80fa-aa306b8c43b8 --protocol-port 443 661cc831-c57c-4aa1-9b99-b5c1ab7c78df
+-----------------------------+--------------------------------------+
| Field                       | Value                                |
+-----------------------------+--------------------------------------+
| admin_state_up              | True                                 |
| connection_limit            | -1                                   |
| created_at                  | 2019-03-15T07:36:44                  |
| default_pool_id             | 6ee8eaf0-d8a7-46c3-80fa-aa306b8c43b8 |
| default_tls_container_ref   | None                                 |
| description                 |                                      |
| id                          | a3c01bb5-1464-4206-9cdd-5a8cac56ac8c |
| insert_headers              | None                                 |
| l7policies                  |                                      |
| loadbalancers               | 661cc831-c57c-4aa1-9b99-b5c1ab7c78df |
| name                        | kuryr/kubernetes:HTTPS:443           |
| operating_status            | OFFLINE                              |
| project_id                  | 77622b1a98e14737a4f1563aa0531c1e     |
| protocol                    | HTTPS                                |
| protocol_port               | 443                                  |
| provisioning_status         | PENDING_CREATE                       |
| sni_container_refs          | []                                   |
| timeout_client_data         | 50000                                |
| timeout_member_connect      | 5000                                 |
| timeout_member_data         | 50000                                |
| timeout_tcp_inspect         | 0                                    |
| updated_at                  | 2019-03-15T07:36:44                  |
| client_ca_tls_container_ref | None                                 |
| client_authentication       | NONE                                 |
| client_crl_container_ref    | None                                 |
+-----------------------------+--------------------------------------+
```

## 編輯配置檔/etc/kuryr/kuryr.conf
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
# password = ADMIN_PASS
password = password
project_name = k8s
project_domain_name = Default
auth_type = password
[neutron_defaults]
ovs_bridge = br-int
pod_security_groups = 5c0ddafd-1c06-4207-adbd-2e72d73cc810
pod_subnet = 5b03e5b7-d331-41e5-94e5-eee95ca0892b
project = 37ea8f533f6b4287a4a9bdd73a249404
service_subnet = 91322fae-b300-486d-8572-e4c8eef5d177
```

## loadbalancer create

```
$ openstack subnet list
+--------------------------------------+----------------+--------------------------------------+----------------+
| ID                                   | Name           | Network                              | Subnet         |
+--------------------------------------+----------------+--------------------------------------+----------------+
| 1203dae9-f031-4acd-802c-1821b36f9af3 | test           | 38d17d93-f49c-4764-ac03-6b24aba9f33a | 10.0.2.0/24    |
| 46fbcd7d-13b6-47ec-8098-549c89931b43 | service        | a8cdd457-9f33-4413-aaf3-25786c05c1a6 | 10.2.0.0/16    |
| 48c7085d-b647-49eb-af95-5b7c3d2b8286 | pod            | 1abcdd6a-3b02-401f-8e95-8fd1c15d665a | 10.1.0.0/16    |
| b982dba2-1fce-47e0-9863-ea68350bba03 | lb-mgmt-subnet | d713a472-5a7e-483f-b641-2871fba869ce | 192.168.0.0/24 |
| dc57614a-f9fe-4a27-932c-7b771755f507 | public         | bd9b7d21-23ba-4db9-9b14-bd9ea9c8f9ac | 10.0.1.0/24    |
+--------------------------------------+----------------+--------------------------------------+----------------+

$ openstack loadbalancer create --vip-address 10.2.0.1 --vip-subnet-id 46fbcd7d-13b6-47ec-8098-549c89931b43 --name default/kubernetes
+---------------------+--------------------------------------+
| Field               | Value                                |
+---------------------+--------------------------------------+
| admin_state_up      | True                                 |
| created_at          | 2019-03-14T08:52:20                  |
| description         |                                      |
| flavor_id           | None                                 |
| id                  | c9c1f443-dfb4-4ee2-b76f-6472dc51d242 |
| listeners           |                                      |
| name                | default/kubernetes                   |
| operating_status    | OFFLINE                              |
| pools               |                                      |
| project_id          | 456101ea23a04d08bea1f700e0de9020     |
| provider            | amphora                              |
| provisioning_status | PENDING_CREATE                       |
| updated_at          | None                                 |
| vip_address         | 10.2.0.1                             |
| vip_network_id      | a8cdd457-9f33-4413-aaf3-25786c05c1a6 |
| vip_port_id         | 9d50d3a2-b322-4bdf-8501-b20099845a7d |
| vip_qos_policy_id   | None                                 |
| vip_subnet_id       | 46fbcd7d-13b6-47ec-8098-549c89931b43 |
+---------------------+--------------------------------------+

openstack loadbalancer pool create --name default/kubernetes:HTTPS:443 --protocol HTTPS --lb-algorithm LEAST_CONNECTIONS --loadbalancer c9c1f443-dfb4-4ee2-b76f-6472dc51d242
+----------------------+--------------------------------------+
| Field                | Value                                |
+----------------------+--------------------------------------+
| admin_state_up       | True                                 |
| created_at           | 2019-03-14T09:03:51                  |
| description          |                                      |
| healthmonitor_id     |                                      |
| id                   | bebb5c98-630d-4438-909d-baba7c189df1 |
| lb_algorithm         | LEAST_CONNECTIONS                    |
| listeners            |                                      |
| loadbalancers        | c9c1f443-dfb4-4ee2-b76f-6472dc51d242 |
| members              |                                      |
| name                 | default/kubernetes:HTTPS:443         |
| operating_status     | OFFLINE                              |
| project_id           | 456101ea23a04d08bea1f700e0de9020     |
| protocol             | HTTPS                                |
| provisioning_status  | PENDING_CREATE                       |
| session_persistence  | None                                 |
| updated_at           | None                                 |
| tls_container_ref    | None                                 |
| ca_tls_container_ref | None                                 |
| crl_container_ref    | None                                 |
| tls_enabled          | False                                |
+----------------------+--------------------------------------+

$ openstack loadbalancer member create --name k8s-master-0 --address 192.168.1.2 --protocol-port 6443 bebb5c98-630d-4438-909d-baba7c189df1
+---------------------+--------------------------------------+
| Field               | Value                                |
+---------------------+--------------------------------------+
| address             | 192.168.1.2                          |
| admin_state_up      | True                                 |
| created_at          | 2019-03-14T09:06:52                  |
| id                  | b40d2db2-fc11-4396-8e1e-cc8dee50f442 |
| name                | k8s-master-0                         |
| operating_status    | NO_MONITOR                           |
| project_id          | 456101ea23a04d08bea1f700e0de9020     |
| protocol_port       | 6443                                 |
| provisioning_status | PENDING_CREATE                       |
| subnet_id           | None                                 |
| updated_at          | None                                 |
| weight              | 1                                    |
| monitor_port        | None                                 |
| monitor_address     | None                                 |
| backup              | False                                |
+---------------------+--------------------------------------+

$ openstack loadbalancer listener create --name default/kubernetes:HTTPS:443 --protocol HTTPS --default-pool bebb5c98-630d-4438-909d-baba7c189df1 --protocol-port 443 c9c1f443-dfb4-4ee2-b76f-6472dc51d242
+-----------------------------+--------------------------------------+
| Field                       | Value                                |
+-----------------------------+--------------------------------------+
| admin_state_up              | True                                 |
| connection_limit            | -1                                   |
| created_at                  | 2019-03-14T09:08:25                  |
| default_pool_id             | bebb5c98-630d-4438-909d-baba7c189df1 |
| default_tls_container_ref   | None                                 |
| description                 |                                      |
| id                          | e8a5fd1d-1b72-41d4-8e5f-03f4470467dc |
| insert_headers              | None                                 |
| l7policies                  |                                      |
| loadbalancers               | c9c1f443-dfb4-4ee2-b76f-6472dc51d242 |
| name                        | default/kubernetes:HTTPS:443         |
| operating_status            | OFFLINE                              |
| project_id                  | 456101ea23a04d08bea1f700e0de9020     |
| protocol                    | HTTPS                                |
| protocol_port               | 443                                  |
| provisioning_status         | PENDING_CREATE                       |
| sni_container_refs          | []                                   |
| timeout_client_data         | 50000                                |
| timeout_member_connect      | 5000                                 |
| timeout_member_data         | 50000                                |
| timeout_tcp_inspect         | 0                                    |
| updated_at                  | 2019-03-14T09:08:25                  |
| client_ca_tls_container_ref | None                                 |
| client_authentication       | NONE                                 |
| client_crl_container_ref    | None                                 |
+-----------------------------+--------------------------------------+
```

## kuryr-cni
/opt/stack/kuryr-k8s-controller/env/local/bin

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