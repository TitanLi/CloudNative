# NSD
[TOSCA Simple Profile for Network Functions Virtualization (NFV) Version 1.0](http://docs.oasis-open.org/tosca/tosca-nfv/v1.0/csd03/tosca-nfv-v1.0-csd03.html)

[Orchestrating VNFs and VNFFG using Network Services Descriptor (NSD)](https://docs.openstack.org/tacker/latest/user/nsd_usage_guide.html)

## Using NSD to create VNFs
### Create VNFD
```shell
$ openstack vnf descriptor create --vnfd-file sample-tosca-vnfd1.yaml sample-tosca-vnfd1
$ openstack vnf descriptor create --vnfd-file sample-tosca-vnfd2.yaml sample-tosca-vnfd2
```
### Onboard the above NSD, then create NS from NSD
```shell
$ openstack ns descriptor create --nsd-file sample-tosca-nsd.yaml NSD-template
$ openstack ns create --nsd-name NSD-template --param-file ns_param.yaml NS1
```
### Create NS directly from NSD
```shell
$ openstack ns create --nsd-template tosca-multiple-vnffg-nsd.yaml --param-file ns_param.yaml NS2
```
### 常用指令
```shell
$ openstack ns list --fit-width
$ openstack vnf graph list --fit-width
$ openstack vnf list --fit-width
$ openstack vnf network forwarding path list
$ openstack sfc port chain list --fit-width
```