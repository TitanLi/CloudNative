# Tacker
[Install Tacker](https://docs.openstack.org/tacker/latest/install/manual_installation.html#registering-default-vim)

[Tacker基本操作](https://docs.openstack.org/tacker/latest/user/multisite_vim_usage_guide.html)
## 新增VIM
```shell
$ vim vim_config.yaml
auth_url: 'http://10.0.1.100:35357/v3'
username: 'admin'
password: '9Y9vpZaTHIbRD17hMOKylxvPb1RIKplbmvp58ug0'
project_name: 'admin'
project_domain_name: 'Default'
user_domain_name: 'Default'
# 關閉SSL
cert_verify: 'False'

# 建立默認VIM
$ openstack vim register --config-file vim_config.yaml \
       --description 'my first vim' --is-default hellovim
```
## Updating a VIM
> Note that ‘auth_url’ parameter of a VIM is not allowed to be updated as ‘auth_url’ uniquely identifies a given ‘vim’ resource.
```shell
$ vim update.yaml
# 新增資料
username: 'new_user'
password: 'new_pw'

$ openstack vim set VIM0 --config-file update.yaml
```
## Deleting a VIM
```shell
$ openstack vim delete VIM1
```
## 驗證
```yaml
$ vim sample-vnfd.yaml

tosca_definitions_version: tosca_simple_profile_for_nfv_1_0_0

description: Demo example

metadata:
  template_name: sample-tosca-vnfd

topology_template:
  node_templates:
    VDU1:
      type: tosca.nodes.nfv.VDU.Tacker
      capabilities:
        nfv_compute:
          properties:
            num_cpus: 1
            mem_size: 512 MB
            disk_size: 1 GB
      properties:
        image: cirros
        availability_zone: nova
        mgmt_driver: noop
        key_name: Titan
        # config: |
        #     param0: key1
        #     param1: key2

    CP1:
      type: tosca.nodes.nfv.CP.Tacker
      properties:
        management: true
        order: 0
        anti_spoofing_protection: false
      requirements:
        - virtualLink:
            node: VL1
        - virtualBinding:
            node: VDU1

    VL1:
      type: tosca.nodes.nfv.VL
      properties:
        network_name: net0
        vendor: Tacker
```
## Onboard a VNFD
```shell
$ openstack vnf descriptor create --vnfd-file sample-vnfd.yaml samplevnfd
```
## Deploying a new VNF on registered VIM
```shell
# openstack vnf create --description 'Openwrt VNF on Site1' --vnfd-id <VNFD-ID> --vim-name <VIM-Name> <VNF-Name>
$ openstack vnf create --vnfd-name samplevnfd samplevnf
```
## 常用Tacker命令
```shell
# 可用VIM列表
$ openstack vim list
# VNFD
$ openstack vnf descriptor list
# VNF
$ openstack vnf list
$ openstack vnf show samplevnf
```