# Kubernetes部署
[Kubernetes基本介紹](https://www.inwinstack.com/2018/05/08/what-is-kubernetes-part2/?fbclid=IwAR2HmDMpb9rf8jAzskQsyPQ4eWlgUUy7-YN9hI1qtUIurGISkDO9jn22RZ8)

[常用指令](http://kubernetes.kansea.com/docs/user-guide/kubectl/kubectl_stop/)

## Docker安裝
[Docker安裝教學](https://kubernetes.io/docs/setup/cri/?fbclid=IwAR37EeobqeFcsA3-IOqrgBTtFsFJawzy-XGmmaC79ip2FJSmhLU48QB-b_U)
### Install Docker CE Set up the repository:
#### Update the apt package index
```
$ apt-get update
```
#### Install packages to allow apt to use a repository over HTTPS
```
$ apt-get update && apt-get install apt-transport-https ca-certificates curl software-properties-common
```
#### Add Docker’s official GPG key
```    
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
```
#### Add docker apt repository.
```
$ add-apt-repository \
  "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) \
  stable"
```
#### Install docker ce.
```
$ apt-get update && apt-get install docker-ce=18.06.0~ce~3-0~ubuntu -y
```
#### Setup daemon.
```
$ cat > /etc/docker/daemon.json <<EOF
{
  "exec-opts": ["native.cgroupdriver=systemd"],
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "100m"
  },
  "storage-driver": "overlay2"
}
EOF

$ mkdir -p /etc/systemd/system/docker.service.d
```
#### Restart docker
```
$ systemctl daemon-reload
$ systemctl restart docker
```
## 關閉swap
```
$ free
$ swapoff -a
```
## 編輯DNS
```
$ vim /etc/resolv.conf
更改 nameserver 8.8.8.8
```
## Install kubeadm、kubelet、kubectl(每個node)
[Installing kubeadm, kubelet and kubectl](https://kubernetes.io/docs/setup/independent/install-kubeadm/?fbclid=IwAR1h7m0h4gocNzWkvdKcEiZjh4gI3_vkT4TrQHtV44LdMBj-zRdLsQ1z7-I)
```
$ apt-get update && apt-get install -y apt-transport-https curl
$ curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
$ cat <<EOF >/etc/apt/sources.list.d/kubernetes.list
deb https://apt.kubernetes.io/ kubernetes-xenial main
EOF
$ apt-get update
$ apt-get install -y kubelet kubeadm kubectl
$ apt-mark hold kubelet kubeadm kubectl
```

## 初始化(在master做)
[官方教學](https://kubernetes.io/docs/setup/independent/create-cluster-kubeadm/?fbclid=IwAR2duJe2XRO1lOX367yItDvCkOBJrYVMwRG7xzUw3ZlcFyIB71o7S5Zb9ZI)

```
# 在者邊因為要與OpenStack kuryr溝通，必須依照環境做出相關設定
$ kubeadm init --pod-network-cidr=10.1.0.0/16 --service-cidr=10.2.0.0/16

Your Kubernetes master has initialized successfully!

To start using your cluster, you need to run the following as a regular user:

  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config

You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
  https://kubernetes.io/docs/concepts/cluster-administration/addons/

You can now join any number of machines by running the following on each node
as root:

  kubeadm join 10.0.1.98:6443 --token jubkkp.wfjrcn9lonvaqrj8 --discovery-token-ca-cert-hash sha256:10a4ffe174ae991a624be0f48d260c004c833ed4dc5415f5515ff49664633971
```
## 設定環境參數
```
$ vim k8s
加入以下內容
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

$ . k8s
```
## 查看狀態
```
$ kubectl get nodes
NAME     STATUS     ROLES    AGE     VERSION
titan2   NotReady   master   3m53s   v1.13.4
```

## 到node join(到node執行，讓master發現node)
```
# 可在master查看join command
# $ kubeadm token create --print-join-command
# kubeadm join 10.0.1.98:6443 --token 84e03f.7iflrbivnucctzcm --discovery-token-ca-cert-hash sha256:10a4ffe174ae991a624be0f48d260c004c833ed4dc5415f5515ff49664633971

# 在每個node執行
$ kubeadm join 10.0.1.98:6443 --token 84e03f.7iflrbivnucctzcm --discovery-token-ca-cert-hash sha256:10a4ffe174ae991a624be0f48d260c004c833ed4dc5415f5515ff49664633971
```

## 查看狀態
```
$ kubectl get node
NAME     STATUS     ROLES    AGE    VERSION
titan2   NotReady   master   35m    v1.13.4
titan3   NotReady   <none>   9m4s   v1.13.4
```

## 建立 flannel CNI(在master執行)
[https://kubernetes.io/docs/setup/independent/create-cluster-kubeadm/](https://kubernetes.io/docs/setup/independent/create-cluster-kubeadm/)
Flannel
```
$ curl -OL https://raw.githubusercontent.com/coreos/flannel/a70459be0084506e4ec919aa1c114638878db11b/Documentation/kube-flannel.yml

# 把kube-flannel.yml裡面的10.244.0.0/16取代成10.1.0.0/16
$ vim kube-flannel.yml

$ kubectl apply -f kube-flannel.yml
```

## 查看狀態
```
$ kubectl get nodes
NAME     STATUS   ROLES    AGE   VERSION
titan2   Ready    master   36m   v1.13.4
titan3   Ready    <none>   10m   v1.13.4
```

## 常用指令
```
$ kubectl api-resources

NAME                              SHORTNAMES   APIGROUP                       NAMESPACED   KIND
bindings                                                                      true         Binding
componentstatuses                 cs                                          false        ComponentStatus
configmaps                        cm                                          true         ConfigMap
endpoints                         ep                                          true         Endpoints
events                            ev                                          true         Event
```
```
$ kubectl get pod -n kube-system -o wide

NAME                             READY   STATUS    RESTARTS   AGE    IP          NODE     NOMINATED NODE   READINESS GATES
coredns-86c58d9df4-6td9b         1/1     Running   0          114m   10.1.1.2    titan2   <none>           <none>
coredns-86c58d9df4-82qgw         1/1     Running   0          114m   10.1.1.3    titan2   <none>           <none>
etcd-titan1                      1/1     Running   0          113m   10.0.1.97   titan1   <none>           <none>
kube-apiserver-titan1            1/1     Running   0          113m   10.0.1.97   titan1   <none>           <none>
kube-controller-manager-titan1   1/1     Running   0          113m   10.0.1.97   titan1   <none>           <none>
kube-flannel-ds-amd64-6zmbp      1/1     Running   0          63m    10.0.1.98   titan2   <none>           <none>
kube-flannel-ds-amd64-s6gxd      1/1     Running   0          63m    10.0.1.97   titan1   <none>           <none>
kube-proxy-rgzlg                 1/1     Running   0          107m   10.0.1.98   titan2   <none>           <none>
kube-proxy-xddbp                 1/1     Running   0          114m   10.0.1.97   titan1   <none>           <none>
kube-scheduler-titan1            1/1     Running   0          113m   10.0.1.97   titan1   <none>           <none>
```
```
$ kubectl get svc --all-namespaces -o wide

NAMESPACE     NAME         TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)         AGE    SELECTOR
default       kubernetes   ClusterIP   10.2.0.1     <none>        443/TCP         114m   <none>
kube-system   kube-dns     ClusterIP   10.2.0.10    <none>        53/UDP,53/TCP   113m   k8s-app=kube-dns
```
```
$ sudo cat /etc/kubernetes/manifests/kube-apiserver.yaml

apiVersion: v1
kind: Pod
metadata:
  annotations:
    scheduler.alpha.kubernetes.io/critical-pod: ""
  creationTimestamp: null
  labels:
    component: kube-apiserver
    tier: control-plane
  name: kube-apiserver
  namespace: kube-system
spec:
  containers:
  - command:
    - kube-apiserver
    - --authorization-mode=Node,RBAC
    - --advertise-address=10.0.1.97
    - --allow-privileged=true
    - --client-ca-file=/etc/kubernetes/pki/ca.crt
    - --enable-admission-plugins=NodeRestriction
    - --enable-bootstrap-token-auth=true
    - --etcd-cafile=/etc/kubernetes/pki/etcd/ca.crt
    - --etcd-certfile=/etc/kubernetes/pki/apiserver-etcd-client.crt
    - --etcd-keyfile=/etc/kubernetes/pki/apiserver-etcd-client.key
    - --etcd-servers=https://127.0.0.1:2379
```