# OpenWRT
## openwrt VNFD
```yaml
$ vim tosca-vnfd-openwrt.yaml
tosca_definitions_version: tosca_simple_profile_for_nfv_1_0_0

description: OpenWRT with services

metadata:
  template_name: OpenWRT

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
        image: OpenWRT
        config: |
          param0: key1
          param1: key2
        mgmt_driver: openwrt
        key_name: Titan
        monitoring_policy:
          name: ping
          parameters:
            count: 3
            interval: 10
          actions:
            failure: respawn

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

    CP2:
      type: tosca.nodes.nfv.CP.Tacker
      properties:
        order: 1
        anti_spoofing_protection: false
      requirements:
        - virtualLink:
            node: VL2
        - virtualBinding:
            node: VDU1

    CP3:
      type: tosca.nodes.nfv.CP.Tacker
      properties:
        order: 2
        anti_spoofing_protection: false
      requirements:
        - virtualLink:
            node: VL3
        - virtualBinding:
            node: VDU1

    VL1:
      type: tosca.nodes.nfv.VL
      properties:
        network_name: net_mgmt
        vendor: Tacker

    VL2:
      type: tosca.nodes.nfv.VL
      properties:
        network_name: net0
        vendor: Tacker

    VL3:
      type: tosca.nodes.nfv.VL
      properties:
        network_name: net1
        vendor: Tacker firewall
```
## openwrt config
```yaml
$ vim tosca-config-openwrt-firewall.yaml
vdus:
  VDU1:
    config:
      firewall: |
        package firewall
        config defaults
            option syn_flood '1'
            option input 'ACCEPT'
            option output 'ACCEPT'
            option forward 'REJECT'
        config zone
            option name 'lan'
            list network 'lan'
            option input 'ACCEPT'
            option output 'ACCEPT'
            option forward 'ACCEPT'
        config zone
            option name 'wan'
            list network 'wan'
            list network 'wan6'
            option input 'REJECT'
            option output 'ACCEPT'
            option forward 'REJECT'
            option masq '1'
            option mtu_fix '1'
        config forwarding
            option src 'lan'
            option dest 'wan'
        config rule
            option name 'Allow-DHCP-Renew'
            option src 'wan'
            option proto 'udp'
            option dest_port '68'
            option target 'ACCEPT'
            option family 'ipv4'
        config rule
            option name 'Allow-Ping'
            option src 'wan'
            option proto 'icmp'
            option icmp_type 'echo-request'
            option family 'ipv4'
            option target 'ACCEPT'
        config rule
            option name 'Allow-IGMP'
            option src 'wan'
            option proto 'igmp'
            option family 'ipv4'
            option target 'ACCEPT'
        config rule
            option name 'Allow-DHCPv6'
            option src 'wan'
            option proto 'udp'
            option src_ip 'fe80::/10'
            option src_port '547'
            option dest_ip 'fe80::/10'
            option dest_port '546'
            option family 'ipv6'
            option target 'ACCEPT'
        config rule
            option name 'Allow-MLD'
            option src 'wan'
            option proto 'icmp'
            option src_ip 'fe80::/10'
            list icmp_type '130/0'
            list icmp_type '131/0'
            list icmp_type '132/0'
            list icmp_type '143/0'
            option family 'ipv6'
            option target 'ACCEPT'
        config rule
            option name 'Allow-ICMPv6-Input'
            option src 'wan'
            option proto 'icmp'
            list icmp_type 'echo-request'
            list icmp_type 'echo-reply'
            list icmp_type 'destination-unreachable'
            list icmp_type 'packet-too-big'
            list icmp_type 'time-exceeded'
            list icmp_type 'bad-header'
            list icmp_type 'unknown-header-type'
            list icmp_type 'router-solicitation'
            list icmp_type 'neighbour-solicitation'
            list icmp_type 'router-advertisement'
            list icmp_type 'neighbour-advertisement'
            option limit '190/sec'
            option family 'ipv6'
            option target 'REJECT'
```
## 執行
```shell
# 建立VNFD
$ openstack vnf descriptor create --vnfd-file tosca-vnfd-openwrt.yaml tosca-vnfd-openwrt
# 啟動VNF
$ openstack vnf create --vnfd-name tosca-vnfd-openwrt --config-file tosca-config-openwrt-firewall.yaml tosca-vnfd-openwrt-demo
# 檢查狀態
$ openstack vnf list
$ openstack vnf show <VNF_ID>
```