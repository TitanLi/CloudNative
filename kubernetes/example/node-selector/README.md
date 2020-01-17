# nodeSelector
## 查詢現有Node標籤
```shell
$ kubectl get nodes --show-labels
NAME     STATUS   ROLES    AGE     VERSION   LABELS
titan1   Ready    master   2d19h   v1.17.0   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=titan1,kubernetes.io/os=linux,node-role.kubernetes.io/master=
titan3   Ready    <none>   2d19h   v1.17.0   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=titan3,kubernetes.io/os=linux
titan4   Ready    <none>   2d19h   v1.17.0   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=titan4,kubernetes.io/os=linux
titan6   Ready    <none>   2d19h   v1.17.0   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=titan6,kubernetes.io/os=linux
```
## 新增標籤
```shell
$ kubectl label node <node name> <label>=<value>
$ kubectl label node titan3 networkSpeed=high
$ kubectl label node titan4 networkSpeed=high
$ kubectl label node titan6 networkSpeed=low
```
## 確認labels新增結果
```shell
$ kubectl get nodes --show-labels
NAME     STATUS   ROLES    AGE     VERSION   LABELS
titan1   Ready    master   2d19h   v1.17.0   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=titan1,kubernetes.io/os=linux,node-role.kubernetes.io/master=
titan3   Ready    <none>   2d19h   v1.17.0   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=titan3,kubernetes.io/os=linux,networkSpeed=high
titan4   Ready    <none>   2d19h   v1.17.0   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=titan4,kubernetes.io/os=linux,networkSpeed=high
titan6   Ready    <none>   2d19h   v1.17.0   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=titan6,kubernetes.io/os=linux,networkSpeed=low
```
## 建立測試用 Deployment
```shell
$ vim deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  selector:
    matchLabels:
      app: nginx
  replicas: 7
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
        - name: nginx
          image: nginx:1.7.9
          ports:
            - containerPort: 80
      nodeSelector:
        networkSpeed: "high"
```
## 確認Pods放置節點
```shell
$ kubectl get pod -o wide
NAME                                READY   STATUS    RESTARTS   AGE     IP             NODE     NOMINATED NODE   READINESS GATES
nginx-deployment-7d5978b7f7-95zj7   1/1     Running   0          18m     10.244.2.128   titan4   <none>           <none>
nginx-deployment-7d5978b7f7-g2r7b   1/1     Running   0          17m     10.244.2.129   titan4   <none>           <none>
nginx-deployment-7d5978b7f7-kqpv6   1/1     Running   0          17m     10.244.2.130   titan4   <none>           <none>
nginx-deployment-7d5978b7f7-l7rwd   1/1     Running   0          18m     10.244.1.130   titan3   <none>           <none>
nginx-deployment-7d5978b7f7-pz2nl   1/1     Running   0          17m     10.244.1.131   titan3   <none>           <none>
nginx-deployment-7d5978b7f7-t94sm   1/1     Running   0          9m28s   10.244.2.131   titan4   <none>           <none>
nginx-deployment-7d5978b7f7-vhr6p   1/1     Running   0          17m     10.244.1.132   titan3   <none>           <none>
```
## 移除標籤
> You can remove incorrect label with <label>-
```shell
$ kubectl label node titan6 networkSpeed-
```