# 成功
## 開始使用環境
```shell
$ pip install python-openstackclient python-glanceclient python-neutronclient --ignore-installed PyYAML
$ pip install python-tackerclient
$ kolla-ansible/tools/kolla-ansible post-deploy
```
## 建立cloud image
```shell
$ . /etc/kolla/admin-openrc.sh
$ wget http://download.cirros-cloud.net/0.4.0/cirros-0.4.0-x86_64-disk.img
$ openstack image create "cirros"   --file cirros-0.4.0-x86_64-disk.img   --disk-format qcow2 --container-format bare   --public
$ wget http://cloud-images.ubuntu.com/xenial/current/xenial-server-cloudimg-amd64-disk1.img
$ openstack image create "ubuntu"   --file xenial-server-cloudimg-amd64-disk1.img   --disk-format qcow2 --container-format bare   --public
```
## 建立VIM資訊
```shell
$ vim vim_config.yaml
auth_url: 'http://10.0.1.101:35357/v3'
username: 'admin'
password: '2bYiAgHvccZoaDIZyeGhbVlR5ZkQt1LgNV76bp7Q'
project_name: 'admin'
project_domain_name: 'Default'
user_domain_name: 'Default'
cert_verify: 'False'

$ openstack vim register --config-file vim_config.yaml        --description 'my first vim' --is-default hellovim
```
## 建立Network
1. net_mgmt 10.10.0.0/24 10.10.0.254
2. net0 10.20.0.0/24 10.20.0.254
3. net1 10.30.0.0/24 10.30.0.254
## 新增Security Groups規則
ICMP Ingress Egress
TCP Ingress Egress
UDP Ingress Egress
## 新增Kry Pairs
Titan
## 建立http_client VM、http_server VM
```shell
$ net_id=$(openstack network list | grep net0 | awk '{print $2}')
$ openstack server create --flavor m1.tiny --image ubuntu --key-name Titan --nic net-id=$net_id http_client
$ openstack server create --flavor m1.tiny --image ubuntu --key-name Titan  --nic net-id=$net_id http_server
```
## 建立VNFD1、VNFD2
```shell
$ vim tosca-vnffg-vnfd1.yaml
$ vim tosca-vnffg-vnfd2.yaml
$ tacker vnfd-create --vnfd-file tosca-vnffg-vnfd1.yaml vnfd1
$ tacker vnfd-create --vnfd-file tosca-vnffg-vnfd2.yaml vnfd2
```
## Create VNF
```yaml
$ tacker vnf-create --vnfd-name vnfd1 vnf1_001
$ tacker vnf-create --vnfd-name vnfd2 vnf2_001
```
## 建立http server
```shell
$ ssh ubuntu@HTTP_SERVER_IP
$ vim shell.sh
#!/bin/sh
sudo apt-get update
sudo apt-get install -y build-essential libssl-dev
curl https://raw.githubusercontent.com/creationix/nvm/v0.25.0/install.sh | bash
source ~/.profile
nvm install 8
nvm alias default 8
npm install koa
npm install koa-router
npm install -g pm2
cat << EOF >> /home/ubuntu/app.js
const koa = require('koa');
const Router = require('koa-router');
const app = new koa();
const router = Router();
router.get('/',async (ctx) => {
  console.log('apple');
  ctx.body = 'apple';
});
app.use(router.routes());
app.listen(3000);
EOF
pm2 start /home/ubuntu/app.js

$ . shell.sh
```

## Create VNFFG
```yaml
# http_client IP 10.20.0.14
$ openstack port list | grep 10.20.0.14
9079ae69-6cd5-4173-8357-84e10ffd01c7

# http_server IP 10.20.0.6
$ openstack port list | grep 10.20.0.6
70268b55-5fc4-4405-a73e-77f7e723fc33

$ vim tosca-vnffgd-sample.yaml
tosca_definitions_version: tosca_simple_profile_for_nfv_1_0_0

description: Sample symmetrical VNFFG template (network_dst_port_id and ip_dst_prefix must be set)

topology_template:

  node_templates:

    Forwarding_path1:
      type: tosca.nodes.nfv.FP.TackerV2
      description: creates path (CP12->CP22)
      properties:
        id: 96
        policy:
          type: ACL
          criteria:
            - name: block_tcp
              classifier:
                network_src_port_id: 9079ae69-6cd5-4173-8357-84e10ffd01c7
                network_dst_port_id: 70268b55-5fc4-4405-a73e-77f7e723fc33
                ip_dst_prefix: 10.20.0.6/24
                destination_port_range: 3000-3000
                ip_proto: 6
        path:
          - forwarder: VNFD1
            capability: CP12
          - forwarder: VNFD2
            capability: CP22

  groups:
    VNFFG1:
      type: tosca.groups.nfv.VNFFG
      description: HTTP to Corporate Net
      properties:
        vendor: tacker
        version: 1.0
        number_of_endpoints: 2
        dependent_virtual_link: [VL12,VL22]
        connection_point: [CP12,CP22]
        constituent_vnfs: [VNFD1,VNFD2]
      members: [Forwarding_path1]

# 建立VNFFGD
$ openstack vnf graph descriptor create --vnffgd-file tosca-vnffgd-sample.yaml tosca-vnffgd-sample

# 建立VNFFG
$ openstack vnf list
+--------------------------------------+----------+-----------------+--------+--------------------------------------+--------------------------------------+
| ID                                   | Name     | Mgmt Ip Address | Status | VIM ID                               | VNFD ID                              |
+--------------------------------------+----------+-----------------+--------+--------------------------------------+--------------------------------------+
| 33ffe62d-7a40-49b2-89cd-7fc303384152 | vnf2_001 |                 | ACTIVE | bc9a06a1-9596-46bc-abc1-55ccd21a2083 | 29e3585f-d1d5-44fe-803a-e8e66d3c1d75 |
| 50ac8288-70dc-4335-8904-9aef204a5727 | vnf1_001 |                 | ACTIVE | bc9a06a1-9596-46bc-abc1-55ccd21a2083 | cced482b-4f2c-4da9-a871-7018fcd4389c |
+--------------------------------------+----------+-----------------+--------+--------------------------------------+--------------------------------------+

$ openstack vnf graph create --vnffgd-name tosca-vnffgd-sample --vnf-mapping VNFD1:'50ac8288-70dc-4335-8904-9aef204a5727',VNFD2:'33ffe62d-7a40-49b2-89cd-7fc303384152' tosca-vnffgd-sample
```