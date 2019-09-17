# Monitoring VNF
## Table of Contents
* [Create Monitoring VNFD](#monitoring-vnfd)
* [執行](#執行)
## Create Monitoring VNFD
```yaml
$ vim sample-monitoringVNF.yaml
tosca_definitions_version: tosca_simple_profile_for_nfv_1_0_0
description: monitoringVNF
metadata:
  template_name: sample-monitoringVNF

topology_template:
  node_templates:
    VDU1:
      type: tosca.nodes.nfv.VDU.Tacker
      capabilities:
        nfv_compute:
          properties:
            num_cpus: 1
            mem_size: 4096 MB
            disk_size: 15 GB
      properties:
        image: cirros
        availability_zone: nova
        mgmt_driver: noop
        key_name: Titan
        config: |
          param0: key1
          param1: key2
        monitoring_policy:
          name: ping
          parameters:
            monitoring_delay: 10
            count: 3
            interval: 2
            timeout: 2
            action:
              failure: respawn
            retry: 5
            port: 22

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
        network_name: net_mgmt
        vendor: Tacker
```
## 執行
```shell
$ openstack vnf descriptor create --vnfd-file sample-monitoringVNF.yaml sample-monitoringVNF
$ openstack vnf create --vnfd-name sample-monitoringVNF monitoringVNF-demo
```