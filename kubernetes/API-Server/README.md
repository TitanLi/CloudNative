# API Server
> NodeJS API Server使用Kubernetes Deployment運行
> 使用Service將Port對外
## Docker Build
```shell
$ docker build -t nodejs-api ./dockerfile
```

## Run Pod
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
  labels:
    app: myapp
spec:
  containers:
  - name: myapp-container
    image: nodejs-api
    imagePullPolicy: IfNotPresent
    command: ['pm2-runtime','app.js']
```

## Run Deployment
1. 建立Yaml
```yaml
$ vim api-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-deployment
  labels:
    name: api
spec:
  replicas: 2 # 搭配ReplicaSet產生2個Pod
  selector:
    matchLabels: # 挑選帶有app=api的Pod,必需與下方的Pod label相符合
      app: api
  template:
    metadata: # Pod metadata
      labels: # 設定Pod的label資訊
        app: api
    spec:
      containers:
        - name: nodejs-api-app
          image: nodejs-api
          imagePullPolicy: IfNotPresent
          command: ['node','app.js']
          ports:
            - containerPort: 3000

$ vim api-service.yaml
apiVersion: v1
kind: Service
metadata:
    name: api-service # 服務名稱
spec:
  selector:
    app: api # 找到對應的Pod
  ports:
  - name: http-api  # 讓維運人員讀取
    protocol: TCP
    port: 3000
  - name: https-api # 讓維運人員讀取
    port: 443
    protocol: TCP
  type: NodePort
```
2. Apply
```shell
$ kubectl apply -f api.yaml 
service/api-service created
```
3. get service
```shell
$ kubectl get service
NAME          TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
api-service   NodePort    10.111.190.67   <none>        3000:30624/TCP   3s
kubernetes    ClusterIP   10.96.0.1       <none>        443/TCP          7h46m
```
4. curl
```shell
$ curl 192.168.2.94:30624/?apple=1
$ curl 192.168.2.97:30624/?apple=1
```