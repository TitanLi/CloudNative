# VNFFG
## Create HTTP client and HTTP server
```shell
$ net_id=$(openstack network list | grep net0 | awk '{print $2}')
$ openstack server create --flavor m1.tiny --image cirros --nic net-id=$net_id http_client
$ openstack server create --flavor m1.tiny --image cirros --nic net-id=$net_id http_server
```
## 取得Port ID
```shell
# network_src_port_id
$ client_ip=$(openstack server list | grep http_client | grep -Eo '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+')
$ network_source_port_id=$(openstack port list | grep $client_ip | awk '{print $2}')
$ echo $network_source_port_id
afced056-6176-4c7d-9b3b-05fd6226deab
# network_dest_port_id
$ ip_dst=$(openstack server list | grep http_server | grep -Eo '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+')
$ network_dest_port_id=$(openstack port list | grep $ip_dst | awk '{print $2}')
$ echo $network_dest_port_id
48217155-a950-4cec-80ab-de14fa63c19f
```
## tosca-vnffg-vnfd1
```yaml
$ vim tosca-vnffg-vnfd1.yaml
tosca_definitions_version: tosca_simple_profile_for_nfv_1_0_0

description: sample-tosca-vnfd1

metadata:
  template_name: sample-tosca-vnfd1

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
        config: |
          param0: key1
          param1: key2
        user_data_format: RAW
        user_data: |
          #!/bin/sh
          echo 1 > /proc/sys/net/ipv4/ip_forward
          cat << EOF >> /etc/network/interfaces
          auto eth1
          iface eth1 inet dhcp
          auto eth2
          iface eth2 inet dhcp
          EOF
          ifup eth1
          ifup eth2
    CP11:
      type: tosca.nodes.nfv.CP.Tacker
      properties:
        management: true
        order: 0
        anti_spoofing_protection: false
      requirements:
        - virtualLink:
            node: VL11
        - virtualBinding:
            node: VDU1

    CP12:
      type: tosca.nodes.nfv.CP.Tacker
      properties:
        order: 1
        anti_spoofing_protection: false
      requirements:
        - virtualLink:
            node: VL12
        - virtualBinding:
            node: VDU1

    CP13:
      type: tosca.nodes.nfv.CP.Tacker
      properties:
        order: 2
        anti_spoofing_protection: false
      requirements:
        - virtualLink:
            node: VL13
        - virtualBinding:
            node: VDU1

    VL11:
      type: tosca.nodes.nfv.VL
      properties:
        network_name: net_mgmt
        vendor: Tacker

    VL12:
      type: tosca.nodes.nfv.VL
      properties:
        network_name: net0
        vendor: Tacker

    VL13:
      type: tosca.nodes.nfv.VL
      properties:
        network_name: net1
        vendor: Tacker
```
## tosca-vnffg-vnfd2
```yaml
$ vim tosca-vnffg-vnfd2.yaml
tosca_definitions_version: tosca_simple_profile_for_nfv_1_0_0

description: sample-tosca-vnfd2

metadata:
  template_name: sample-tosca-vnfd2

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
        config: |
          param0: key1
          param1: key2
        user_data_format: RAW
        user_data: |
          #!/bin/sh
          echo 1 > /proc/sys/net/ipv4/ip_forward
          cat << EOF >> /etc/network/interfaces
          auto eth1
          iface eth1 inet dhcp
          auto eth2
          iface eth2 inet dhcp
          EOF
          ifup eth1
          ifup eth2
    CP21:
      type: tosca.nodes.nfv.CP.Tacker
      properties:
        management: true
        order: 0
        anti_spoofing_protection: false
      requirements:
        - virtualLink:
            node: VL21
        - virtualBinding:
            node: VDU1

    CP22:
      type: tosca.nodes.nfv.CP.Tacker
      properties:
        order: 1
        anti_spoofing_protection: false
      requirements:
        - virtualLink:
            node: VL22
        - virtualBinding:
            node: VDU1

    CP23:
      type: tosca.nodes.nfv.CP.Tacker
      properties:
        order: 2
        anti_spoofing_protection: false
      requirements:
        - virtualLink:
            node: VL23
        - virtualBinding:
            node: VDU1

    VL21:
      type: tosca.nodes.nfv.VL
      properties:
        network_name: net_mgmt
        vendor: Tacker

    VL22:
      type: tosca.nodes.nfv.VL
      properties:
        network_name: net0
        vendor: Tacker

    VL23:
      type: tosca.nodes.nfv.VL
      properties:
        network_name: net1
        vendor: Tacker
```
## tosca-vnffgd-sample
```yaml
$ vim tosca-vnffgd-sample.yaml
tosca_definitions_version: tosca_simple_profile_for_nfv_1_0_0

description: Sample VNFFG template

topology_template:

  node_templates:

    Forwarding_path1:
      type: tosca.nodes.nfv.FP.TackerV2
      description: creates path (CP12->CP22)
      properties:
        id: 51
        symmetrical: true
        correlation: nsh
        policy:
          type: ACL
          criteria:
            - name: block_tcp
              classifier:
                network_src_port_id: afced056-6176-4c7d-9b3b-05fd6226deab
                network_dst_port_id: 48217155-a950-4cec-80ab-de14fa63c19f
                ip_dst_prefix: 10.30.0.253/24
                destination_port_range: 80-30000
                ip_proto: 6
        path:
          - forwarder: VNFD1
            capability: CP12
            sfc_encap: True
          - forwarder: VNFD2
            capability: CP22
            sfc_encap: False
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
```
## Create VNFFGD
```shell
# $ openstack vnf graph descriptor create --vnffgd-file <vnffgd-file> <vnffgd-name>
$ openstack vnf graph descriptor create --vnffgd-file tosca-vnffgd-sample.yaml tosca-vnffgd-sample
```
## Create VNFD,VNF
```shell
$ openstack vnf descriptor create --vnfd-file tosca-vnffg-vnfd1.yaml VNFD1
$ openstack vnf create --vnfd-name VNFD1 VNF1

$ openstack vnf descriptor create --vnfd-file tosca-vnffg-vnfd2.yaml VNFD2
$ openstack vnf create --vnfd-name VNFD2 VNF2
```
## Create VNFFG
> vnffgd-name : VNFFGD to use to instantiate this VNFFG <br>
> param-file : Parameter file in Yaml <br>
> vnf-mapping : Allows a list of logical VNFD to VNF instance mapping <br>
> symmetrical : If –symmetrical is present, symmetrical is True (default: False - The symmectical is set in template has higher priority)
```shell
$ openstack vnf list
+--------------------------------------+-------------------------+-------------------------+----------------+--------------------------------------+--------------------------------------+
| ID                                   | Name                    | Mgmt Ip Address         | Status         | VIM ID                               | VNFD ID                              |
+--------------------------------------+-------------------------+-------------------------+----------------+--------------------------------------+--------------------------------------+
| 058b9ba3-4402-4140-8dd1-1c616fb39bae | VNF2                    | {"VDU1": "10.20.0.132"} | ACTIVE         | 895044c5-2398-439c-8db5-2fec8c89d5b3 | b9aae699-b3a4-4965-b40a-7b7dcb0b5b9a |
| 67148c8b-2d88-4430-96a3-85483b78d306 | VNF1                    | {"VDU1": "10.20.0.12"}  | ACTIVE         | 895044c5-2398-439c-8db5-2fec8c89d5b3 | efc6873f-bed8-4572-a56e-b86181166801 |

# Tacker provides the following OpenStackClient CLI to create VNFFG from VNFFGD
# $ openstack vnf graph create --vnffgd-name <vnffgd-name> --vnf-mapping <vnf-mapping> --symmetrical <vnffg-name>

# create directly VNFFG from vnffgd template without initiating VNFFGD
# $ openstack vnf graph create --vnffgd-template <vnffgd-template> --vnf-mapping <vnf-mapping> --symmetrical <vnffg-name>

# use a parameterized vnffg template
# $ openstack vnf graph create --vnffgd-name <vnffgd-name> --param-file <param-file> --vnf-mapping <vnf-mapping> --symmetrical <vnffg-name>

$ openstack vnf graph create --vnffgd-name tosca-vnffgd-sample --vnf-mapping VNFD1:'67148c8b-2d88-4430-96a3-85483b78d306',VNFD2:'058b9ba3-4402-4140-8dd1-1c616fb39bae' --symmetrical tosca-vnffgd-sample
```
## VNFFGD(共用)
1. 參數Yaml file
```yaml
$ vim vnffg-param-file.yaml
# 新增內容
net_src_port_id: 640dfd77-c92b-45a3-b8fc-22712de480e1
dst_port_range: 80-1024
ip_dst_pre: 192.168.1.2/24
```
2. VNFFGD取得參數方法
```yaml
tosca_definitions_version: tosca_simple_profile_for_nfv_1_0_0

description: Sample VNFFG template

topology_template:

  inputs:
    net_src_port_id:
        type: string
        description: Port UUID of source VM.
  node_templates:

    Forwarding_path1:
      type: tosca.nodes.nfv.FP.TackerV2
      description: creates path (CP12->CP22)
      properties:
        id: 51
        correlation: mpls
        policy:
          type: ACL
          criteria:
            - name: block_tcp
              classifier:
                network_src_port_id: { get_input: net_src_port_id }
......
```
3. Create VNFFG
```shell
$ openstack vnf graph create --vnffgd-name vnffgd-param --vnf-mapping VNFD1:'91e32c20-6d1f-47a4-9ba7-08f5e5effe07',\
VNFD2:'7168062e-9fa1-4203-8cb7-f5c99ff3ee1b' --param-file vnffg-param-file.yaml myvnffg
```
## Update VNFFG
[Update VNFFG](https://docs.openstack.org/tacker/latest/user/vnffg_usage_guide.html#viewing-a-vnffg)