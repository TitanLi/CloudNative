# Prometheus
> 官方網站：[https://prometheus.io/docs/introduction/overview/](https://prometheus.io/docs/introduction/overview/)
## 下載Prometheus
[https://prometheus.io/download](https://prometheus.io/download)
## 解壓縮
```shell
$ tar xvfz prometheus-*.tar.gz
$ cd prometheus-*
```
## 配置自我修復
```yaml
$ vim prometheus.yml
global:
  scrape_interval:     15s # Set the scrape interval to every 15 seconds. Default is every 1 minute.
  evaluation_interval: 15s # Evaluate rules every 15 seconds. The default is every 1 minute.
  # scrape_timeout is set to the global default (10s).

# Alertmanager configuration
alerting:
  alertmanagers:
  - static_configs:
    - targets:
      # - alertmanager:9093

# Load rules once and periodically evaluate them according to the global 'evaluation_interval'.
rule_files:
  # - "first_rules.yml"
  # - "second_rules.yml"

# A scrape configuration containing exactly one endpoint to scrape:
# Here it's Prometheus itself.
scrape_configs:
  # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
  - job_name: 'prometheus'
    # Override the global default and scrape targets from this job every 5 seconds.
    scrape_interval: 5s
    # metrics_path defaults to '/metrics'
    # scheme defaults to 'http'.

    static_configs:
      - targets: ['0.0.0.0:9090']
```
## 執行prometheus
```shell
$ ./prometheus --config.file=prometheus.yml
```
## prometheus GUI
[http://localhost:9090/graph](http://localhost:9090/graph)

[http://localhost:9090/metrics](http://localhost:9090/metrics)

---

## 新增監控目標
1. 下載Prometheus Client Example
```shell
# Fetch the client library code and compile example.
$ git clone https://github.com/prometheus/client_golang.git
$ cd client_golang/examples/random
$ go get -d
$ go build

# Start 3 example targets in separate terminals:
$ ./random -listen-address=:8080
$ ./random -listen-address=:8081
$ ./random -listen-address=:8082
```
2. 編輯prometheus配置文件
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
  - job_name: 'example-random'
    scrape_interval: 5s
    static_configs:
      - targets: ['192.168.2.95:8080', '192.168.2.95:8081']
        labels:
          group: 'production'

      - targets: ['192.168.2.95:8082']
        labels:
          group: 'canary'
```
3. 重啟服務
4. 驗證
```shell
$ rpc_durations_seconds
```
## 制定常用模型
1. 建立規則
```yaml
$ vim prometheus.rules.yml
groups:
- name: example
  rules:
  - record: job_service:rpc_durations_seconds_count:avg_rate5m
    expr: avg(rate(rpc_durations_seconds_count[5m])) by (job, service)
```
2. 編輯prometheus配置文件
```yaml
$ vim prometheus.yml

global:
  scrape_interval:     15s # Set the scrape interval to every 15 seconds. Default is every 1 minute.
  evaluation_interval: 15s # Evaluate rules every 15 seconds. The default is every 1 minute.
  # scrape_timeout is set to the global default (10s).
alerting:
  alertmanagers:
  - static_configs:
    - targets:
      # - alertmanager:9093

rule_files:
  - 'prometheus.rules.yml'

scrape_configs:
  - job_name: 'prometheus'
    scrape_interval: 5s

    static_configs:
      - targets: ['0.0.0.0:9090']
```
3. 重啟服務
