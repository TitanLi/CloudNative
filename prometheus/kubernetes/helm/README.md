# Helm
Source : [https://github.com/helm/charts/tree/master/stable/prometheus-operator](https://github.com/helm/charts/tree/master/stable/prometheus-operator)

---

## Helm version 2
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
## Add the stable repository
```shell
$ helm repo add stable https://kubernetes-charts.storage.googleapis.com
"stable" has been added to your repositories

$ $ helm repo list
NAME    URL
stable  https://kubernetes-charts.storage.googleapis.com
```
## Get the latest information
```shell
$ helm repo up
```
## Install the stable/prometheus-operator
> 執行會稍微久一些，要等一下 <br>
> 可用以下命令觀察部署狀態 <br>
> $ watch kubectl get pod --namespace=monitoring
```shell
$ helm install stable/prometheus-operator --name=monitoring --namespace=monitoring

....
NOTES:
The Prometheus Operator has been installed. Check its status by running:
  kubectl --namespace monitoring get pods -l "release=monitoring"

Visit https://github.com/coreos/prometheus-operator for instructions on how
to create & configure Alertmanager and Prometheus instances using the Operator.
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
> prometheus dashboard <br>
> [http://192.168.2.96:9090](http://192.168.2.96:9090)
```shell
$ kubectl port-forward --address=0.0.0.0 svc/monitoring-prometheus-oper-prometheus 9090:9090 --namespace=monitoring
```
> grafana dashboard <br>
> [http://192.168.2.96/](http://192.168.2.96/) <br>
> user : admin <br>
> password : prom-operator
```shell
$ kubectl port-forward --address=0.0.0.0 svc/monitoring-grafana 80:80 --namespace=monitoring
```

## Uninstalling the Chart
```shell
$ kubectl get crd --all-namespaces
$ kubectl delete crd prometheuses.monitoring.coreos.com
$ kubectl delete crd prometheusrules.monitoring.coreos.com
$ kubectl delete crd servicemonitors.monitoring.coreos.com
$ kubectl delete crd podmonitors.monitoring.coreos.com
$ kubectl delete crd alertmanagers.monitoring.coreos.com
$ kubectl delete crd thanosrulers.monitoring.coreos.com
```

---
## Helm version 3
helm 3安裝教學：[https://www.linode.com/docs/kubernetes/how-to-install-apps-on-kubernetes-with-helm-3/](https://www.linode.com/docs/kubernetes/how-to-install-apps-on-kubernetes-with-helm-3/)
## Installing Helm
```shell
$ curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 > get_helm.sh

$ chmod 700 get_helm.sh

$ ./get_helm.sh
```
## Add the stable repository
```shell
$ helm repo add stable https://kubernetes-charts.storage.googleapis.com/
```
## Update the repo to ensure you get the latest chart version
```shell
$ helm repo update
```
## The full name for the chart is stable/prometheus-operator. You can inspect the chart for more information
```shell
$ helm show readme stable/prometheus-operator
```
## Install the stable/prometheus-operator
> 執行會稍微久一些，要等一下 <br>
> 可用以下命令觀察部署狀態 <br>
> $ watch kubectl get pod --namespace=monitoring
```shell
$ kubectl create ns monitoring
$ helm install stable/prometheus-operator --namespace=monitoring --generate-name
```

## Port-forward
```shell
$ kubectl get service --namespace=monitoring
NAME                                                      TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)                      AGE
alertmanager-operated                                     ClusterIP   None             <none>        9093/TCP,9094/TCP,9094/UDP   2m
prometheus-operated                                       ClusterIP   None             <none>        9090/TCP                     110s
prometheus-operator-158503-alertmanager                   ClusterIP   10.102.215.52    <none>        9093/TCP                     2m23s
prometheus-operator-158503-operator                       ClusterIP   10.106.176.57    <none>        8080/TCP,443/TCP             2m23s
prometheus-operator-158503-prometheus                     ClusterIP   10.99.44.15      <none>        9090/TCP                     2m23s
prometheus-operator-1585033539-grafana                    ClusterIP   10.105.91.165    <none>        80/TCP                       2m23s
prometheus-operator-1585033539-kube-state-metrics         ClusterIP   10.101.109.248   <none>        8080/TCP                     2m23s
prometheus-operator-1585033539-prometheus-node-exporter   ClusterIP   10.110.54.99     <none>        9100/TCP                     2m23s
```
> prometheus dashboard <br>
> [http://192.168.2.96:9090](http://192.168.2.96:9090)
```shell
$ kubectl port-forward --address=0.0.0.0 svc/prometheus-operator-158503-prometheus9090:9090 --namespace=monitoring
```
> grafana dashboard <br>
> [http://192.168.2.96/](http://192.168.2.96/) <br>
> user : admin <br>
> password : prom-operator
```shell
$ kubectl port-forward --address=0.0.0.0 svc/prometheus-operator-1585033539-grafana 80:80 --namespace=monitoring
```
> 圖片標題 -> Share -> Direct link rendered image -> 複製URL <br>
> 下載grafana dashboard圖片：curl 'http://admin:prom-operator@192.168.2.96/render/d-solo/a87fb0d919ec0ea5f6543124e16c42a5/kubernetes-compute-resources-namespace-workloads?orgId=1&refresh=10s&from=1585196236814&to=1585196536814&var-datasource=Prometheus&var-cluster=&var-namespace=monitoring&var-interval=4h&var-type=deployment&panelId=2&width=1000&height=500&tz=Asia%2FTaipei' -o Desktop/a.png