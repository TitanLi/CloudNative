# CORD
[CORD部署教學](https://guide.opencord.org/cord-6.1/linux.html)

[kubernetes-service](https://github.com/opencord/kubernetes-service)

[simpleexampleservice](https://github.com/opencord/simpleexampleservice)

[Core Models](https://guide.xosproject.org/core_models.html)

[core.xproto](https://github.com/opencord/xos/blob/master/xos/core/models/core.xproto)

## 1. CORD 安裝
> 須先安裝完Kubernetes環境

### 1.1 Install Python
```
$ sudo apt update
$ sudo apt-get install -y python
$ sudo apt-get install -y python-pip
$ pip install requests
```

### 1.2 Download CORD
```
$ mkdir ~/cord
$ cd ~/cord
$ git clone https://gerrit.opencord.org/helm-charts
$ cd helm-charts

$ mkdir ~/bin
$ PATH=~/bin:$PATH

$ curl https://storage.googleapis.com/git-repo-downloads/repo > ~/bin/repo
$ chmod a+x ~/bin/repo

$ mkdir ~/cord
$ cd ~/cord

// $ repo init -u https://gerrit.opencord.org/manifest -b master
// $ repo sync
```

### 1.3 Helm
```
$ curl https://raw.githubusercontent.com/kubernetes/helm/master/scripts/get > get_helm.sh
$ chmod 700 get_helm.sh
$ ./get_helm.sh
```

### 1.4 Tiller
```
$ sudo helm init
$ sudo kubectl create serviceaccount --namespace kube-system tiller
$ sudo kubectl create clusterrolebinding tiller-cluster-rule --clusterrole=cluster-admin --serviceaccount=kube-system:tiller
$ sudo kubectl patch deploy --namespace kube-system tiller-deploy -p '{"spec":{"template":{"spec":{"serviceAccount":"tiller"}}}}'
$ sudo helm init --service-account tiller --upgrade

$ sudo apt-get install socat

$ helm ls
```

### 1.5 Deploy CORD Helm Charts
```
$ cd ~/cord/helm-charts
$ helm init
$ sudo helm dep update xos-core
$ sudo helm install xos-core -n xos-core
$ sudo helm dep update xos-profiles/base-kubernetes
$ sudo helm install xos-profiles/base-kubernetes -n base-kubernetes
```

### 1.6 查看部署狀態
```
$ watch kubectl get pod
Every 2.0s: kubectl get pod                                                                               Mon Jun 24 03:57:00 2019

NAME                                          READY   STATUS      RESTARTS   AGE
base-kubernetes-kubernetes-658d57d549-pgg8b   1/1     Running     0          3m
base-kubernetes-tosca-loader-55zxt            0/1     Completed   0          3m
xos-chameleon-6754f7bcd8-b9nx8                1/1     Running     0          3m12s
xos-core-6f5b55697d-sgqv5                     1/1     Running     0          3m12s
xos-db-66f95c59c7-jqgqv                       1/1     Running     0          3m12s
xos-gui-7c94ffb99c-4pbs8                      1/1     Running     0          3m12s
xos-tosca-f5468cc74-8jlvh                     1/1     Running     0          3m12s
xos-ws-7746c588d9-srwhp                       1/1     Running     0          3m12
```


## 製作CORD simpleexampleservice synchronizer service
### 1. git clone simpleexampleservice project
```
$ git clone https://github.com/opencord/simpleexampleservice.git
```

### 2. 編輯config.yaml
```
$ vim xos/synchronizer/config.yaml

accessor:
  username: admin@opencord.org
  password: letmein
  endpoint: xos-core:50051
```

### 3. 新增service-synchronizer.yaml（for kubernetes）
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

### 4. Build Docker image
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

### 5. 啟用synchronizer
```
$ kubectl apply -f test-synchronizer.yaml
deployment.apps/test-synchronizer created

$ kubectl get pod
test-synchronizer-859cd968bf-jjbzw         1/1     Running     0          40s

$ watch kubectl logs test-synchronizer-859cd968bf-jjbzw
```

### 6. 登入CORD Dashboard
[10.0.1.97:30001](10.0.1.97:30001)

username: admin@opencord.org

password: letmein

### 刪除環境
```
helm delete --purge base-kubernetes
helm delete --purge xos-core
kubectl delete --all pods
```

## TOSCA
### Data Model
[core.xproto](https://github.com/opencord/xos/blob/master/xos/core/models/core.xproto)

[kubernetes-service](https://github.com/opencord/kubernetes-service/blob/master/xos/synchronizer/models/kubernetes.xproto)

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

### 技巧
1. 當應填入值提示為Set of key,value pairs encoded as a json dictionary使用以下方式解決

將yaml轉成json後填入
[json to yaml](https://www.json2yaml.com/)