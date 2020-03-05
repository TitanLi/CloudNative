# Node Exporter
官方教學：[https://prometheus.io/docs/guides/node-exporter/](https://prometheus.io/docs/guides/node-exporter/)

github：[https://github.com/prometheus/node_exporter](https://github.com/prometheus/node_exporter)

## 部署及執行
> Download node_exporter:[https://prometheus.io/download/#node_exporter](https://prometheus.io/download/#node_exporter)

```shell
$ wget https://github.com/prometheus/node_exporter/releases/download/v*/node_exporter-*.*-amd64.tar.gz
$ tar xvfz node_exporter-*.*-amd64.tar.gz
$ cd node_exporter-*.*-amd64
$ ./node_exporter
```

## 驗證
```shell
$ curl http://localhost:9100/metrics
# HELP go_gc_duration_seconds A summary of the pause duration of garbage collection cycles.
# TYPE go_gc_duration_seconds summary
go_gc_duration_seconds{quantile="0"} 6.305e-06
go_gc_duration_seconds{quantile="0.25"} 1.5337e-05
```

## 配置Prometheus instances
```yaml
$ vim prometheus.yml
global:
  scrape_interval:     15s
  evaluation_interval: 15s
alerting:
  alertmanagers:
  - static_configs:
    - targets:
      # - alertmanager:9093

rule_files:
  # - "first_rules.yml"
  # - "second_rules.yml"

scrape_configs:
  - job_name: 'prometheus'
    scrape_interval: 5s

    static_configs:
      - targets: ['0.0.0.0:9090']

  # 新增此項
  - job_name: 'node'
    static_configs:
    - targets: ['192.168.2.95:9100']
```
## query
1. 取的Memory總量
> node_memory_MemTotal_bytes
2. 取得Swap總量
> node_memory_SwapTotal_bytes