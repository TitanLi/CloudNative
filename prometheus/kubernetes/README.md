# Prometheus
## 1. Run node-exporter
> namespace: kube-system <br>
> port: 9100
```shell
$ kubectl apply -f node-exporter-daemonset.yaml
```
## 2. Create configmap
> namespace: kube-system
```shell
$ kubectl apply -f prometheus-cm.yaml
```
## 3. Run prometheus
> namespace: kube-system <br>
> port: 9090 <br>
> targetPort: 9090 <br>
> nodePort: 30001
```shell
$ kubectl apply -f prometheus.yaml
```