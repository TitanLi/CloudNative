# Kubernetes
## 1. 更新套件 (Master, Node)
```
$ apt-get update
```
## 2. Install Docker (Master, Node)
```
$ apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common

$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -

$ apt-key fingerprint 0EBFCD88

$ add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

$ apt-get update

$ apt-get install -y docker-ce docker-ce-cli containerd.io
```
## 3. 查看Docker狀態 (Master, Node)
```
$ service docker status
● docker.service - Docker Application Container Engine
   Loaded: loaded (/lib/systemd/system/docker.service; enabled; vendor preset: enabled)
   Active: active (running) since Mon 2019-06-24 03:31:00 UTC; 3s ago
     Docs: https://docs.docker.com
 Main PID: 5356 (dockerd)
   CGroup: /system.slice/docker.service
           └─5356 /usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.sock
```

## 4. Install Kubernetes kubelet, kubeadm, kubectl (Master, Node)
> 需更改DNS

> vim /etc/resolv.conf

> nameserver 8.8.8.8

```
$ apt-get update && apt-get install -y apt-transport-https curl

$ curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -

$ cat <<EOF >/etc/apt/sources.list.d/kubernetes.list
deb https://apt.kubernetes.io/ kubernetes-xenial main
EOF

$ apt-get update

$ apt-get install -y kubelet kubeadm kubectl

# Turn off swap area
$ swapoff -a
```

## 5. Initializing your master and create a cluster (Master)
```
$ kubeadm init --pod-network-cidr=10.244.0.0/16
```

## 6. To start using your cluster, you need to run the following as a regular user (Master)
```
$ mkdir -p $HOME/.kube
$ cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
$ chown $(id -u):$(id -g) $HOME/.kube/config
```

## 7-1 Node isolation (Single Node)
```
$ kubectl taint nodes --all node-role.kubernetes.io/master-
```

## 7-2 Join your node (Node)
```
$ kubeadm join 10.0.1.97:6443 --token 8jh9ea.n9ap6l78kdlknop2 \
    --discovery-token-ca-cert-hash sha256:23f9c3d418db8c334a213cc72cd540de245f37271abebf6f4b5acd8e05dd2ba2 
```

## 7-3 查看join command (Master)
```
$ kubeadm token create --print-join-command
kubeadm join 10.0.1.11:6443 --token qar5kk.j4nnd3rpidzvvpyl --discovery-token-ca-cert-hash sha256:4ef1b9452e6535deb38ce627481d1ae2fb69a6f68e1a235692f055c9ec7b1c80
```

## 8. Installing a pod network add-on (Master)
> CNI Plugin - Flannel
```
$ kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
```

## 9. Check your master node is ready (Master)
```
$ watch kubectl get node
```

## Uninstall
```shell
$ kubeadm reset
```