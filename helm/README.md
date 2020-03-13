# Helm
> 參考資料：[https://www.digitalocean.com/community/tutorials/how-to-install-software-on-kubernetes-clusters-with-the-helm-package-manager](https://www.digitalocean.com/community/tutorials/how-to-install-software-on-kubernetes-clusters-with-the-helm-package-manager)
## Installing Helm
```shell
$ cd /tmp
$ curl https://raw.githubusercontent.com/kubernetes/helm/master/scripts/get > install-helm.sh
$ chmod u+x install-helm.sh
$ ./install-helm.sh
```
## Installing Tiller
1. Create the tiller serviceaccount
```shell
$ kubectl -n kube-system create serviceaccount tiller
```
2. Bind the tiller serviceaccount to the cluster-admin role
```shell
$ kubectl create clusterrolebinding tiller --clusterrole cluster-admin --serviceaccount=kube-system:tiller
```
3. Init
```shell
$ helm init --service-account tiller
```
4. Verify
```shell
$ kubectl get pods --namespace kube-system
tiller-deploy-5b4685ffbf-n4n7p          1/1     Running   0          14m
```
## Get the latest helm chart repo
```shell
$ helm repo up
```
## Search for available versions for a given stable
```shell
$ helm search stable/prometheus-operator --versions --version=">=4.3" --col-width=20
```
## Deploy Prometheus into the monitoring namespace
```shell
$ helm install stable/prometheus-operator --version=4.3.6 --name=monitoring --namespace=monitoring
```
## List
```shell
$ helm list
NAME      	REVISION	UPDATED                 	STATUS  	CHART            	APP VERSION	NAMESPACE 
prometheus	1       	Thu Mar  5 05:34:47 2020	DEPLOYED	prometheus-11.0.1	2.16.0     	monitoring
```
## Delete
```shell
$ helm delete prometheus
```