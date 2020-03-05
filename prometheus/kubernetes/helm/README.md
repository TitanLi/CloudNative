# Helm
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
## Get the latest information
```shell
$ helm repo up
```
## Install the stable/prometheus-operator
```shell
$ helm install stable/prometheus-operator --name=monitoring --namespace=monitoring
```
## Get service
```shell
$ kubectl get service --namespace=monitoring
NAME                                      TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)                      AGE
alertmanager-operated                     ClusterIP   None             <none>        9093/TCP,9094/TCP,9094/UDP   19m
monitoring-grafana                        ClusterIP   10.103.63.80     <none>        80/TCP                       19m
monitoring-kube-state-metrics             ClusterIP   10.101.170.206   <none>        8080/TCP                     19m
monitoring-prometheus-node-exporter       ClusterIP   10.111.125.151   <none>        9100/TCP                     19m
monitoring-prometheus-oper-alertmanager   ClusterIP   10.106.207.77    <none>        9093/TCP                     19m
monitoring-prometheus-oper-operator       ClusterIP   10.99.31.157     <none>        8080/TCP,443/TCP             19m
monitoring-prometheus-oper-prometheus     ClusterIP   10.100.165.113   <none>        9090/TCP                     19m
prometheus-operated                       ClusterIP   None             <none>        9090/TCP                     18m
```
## Port-forward
> prometheus dashboard
```shell
$ kubectl port-forward --address=0.0.0.0 svc/monitoring-prometheus-oper-prometheus 9090:9090 --namespace=monitoring
```