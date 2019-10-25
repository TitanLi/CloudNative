# Tacker
[Install Tacker](https://docs.openstack.org/tacker/latest/install/manual_installation.html#registering-default-vim)

[Tacker基本操作](https://docs.openstack.org/tacker/latest/user/multisite_vim_usage_guide.html)

----
## 參考資料
[OpenStack SDN - NFV Management and Orchestration](https://networkop.co.uk/blog/2017/11/23/os-nfv-mano/)

[TOSCA Simple Profile for Network Functions Virtualization (NFV) Version 1.0](http://docs.oasis-open.org/tosca/tosca-nfv/v1.0/csd03/tosca-nfv-v1.0-csd03.html)

[Tacker User Guide](https://docs.openstack.org/tacker/rocky/user/index.html)

[tacker samples tosca-templates](https://github.com/openstack/tacker/tree/stable/stein/samples/tosca-templates)

[networking-sfc](https://docs.openstack.org/networking-sfc/latest/contributor/ietf_sfc_encapsulation.html)
----
## Table of Contents
* [環境安裝](#環境安裝)
  - [Prepare initial configuration(globals)](#prepare-initial-configurationglobals)
* [使用教學](#使用教學)
  - [新增vim](#新增vim)
  - [Updating a VIM](#updating-a-vim)
  - [Deleting a VIM](#deleting-a-vim)
  - [建立VNFD Template](#建立vnfd-template)
  - [Onboard a VNFD](#onboard-a-vnfd)
  - [Deploying a new VNF on registered VIM](#deploying-a-new-vnf-on-registered-vim)
  - [常用Tacker命令](#常用tacker命令)
    - [可用VIM列表](#可用VIM列表)
    - [Create VNF](#create-vnf)
    - [VNFD or VNF list](#vnfd-or-vnf-list)
    - [Finding VNFM Status](#finding-vnfm-status)
    - [Deleting VNF and VNFD](#deleting-vnf-and-vnfd)
  - [問題解決](#問題解決)
    - [tacker CLI](#1-tacker-cli)
# 環境安裝
## Prepare initial configuration(globals)
master
```shell
$ vim /etc/kolla/globals.yml 
kolla_base_distro: "ubuntu"
kolla_install_type: "source"
openstack_release: "rocky"
kolla_internal_vip_address: "10.0.1.100"
network_interface: "eno1"
neutron_external_interface: "ens3"
keepalived_virtual_router_id: "96"
enable_glance: "yes"
enable_haproxy: "yes"
enable_keystone: "yes"
enable_mariadb: "yes"
enable_memcached: "yes"
enable_neutron: "yes"
enable_nova: "yes"
enable_rabbitmq: "yes"
enable_aodh: "yes"
enable_ceilometer: "yes"
enable_gnocchi: "yes"
enable_heat: "yes"
enable_horizon: "yes"
enable_neutron_sfc: "yes"
enable_barbican: "yes"
enable_mistral: "yes"
enable_redis: "yes"
enable_tacker: "yes"
# enable_cinder: "yes"
# enable_cinder_backend_iscsi: "yes"
```
# 使用教學
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
## 建立VNFD Template
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
### 可用VIM列表
```shell
$ openstack vim list
```
### Create VNF
方法一:
```shell
$ openstack vnf descriptor create --vnfd-file <yaml file path> <VNFD-NAME>
$ openstack vnf create --vnfd-name <VNFD-FILE-NAME> <VNF-NAME>
```
方法二:
```shell
$ openstack vnf create --vnfd-template <VNFD-FILE-NAME> <VNF-NAME>
```
### VNFD or VNF list
```shell
# VNFD
$ openstack vnf descriptor list
# VNF
$ openstack vnf list
$ openstack vnf show samplevnf
```
### Finding VNFM Status
```shell
$ openstack vim list
$ openstack vnf descriptor list
$ openstack vnf list
$ openstack vnf show <VNF_ID>
$ openstack vnf descriptor show <VNFD_ID>
```
### Deleting VNF and VNFD
```shell
$ openstack vnf delete <VNF_ID/NAME>
$ openstack vnf descriptor delete <VNFD_ID/NAME>
```
## 問題解決
### 1. tacker CLI
問題
```shell
$ openstack vnf descriptor create --vnfd-file tosca-vnffg-vnfd1.yaml VNFD1 
openstack: 'vnf descriptor create --vnfd-file tosca-vnffg-vnfd1.yaml VNFD1' is not an openstack command. See 'openstack --help'.
```
解決方法
```shell
$ pip install python-tackerclient
$ pip install --upgrade python-openstackclient
```