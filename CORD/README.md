# CORD
[CORD部署教學](https://guide.opencord.org/cord-6.1/linux.html)

[kubernetes-service](https://github.com/opencord/kubernetes-service)

[simpleexampleservice](https://github.com/opencord/simpleexampleservice)

[Core Models](https://guide.xosproject.org/core_models.html)

[core.xproto](https://github.com/opencord/xos/blob/master/xos/core/models/core.xproto)

## 製作CORD simpleexampleservice synchronizer service
### git clone simpleexampleservice project
```
$ git clone https://github.com/opencord/simpleexampleservice.git
```

### 編輯config.yaml
```
$ vim xos/synchronizer/config.yaml

accessor:
  username: admin@opencord.org
  password: letmein
  endpoint: xos-core:50051
```

### 新增service-synchronizer.yaml（for kubernetes）
```
apiVersion: apps/v1beta2
kind: Deployment
metadata:
  name: service-synchronizer
  labels:
    app: service-synchronizer
spec:
  replicas: 1
  selector:
    matchLabels:
      app: service-synchronizer
  template:
    metadata:
      labels:
        app: service-synchronizer
    spec:
      containers:
        - name: free5gc-service
          image: lisheng0706/service-synchronizer
          imagePullPolicy: Always
          volumeMounts:
            - name: certchain-volume
              mountPath: /usr/local/share/ca-certificates/local_certs.crt
              subPath: config/ca_cert_chain.pem
      volumes:
        - name: certchain-volume
          configMap:
            name: ca-certificates
            items:
              - key: chain
                path: config/ca_cert_chain.pem
```

### Build Docker image
```
$ docker build -t lisheng0706/test-synchronizer -f Dockerfile.synchronizer --no-cache .

$ docker images
REPOSITORY                           TAG                 IMAGE ID            CREATED             SIZE
lisheng0706/test-synchronizer     latest              0abb27ff21d5        15 seconds ago      423MB

# 登入Docker hub
$ docker login
Login with your Docker ID to push and pull images from Docker Hub. If you don't have a Docker ID, head over to https://hub.docker.com to create one.
Username: 
Password: 
WARNING! Your password will be stored unencrypted in /root/.docker/config.json.
Configure a credential helper to remove this warning. See
https://docs.docker.com/engine/reference/commandline/login/#credentials-store

Login Succeede

$ docker push lisheng0706/test-synchronizer
```

### 啟用synchronizer
```
$ kubectl apply -f test-synchronizer.yaml
deployment.apps/test-synchronizer created

$ kubectl get pod
test-synchronizer-859cd968bf-jjbzw         1/1     Running     0          40s

$ watch kubectl logs test-synchronizer-859cd968bf-jjbzw
```

### 登入CORD Dashboard
[10.0.1.97:30001](10.0.1.97:30001)

username: admin@opencord.org

password: letmein

### 刪除環境
```
helm delete --purge base-kubernetes
helm delete --purge xos-core
```

## TOSCA
### Data Model
[core.xproto](https://github.com/opencord/xos/blob/master/xos/core/models/core.xproto)

### API Create
[TOSCA API](https://guide.opencord.org/cord-6.1/xos-tosca/)
```
curl -H "xos-username: admin@opencord.org" -H "xos-password: letmein"  -X POST --data-binary @make_service.yaml http://10.0.1.98:30007/run

curl -H "xos-username: admin@opencord.org" -H "xos-password: letmein"  -X POST --data-binary @make_service.yaml http://10.0.1.98:30007/delete
```

### custom_types
```
kubectl exec -ti xos-tosca-5b86cfb5bf-8rndt sh

/opt/xos-tosca/src/tosca/custom_types
```