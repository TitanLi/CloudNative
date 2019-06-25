# kube5gc

## Install OVS on node host and Add interface to OVS
```
$ apt install openvswitch-switch
$ ovs-vsctl add-br br0
$ ovs-vsctl add-port br0 ens3

$ vim /etc/network/interfaces.d/50-cloud-init.cfg
# 新增以下內容
auto br0
iface br0 inet static
    address 192.168.2.100
    netmask 255.255.0.0
    bridge_ports enp4s0
    bridge_fd 9
    bridge_hello 2
    bridge_maxage 12
    ridge_stp off

$ sudo service networking restart

$ kubectl apply -f ./mongoDB/free5gc-mongodb.yaml
$ kubectl apply -f ./config

# $ kubectl get pod -n kube-system

$ kubectl apply -f free5gc-amf.yaml
```