# Alert Manager
## 部署及執行
> Download node_exporter:[https://prometheus.io/download/#alertmanager](https://prometheus.io/download/#alertmanager)

```shell
$ wget https://github.com/prometheus/alertmanager/releases/download/v0.20.0/alertmanager-0.20.0.linux-amd64.tar.gz
$ tar xvfz alertmanager-0.20.0.linux-amd64.tar.gz
$ cd alertmanager-0.20.0.linux-amd64
$ ./alertmanager
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
      # 新增此行
      - 192.168.2.95:9093

rule_files:
  # - "first_rules.yml"
  # - "second_rules.yml"

scrape_configs:
  - job_name: 'prometheus'
    scrape_interval: 5s
    static_configs:
      - targets: ['0.0.0.0:9090']
```

## 驗證
[http://192.168.2.95:9093/#/alerts](http://192.168.2.95:9093/#/alerts)

[http://192.168.2.95:9093/metrics](http://192.168.2.95:9093/metrics)