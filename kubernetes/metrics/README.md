# Metrics
> metrics-server github:[https://github.com/kubernetes-sigs/metrics-server](https://github.com/kubernetes-sigs/metrics-server)
## 安裝Metrics Server
1. 取得相關Yaml文件
```shell
$ git clone https://github.com/kubernetes-incubator/metrics-server -b release-0.3
```

2. 修改部分內容
> 編輯metrics-server/deploy/1.8+/resource-reader.yaml 
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

> 編輯metrics-server/deploy/1.8+/metrics-server-deployment.yaml
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
        imagePullPolicy: Always
        args:                                                                 # 增加此行
        - --kubelet-insecure-tls                                              # 增加此行
        - --kubelet-preferred-address-types=InternalIP,ExternalIP,Hostname    # 增加此行
        volumeMounts:
        - name: tmp-dir
          mountPath: /tmp
```

3. 開始部署
```shell
$ kubectl apply -f metrics-server/deploy/1.8+/
```

4. Metrics Server相關Pod、Service默認部署於kube-system的namespace
```shell
$ kubectl get pods -n kube-system | grep metrics
metrics-server-5bfdbd678-74mjm   1/1     Running   0          32m

$ kubectl get svc -n kube-system | grep metrics
metrics-server   ClusterIP   10.108.56.144   <none>        443/TCP                  32m
```

5. 使用服務
> 需等一下
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

## 透過API與metrics溝通
> 此操作僅限localhost
1. 加入proxy
```shell
$ kubectl proxy --address='0.0.0.0' --port=8080 --accept-hosts='^*$'&
```
2. kubectl top nodes
```shell
$ curl http://localhost:8080/apis/metrics.k8s.io/v1beta1/nodes
{
  "kind": "NodeMetricsList",
  "apiVersion": "metrics.k8s.io/v1beta1",
  "metadata": {
    "selfLink": "/apis/metrics.k8s.io/v1beta1/nodes"
  },
  "items": [
    {
      "metadata": {
        "name": "titan1",
        "selfLink": "/apis/metrics.k8s.io/v1beta1/nodes/titan1",
        "creationTimestamp": "2020-02-25T07:05:27Z"
      },
      "timestamp": "2020-02-25T07:05:17Z",
      "window": "30s",
      "usage": {
        "cpu": "161437136n",
        "memory": "2699144Ki"
      }
    },
    {
      "metadata": {
        "name": "titan4",
        "selfLink": "/apis/metrics.k8s.io/v1beta1/nodes/titan4",
        "creationTimestamp": "2020-02-25T07:05:27Z"
      },
      "timestamp": "2020-02-25T07:05:20Z",
      "window": "30s",
      "usage": {
        "cpu": "86024960n",
        "memory": "1267124Ki"
      }
    }
  ]
}
```
3. kubectl top pods
```shell
$ curl http://localhost:8080/apis/metrics.k8s.io/v1beta1/namespaces/kube-system/pods 
{
  "kind": "PodMetricsList",
  "apiVersion": "metrics.k8s.io/v1beta1",
  "metadata": {
    "selfLink": "/apis/metrics.k8s.io/v1beta1/namespaces/kube-system/pods"
  },
  "items": [
    {
      "metadata": {
        "name": "metrics-server-75ff7565b5-4xptk",
        "namespace": "kube-system",
        "selfLink": "/apis/metrics.k8s.io/v1beta1/namespaces/kube-system/pods/metrics-server-75ff7565b5-4xptk",
        "creationTimestamp": "2020-02-25T07:06:45Z"
      },
      "timestamp": "2020-02-25T07:06:14Z",
      "window": "30s",
      "containers": [
        {
          "name": "metrics-server",
          "usage": {
            "cpu": "1102036n",
            "memory": "16784Ki"
          }
        }
      ]
    },
    ....
}
```