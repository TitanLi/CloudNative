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

# 常用指令
1. Pod
```shell
# 查看Pod詳細資訊
$ kubectl describe pod PodName
# 查看Pod資訊(NAME、READY、STATUS、RESTARTS、AGE、IP、NODE、NOMINATED NODE、READINESS、GATES)
$ kubectl get pod -o wide
# 查看Pod label
$ kubectl get pod --show-labels
```
2. Deployment
```shell
# 更新deployment內容
$ kubectl edit deployment/Deployment-Name
# 查看部署狀態
$ kubectl rollout status deployment/Deployment-Name
# 查看更新紀錄
$ kubectl rollout history deployment/Deployment-Name
# 查看更新紀錄詳細訊息
# revision為歷史紀錄編號
$ kubectl rollout history deployment/Deployment-Name --revision=2
# 回滾到以前的版本
# --to-revision可指定滾回版本
$ kubectl rollout undo deployment/Deployment-Name
# 擴展部署(Scale out)
$ kubectl scale deployment Deployment-Name --replicas=10
# 更新container image version
# nodejs-api-app為container name
# nodejs-api:v2為欲更新的image版本
$ kubectl set image deployment api-deployment nodejs-api-app=nodejs-api:v2 --record
# 查看rollout狀態
$ kubectl rollout status deployments api-deployment
```
3. ReplicaSet
```shell
# 查看ReplicaSet細節
$ kubectl describe rs api-deployment-fd8d6c998
```
4. namespace
```shell
# 建立新的namespace
$ kubectl create namespace deployment-test
# 在deployment-test namespace中建立deployment
$ kubectl -n deployment-test apply -f api-deployment.yaml 
```