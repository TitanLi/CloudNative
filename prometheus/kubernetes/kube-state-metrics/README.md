# kube-state-metrics
Source:[https://github.com/kubernetes/kube-state-metrics](https://github.com/kubernetes/kube-state-metrics)

## Git clone project
> git log --oneline <br>
> stable : afacea86
```shell
$ git clone https://github.com/kubernetes/kube-state-metrics
```
## Run Service
```shell
$ cd kube-state-metrics/examples
$ kubectl apply -f standard/
$ kubectl apply -f autosharding/
```
## Verification
kubectl get service --namespace kube-system
NAME                 TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)                  AGE
kube-state-metrics   ClusterIP   None          <none>        8080/TCP,8081/TCP        4s
## Port Forward
```shell
$ kubectl port-forward --address=0.0.0.0 svc/kube-state-metrics 8080 --namespace=kube-system
Forwarding from 0.0.0.0:8080 -> 8080

$ kubectl port-forward --address=0.0.0.0 svc/kube-state-metrics 8081 --namespace=kube-system
Forwarding from 0.0.0.0:8081 -> 8081
```
## Run prometheus
```yaml
$ vim prometheus.yml 
scrape_configs:
  # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
  - job_name: 'prometheus'

    # metrics_path defaults to '/metrics'
    # scheme defaults to 'http'.

    static_configs:
    - targets: ['localhost:9090']
  - job_name: 'kube-state-metrics'
    static_configs:
    - targets: ['localhost:8080','localhost:8081']

$ ./prometheus --config.file=prometheus.yml
```