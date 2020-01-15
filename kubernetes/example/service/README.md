# Service
1. Create a service resource
> 可搭配Deployment example
```shell
$ kubectl apply -f service.yaml
```
2. Look your service NodePort
```shell
$ kubectl get service
```
3. Use web browser to watch your service on Kubernetes, Enter on URL

[http://192.168.2.94:30307/](http://192.168.2.94:30307/)

4. Edit web file to verify that is load balance
```shell
$ kubectl exec nginx-deployment-54f57cf6bf-978zs bash
$ echo 1 >> /usr/share/nginx/html/index.html

$ kubectl exec -ti nginx-deployment-54f57cf6bf-bxp4s bash
$ echo 2 >> /usr/share/nginx/html/index.html

$ kubectl exec -ti nginx-deployment-54f57cf6bf-c46kp bash
$ echo 3 >> /usr/share/nginx/html/index.html

$ kubectl exec -ti nginx-deployment-54f57cf6bf-z46zd bash
$ echo 4 >> /usr/share/nginx/html/index.html
```