# VNFFGD
[Implement Tacker VNF Forwarding Graph](https://github.com/openstack/tacker-specs/blob/master/specs/newton/tacker-vnffg.rst)

```yaml
Forwarding_path1:
  type: tosca.nodes.nfv.FP
  id: 51
  description: creates path (CP11->CP12->CP32)
  properties:
    policy:
      type: ACL
      criteria:
        - neutron_net_name: tenant1_net
        - dest_port_range: 80-1024
        - ip_proto: tcp
        - ip_dest: 192.168.1.2
  requirements:
    - forwarder: VNF1
      capability: CP11
    - forwarder: VNF1
      capability: CP12
    - forwarder: VNF3
      capability: CP32

groups:
  VNFFG1:
    type: tosca.groups.nfv.VNFFG
    description: HTTP to Corporate Net
    properties:
      vendor: tacker
      version: 1.0
      number_of_endpoints: 5
      dependent_virtual_link: [VL1,VL2,VL3]
      connection_point: [CP11,CP12,CP32]
      constituent_vnfs: [VNF1,VNF3]
    members: [Forwarding_path1]
```