# Metrics
## 安裝Metrics Server
1. 取得相關Yaml文件
```shell
$ git clone https://github.com/kubernetes-incubator/metrics-server
```

2. 修改部分內容
> 編輯metrics-server/deploy/kubernetes/resource-reader.yaml
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: system:metrics-server
rules:
- apiGroups:
  - ""
  resources:
  - pods
  - nodes
  - namespaces      # 增加此行
  - nodes/stats
  verbs:
  - get
  - list
  - watch
```

> 編輯metrics-server/deploy/kubernetes/metrics-server-deployment.yaml
```yaml
spec:
  selector:
    matchLabels:
      k8s-app: metrics-server
  template:
    metadata:
      name: metrics-server
      labels:
        k8s-app: metrics-server
    spec:
      serviceAccountName: metrics-server
      volumes:
      # mount in tmp so we can safely use from-scratch images and/or read-only containers
      - name: tmp-dir
        emptyDir: {}
      containers:
      - name: metrics-server
        image: k8s.gcr.io/metrics-server-amd64:v0.3.6
        command:                                        # 增加此行
          - /metrics-server                             # 增加此行
          - --kubelet-insecure-tls                      # 增加此行
```

3. 開始部署
```shell
$ kubectl apply -f metrics-server/deploy/kubernetes/.
```

4. Metrics Server相關Pod、Service默認部署於kube-system的namespace
```shell
$ kubectl get pods -n kube-system | grep metrics
metrics-server-5bfdbd678-74mjm   1/1     Running   0          32m

$ kubectl get svc -n kube-system | grep metrics
metrics-server   ClusterIP   10.108.56.144   <none>        443/TCP                  32m
```

5. 使用服務
```shell
$ kubectl top nodes
NAME     CPU(cores)   CPU%   MEMORY(bytes)   MEMORY%   
titan1   79m          0%     756Mi           4%        
titan4   171m         2%     1041Mi          6% 

$ kubectl top pods -n kube-system
NAME                             CPU(cores)   MEMORY(bytes)   
coredns-6955765f44-4nq8m         4m           7Mi             
coredns-6955765f44-rqf8b         4m           7Mi             
etcd-titan4                      25m          37Mi            
kube-apiserver-titan4            55m          210Mi           
kube-controller-manager-titan4   26m          36Mi            
kube-flannel-ds-amd64-j6x8n      3m           12Mi            
kube-flannel-ds-amd64-xzsjb      4m           10Mi            
kube-proxy-c85z8                 1m           10Mi            
kube-proxy-stxhg                 1m           10Mi            
kube-scheduler-titan4            5m           12Mi            
metrics-server-5bfdbd678-74mjm   1m           12Mi
```