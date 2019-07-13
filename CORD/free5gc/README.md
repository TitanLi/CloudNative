# kube5gc

## Install OVS on node host and Add interface to OVS
```
$ apt install -y openvswitch-switch
$ ovs-vsctl add-br br0

# 第二張網卡
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

$ kubectl get pod -n kube-system
network-controller-server-unix-5cxwg   1/1     Running   0          39s
network-controller-server-unix-png47   1/1     Running   0          39s

$ kubectl get cm
free5gc-configmap                1      69s
free5gc-freediameter-configmap   2      68s

$ kubectl apply -f free5gc-amf.yaml

$ kubectl get pod
NAME                                      READY   STATUS    RESTARTS   AGE
free5gc-amf-deployment-68765894f6-pv6tz   1/1     Running   0          3m28s
free5gc-mongodb-76c49fdcf-hxnd5           1/1     Running   0          5m29s
```