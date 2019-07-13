# ReplicationController
## 範例
[redis-master.yaml](https://github.com/TitanLi/CloudNative/tree/master/kubernetes/redis/redis-master-controller.yaml)
```
$ kubectl apply -f redis-master.yaml
$ kubectl get rc
$ kubectl get pods
```

# service
## 範例
[redis-master-service.yaml](https://github.com/TitanLi/CloudNative/tree/master/kubernetes/redis/redis-master-service.yaml)

```
$ kubectl apply -f redis-master-service.yaml
$ kubectl get services
$ kubectl get pods
```

# NodePort
## 範例
[frontend-service.yaml](https://github.com/TitanLi/CloudNative/tree/master/kubernetes/redis/frontend-service.yaml)

```
$ kubectl apply -f frontend-service.yaml
$ kubectl get services
$ kubectl get pods
```