# Using NSD to create VNFs and single VNFFG
參考資料：[https://docs.openstack.org/tacker/rocky/user/nsd_usage_guide.html](https://docs.openstack.org/tacker/rocky/user/nsd_usage_guide.html)
## Create VNFD
```shell
$ openstack vnf descriptor create --vnfd-file tosca-vnfd1-sample.yaml sample-vnfd1
$ openstack vnf descriptor create --vnfd-file tosca-vnfd2-sample.yaml sample-vnfd2
```
## Find http_client(IP:10.20.0.4),http_server port(IP:10.20.0.2)
```shell
# http_client port ID
$ openstack port list | grep 10.20.0.4
d0f4f11e-d4e1-43fc-900d-d65533133f17

# http_server port ID
$ openstack port list | grep 10.20.0.2
3316010b-d7a2-4a8b-a80a-1a915066260f
```
## Onboard the above NSD, then create NS from NSD
```shell
# Onboard the above NSD
$ openstack ns descriptor create --nsd-file tosca-single-vnffg-nsd.yaml NSD-VNFFG-template
# Create NS from NSD
$ openstack ns create --nsd-name NSD-VNFFG-template --param-file ns_param.yaml NS2
```
## 常用指令
```shell
$ openstack ns list --fit-width
$ openstack vnf graph list --fit-width
$ openstack vnf list --fit-width
$ openstack vnf network forwarding path list
$ openstack sfc port chain list --fit-width
```