# Deployment
1. Create a Deployment based on the YAML file
```shell
$ kubectl apply -f deployment.yaml
```
2. Display information about the Deployment
```shell
$ kubectl describe deployment nginx-deployment
```
3. Display information about a pod
```shell
$ kubectl get pod
$ kubectl describe pod nginx-deployment-54f57cf6bf-bxp4s
```
4. Change deployment replica
```shell
$ kubectl edit deployment nginx-deployment
spec:
  progressDeadlineSeconds: 600
  replicas: 4
  
$ watch kubectl get pod
```
5. Edit deployment.yaml
> mountPath會指向Pod運行的主機

> 可用kubectl get pod -o wide查看Pod在哪台主機上
```yaml
$ vim deployment.yaml

...
    spec:
      containers:
        - name: nginx
          image: nginx:1.7.9
          ports:
            - containerPort: 80
          volumeMounts:
            - name: web-persistent-storage # 需與volumes name對應
              mountPath: /usr/share/nginx/html/
      volumes:
        - name: web-persistent-storage
          persistentVolumeClaim:
            claimName: web-pv-claim # 需與pvc metadata name對應

$ kubectl apply -f deployment.yaml
```
6. Add a volume on web path
```shell
$ cat <<EOF > pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: web-pv-claim
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 20Gi
EOF

$ cat <<EOF > pv.yaml
kind: PersistentVolume
apiVersion: v1
metadata:
  name: web-pv-volume
  labels:
    type: local
spec:
  capacity:
    storage: 20Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: "/mnt/"
EOF

$ kubectl apply -f pv.yaml
$ kubectl apply -f pvc.yaml
```
7. Add a index.html in /mnt/
```shell
$ cd /mnt/

cat <<EOF > index.html 
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
</head>
<body>
<h1>Apple</h1>
</body>
</html>
EOF
```