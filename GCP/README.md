# GCP
## Install 
```shell 
$ brew cask install google-cloud-sdk
```

## Login
```shell
$ gcloud auth login
```

## 設定Project Name
```shell
$ gcloud config set project PROJECT-ID

# example
$ gcloud config set project  eternal-skyline-267800
```

## 查看防火牆設定
```shell
$ gcloud compute firewall-rules list
# 檢查ssh是否已開啟若沒開啟執行以下指令
$ gcloud compute firewall-rules create default-allow-ssh --allow tcp:22
```

## 登入遠端主機
```shell
$ gcloud compute ssh [USER]@$PROB_INSTANCE

# example
$ gcloud compute ssh lisheng0706@web-app
```

## 新增防火牆規則
官方教學：[https://cloud.google.com/vpc/docs/using-firewalls?hl=zh-tw](https://cloud.google.com/vpc/docs/using-firewalls?hl=zh-tw)

選擇VPC網路 > 防火牆規則 > 建立防火牆規則 > 設定規則
1. 輸入規則名稱(Name)
> web-app-ingress
2. 選擇實施防火牆規則的網路(Network)
> default
3. 設定優先等級(Priority)，數值越低優先權越高
> 1000
4. 選擇流量方向(Direction of traffic)
> 輸入
5. 選擇相符實執行動做(Action on match)
> 允許
6. 選擇目標(Targets)
> 網路中的所有執行個體(All instances in the network)
7. 目的地篩選器(Destination filter)
> 0.0.0.0/0
8. 次要來源篩選器(Secondary source filter)
> 無
9. 通訊協定和通訊埠(Protocols and ports)
> 全部允許(Allow all)
