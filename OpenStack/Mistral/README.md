# Mistral
[安裝教學](https://cao0507.github.io/2017/12/23/Openstack%E7%8E%AF%E5%A2%83%E4%B8%8B%E6%89%8B%E5%8A%A8%E5%AE%89%E8%A3%85Mistral/)
[Welcome to the Mistral documentation](https://docs.openstack.org/mistral/latest/)

## 安裝必要元件
```
$ apt-get install python-dev python-setuptools python-pip libffi-dev \
  libxslt1-dev libxml2-dev libyaml-dev libssl-dev
```

## 安裝Mistral server
```
$ git clone https://github.com/openstack/mistral.git
$ cd mistral

$ pip install -r requirements.txt
$ python setup.py install
```

## 產生配置文件
```
$ oslo-config-generator --config-file tools/config/config-generator.mistral.conf --output-file etc/mistral.conf
```

## 建立Mistral及logs目錄
```
$ mkdir -p /etc/mistral /var/log/mistral
```

## 複製配置文件
```
$ cp etc/* /etc/mistral/
```

## 建立mistral使用者
```
$ openstack user create --domain default --password-prompt mistral
User Password:MISTRAL_PASS
Repeat User Password:MISTRAL_PASS

$ openstack role add --project service --user mistral admin
```

## 建立資料庫
```
$ mysql
MariaDB [(none)]> CREATE DATABASE mistral;
MariaDB [mistral]> GRANT ALL PRIVILEGES ON mistral.* TO 'mistral'@'localhost' IDENTIFIED BY 'openstack';
MariaDB [mistral]> GRANT ALL PRIVILEGES ON mistral.* TO 'mistral'@'%' IDENTIFIED BY 'openstack';
MariaDB [mistral]> flush privileges;
MariaDB [mistral]> exit;
```

## 建立service和endpoint
```
$ openstack service create --name mistral --description "Openstack Workflow service" workflow
$ openstack endpoint create --region RegionOne workflow public http://controller:8989/v2
$ openstack endpoint create --region RegionOne workflow internal http://controller:8989/v2
$ openstack endpoint create --region RegionOne workflow admin http://controller:8989/v2
```

## 修改配置文件
```
$ vim /etc/mistral/mistral.conf 
[DEFAULT]
transport_url = rabbit://openstack:RABBIT_PASS@controller

[database]
connection = mysql+pymysql://mistral:openstack@controller/mistral

[keystone_authtoken]
auth_uri = http://controller:5000
auth_url = http://controller:5000
memcached_servers = controller:11211
auth_type = password
project_domain_name = Default
user_domain_name = Default
project_name = service
username = mistral
password = MISTRAL_PASS
```

## 初始化資料庫
```
$ mistral-db-manage --config-file /etc/mistral/mistral.conf upgrade head
$ mistral-db-manage --config-file /etc/mistral/mistral.conf populate
```

## 安裝Mistral client
```
$ pip install python-mistralclient
```

## 安装Mistral horizon
```
$ git clone https://git.openstack.org/openstack/mistral-dashboard.git -b stable/queens
$ cd mistral-dashboard/
$ pip install -r requirements.txt
$ python setup.py install
$ cp -b mistraldashboard/enabled/_50_mistral.py /usr/share/openstack-dashboard/openstack_dashboard/enabled/_50_mistral.py
```

## 重啟apache2
```
$ service apache2 restart
```
[Mistral horizon](https://i.imgur.com/3ujmzUI.png)

## 運行Mistral server
```
$ python mistral/mistral/cmd/launch.py --server all --config-file /etc/mistral/mistral.conf

or

# Running Mistral API server
$ mistral-server --server api --config-file /etc/mistral/mistral.conf

# Running Mistral Engines
$ mistral-server --server engine --config-file /etc/mistral/mistral.conf

# Running Mistral Executors
$ mistral-server --server executor --config-file /etc/mistral/mistral.conf

# To run more than one server
$ mistral-server --server api,engine --config-file <path-to-mistral.conf>
```

## 測試Mistral CLI
```
$ mistral workbook-list
$ mistral action-list
```

## Mistral Service狀態監控
> 透過tooz coordinator的member管理實現的，當成是啟動時，會自動註冊member，程式壞掉或退出時，會從member中移除，由此判斷該服務是否運行，coordinator的backend可以是zookeeper、redis、memcached等，這裡選用memcached
```
$ vim /etc/mistral/mistral.conf
[coordination]
backend_url = memcached://10.0.1.97:11211 
heartbeat_interval = 5.0
```
完成後即可執行
> hostname:titan1,pid:23717
```
$ mistral service-list
+--------------+----------------+
| Name         | Type           |
+--------------+----------------+
| titan1_23717 | engine_group   |
| titan1_23717 | api_group      |
| titan1_23717 | executor_group |
+--------------+----------------+
```

## 技巧
[https://blog.csdn.net/tpiperatgod/article/details/56282219](https://blog.csdn.net/tpiperatgod/article/details/56282219)
### 常用指令
#### action
```
# 查詢有哪些action可以使用
$ mistral action-list

# 查詢action傳入參數，可以通過mistral action-get {action_name}來查看
$ mistral action-get keystone.users_get

# 建立action
$ mistral action-create hello_Ad_hoc.yaml

# 刪除action
$ mistral action-delete {action_name}
```
#### workflow
```
# 查看所有workflow list
$ mistral workflow-list

# 建立workflow
$ mistral workflow-create my_workflow.yaml

# 刪除workflow
$ mistral workflow-delete {workflow_name}
```
#### execution
```
# 查看所有workflow執行結果
$ mistral execution-list

# 執行workflow可執行mistral execution-create {workflow_name} '參數(key-value)'
$ mistral execution-create hello_Ad_hoc_workflow '{"name": "Titan"}'

# 刪除execution
$ mistral execution-delete {execution-create_ID}
```
#### task
```
# 查看execution之後的task，可透過execution ID查詢
$ mistral task-list {execution_ID}

# 取得task執行結果
$ mistral task-get-result {task-list_ID}

# 一個task有多個action時可使用此方法查看執行狀態
$ mistral action-execution-list {task-list_ID}

# 查看task單一action輸出結果
$ mistral action-execution-get-output {action-execution-list_ID}
```
### Others action
```
std.async_noop
std.echo
std.email
std.fail
std.http
std.javascript
std.mistral_http
std.noop
std.ssh
std.ssh_proxied
std.wait_ssh
```
### workflow template
1. direct workflow
> 純屬範例，不能直接執行，僅作為Demo使用
```yaml
---
version: "2.0"

# workflow name
my_workflow:
  type: direct
  # 描述功能
  description: workflow template demo
  # 輸入參數
  input:
    - names
    - apple
  # 輸出參數
  output:
    # <% $.name%> 取得參數
    vm_id: <% $.vm_id %>
  # 開始撰寫task
  tasks:
    # 第一個task名稱
    task1:
      # 描述功能
      description: task1 demo
      # 若輸入參數為list可使用此方法執行，將會在task中產生多個action執行
      with-items: name in <% $.names %>
      action: std.echo output=<% $.name %>
      # 輸出結果
      publish:
        vm_id: <% task(task1).result.id %>
      # 此任務成功後執行task2
      on-success: task2
      # 若失敗觸發
      on-error:
        # 什麼都不要做
        - noop
      # 此任務結束後執行（不管成功還是失敗）都會執行
      on-complete:
        - wait_for_all_tasks
    # 第二個task名稱
    task2:
      action: std.echo output="Done"
      # 透過retry設定輪詢間隔與時間
      retry:
        delay: 5
        count: 15
```
> action、on-success、on-error、on-complete可理解為
```
try:
    action
    on-success
except:
    on-error
finally:
    on-complete
```
> 並行使用
>> join:all表示需等待所有task完成，也可以設置為1或one，至樣就只需等待任一一個task執行結束即可
```
tasks:
  A:
    action: action.x
    on-success:
      C
  
  B:
    action: action.y
    on-success:
      C
  
  C:
    join: all
    action: action.z
```
2. Reverse Workflow
> 此task是屬於反向依賴，意思是執行A，如果A宣告依賴於B、C，則需要先執行B、C
>> 需注意Reverse Workflow不能使用on-success、on-error以及on-complete指令
```
tasks:
  A:
    action: action.x
    requires: [B]  
  B:
    action: action.y
  C:
    action: action.z
```
## 開始使用
### 建立workflow(建立任務模板)
> name:是一組參數 <br>
> with-times:是workflow的一個指令，可以想像就是for in功能 <br>
> action:要執行的命令，此為執行std.echo，即打印name參數 <br>
> on-success:成功後執行的task

```yaml
# 編輯
$ vim my_workflow.yaml
# 輸入
---
version: "2.0"

my_workflow:
  type: direct

  input:
    - names

  tasks:
    task1:
      with-items: name in <% $.names %>
      action: std.echo output=<% $.name %>
      on-success: task2

    task2:
      action: std.echo output="Done"

# 建立workflow
$ mistral workflow-create my_workflow.yaml
+--------------------------------------+-------------+-----------+----------------------------------+--------+-------+---------------------+------------+
| ID                                   | Name        | Namespace | Project ID                       | Tags   | Input | Created at          | Updated at |
+--------------------------------------+-------------+-----------+----------------------------------+--------+-------+---------------------+------------+
| b7a9c1e5-da82-456f-ac3a-ffc004691da7 | my_workflow |           | aeee8a0d64ba46a78b5664b994d8a16d | <none> | names | 2019-07-19 06:21:49 | None       |
+--------------------------------------+-------------+-----------+----------------------------------+--------+-------+---------------------+------------+
```
### 執行以創建好的workflow
``` shell
$ mistral execution-create my_workflow '{"names": ["John", "Mistral", "Ivan", "Crystal"]}'
+--------------------+--------------------------------------+
| Field              | Value                                |
+--------------------+--------------------------------------+
| ID                 | 13477050-7afa-46e0-8b3d-9e99cfeaa06b |
| Workflow ID        | b7a9c1e5-da82-456f-ac3a-ffc004691da7 |
| Workflow name      | my_workflow                          |
| Workflow namespace |                                      |
| Description        |                                      |
| Task Execution ID  | <none>                               |
| State              | RUNNING                              |
| State info         | None                                 |
| Created at         | 2019-07-19 06:22:05                  |
| Updated at         | 2019-07-19 06:22:05                  |
+--------------------+--------------------------------------+
```
### 查看整個workflow執行狀態
``` shell
$ mistral execution-list
+--------------------------------------+--------------------------------------+---------------+--------------------+-------------+-------------------+---------+------------+---------------------+---------------------+
| ID                                   | Workflow ID                          | Workflow name | Workflow namespace | Description | Task Execution ID | State   | State info | Created at          | Updated at          |
+--------------------------------------+--------------------------------------+---------------+--------------------+-------------+-------------------+---------+------------+---------------------+---------------------+
| 13477050-7afa-46e0-8b3d-9e99cfeaa06b | b7a9c1e5-da82-456f-ac3a-ffc004691da7 | my_workflow   |                    |             | <none>            | SUCCESS | None       | 2019-07-19 06:22:05 | 2019-07-19 06:22:08 |
+--------------------------------------+--------------------------------------+---------------+--------------------+-------------+-------------------+---------+------------+---------------------+---------------------+
```
### 查看task執行狀態
``` shell
$ mistral task-list 13477050-7afa-46e0-8b3d-9e99cfeaa06b
+--------------------------------------+-------+---------------+--------------------+--------------------------------------+---------+------------+---------------------+---------------------+
| ID                                   | Name  | Workflow name | Workflow namespace | Execution ID                         | State   | State info | Created at          | Updated at          |
+--------------------------------------+-------+---------------+--------------------+--------------------------------------+---------+------------+---------------------+---------------------+
| 7b600295-289e-4644-9a0d-1e877f559100 | task1 | my_workflow   |                    | 13477050-7afa-46e0-8b3d-9e99cfeaa06b | SUCCESS | None       | 2019-07-19 06:22:05 | 2019-07-19 06:22:06 |
| 76dd77f2-3f65-4e72-b685-7f87c89aeed4 | task2 | my_workflow   |                    | 13477050-7afa-46e0-8b3d-9e99cfeaa06b | SUCCESS | None       | 2019-07-19 06:22:06 | 2019-07-19 06:22:06 |
+--------------------------------------+-------+---------------+--------------------+--------------------------------------+---------+------------+---------------------+---------------------+
```
### 查看task執行結果（即std.echo）
```shell
$ mistral task-get-result 7b600295-289e-4644-9a0d-1e877f559100
[
    "John", 
    "Mistral", 
    "Ivan", 
    "Crystal"
]
```
### 查看action執行狀態
> 因task1使用with-items，因此會出現多個action
``` shell
$ mistral action-execution-list 7b600295-289e-4644-9a0d-1e877f559100
+--------------------------------------+----------+---------------+--------------------+-----------+--------------------------------------+---------+----------+---------------------+---------------------+
| ID                                   | Name     | Workflow name | Workflow namespace | Task name | Task ID                              | State   | Accepted | Created at          | Updated at          |
+--------------------------------------+----------+---------------+--------------------+-----------+--------------------------------------+---------+----------+---------------------+---------------------+
| 3def2f31-db1a-4183-a9ce-726e5c4b9387 | std.echo | my_workflow   |                    | task1     | 7b600295-289e-4644-9a0d-1e877f559100 | SUCCESS | True     | 2019-07-19 06:22:05 | 2019-07-19 06:22:06 |
| 4d423c22-c946-4d5c-bff9-1b6d09491885 | std.echo | my_workflow   |                    | task1     | 7b600295-289e-4644-9a0d-1e877f559100 | SUCCESS | True     | 2019-07-19 06:22:05 | 2019-07-19 06:22:06 |
| 732dfd4f-0f60-4c6e-97c5-1b3bdd9e5ed2 | std.echo | my_workflow   |                    | task1     | 7b600295-289e-4644-9a0d-1e877f559100 | SUCCESS | True     | 2019-07-19 06:22:05 | 2019-07-19 06:22:06 |
| f8d916c6-8aa2-4dc8-8572-bc822f708bd9 | std.echo | my_workflow   |                    | task1     | 7b600295-289e-4644-9a0d-1e877f559100 | SUCCESS | True     | 2019-07-19 06:22:05 | 2019-07-19 06:22:05 |
+--------------------------------------+----------+---------------+--------------------+-----------+--------------------------------------+---------+----------+---------------------+---------------------+
```
### 查看單一action執行結果
``` shell
$ mistral action-execution-get-output 3def2f31-db1a-4183-a9ce-726e5c4b9387
{
    "result": "Crystal"
}
```

## 進階使用
### Ad-hoc actions
> 可用來填寫預設值
#### 建立Ad-hoc actions yaml
```yaml
$ vim hello_Ad_hoc.yaml
# 新增
---
version: '2.0'
hello_Ad_hoc:
  input:
    - execution_name
  base: std.echo
  base-input:
    output: Hello <% $.execution_name %>

# 建立action
$ mistral action-create hello_Ad_hoc.yaml
+--------------------------------------+--------------+-----------+----------------+-------------+--------+---------------------+------------+
| ID                                   | Name         | Is system | Input          | Description | Tags   | Created at          | Updated at |
+--------------------------------------+--------------+-----------+----------------+-------------+--------+---------------------+------------+
| 1c50bc3d-6dad-4352-8957-116bb35b696b | hello_Ad_hoc | False     | execution_name | None        | <none> | 2019-07-19 08:25:01 | None       |
+--------------------------------------+--------------+-----------+----------------+-------------+--------+---------------------+------------+
```
#### 建立workflow使用剛剛建立的action
``` yaml
$ vim hello_Ad_hoc_workflow.yaml
---
version: "2.0"

hello_Ad_hoc_workflow:
  type: direct

  input:
    - name

  tasks:
    hello-task1:
      action: hello_Ad_hoc execution_name=<% $.name %>

$ mistral workflow-create hello_Ad_hoc_workflow.yaml
+--------------------------------------+-----------------------+-----------+----------------------------------+--------+-------+---------------------+------------+
| ID                                   | Name                  | Namespace | Project ID                       | Tags   | Input | Created at          | Updated at |
+--------------------------------------+-----------------------+-----------+----------------------------------+--------+-------+---------------------+------------+
| bf6212d6-d73b-44bb-95b1-856a4ad8e978 | hello_Ad_hoc_workflow |           | aeee8a0d64ba46a78b5664b994d8a16d | <none> | name  | 2019-07-19 08:29:13 | None       |
+--------------------------------------+-----------------------+-----------+----------------------------------+--------+-------+---------------------+------------+
```
#### 使用workflow（hello_Ad_hoc_workflow）
```
$ mistral execution-create hello_Ad_hoc_workflow '{"name": "Titan"}'
+--------------------+--------------------------------------+
| Field              | Value                                |
+--------------------+--------------------------------------+
| ID                 | d218d295-d61d-4052-8c8b-bc92b507896c |
| Workflow ID        | bf6212d6-d73b-44bb-95b1-856a4ad8e978 |
| Workflow name      | hello_Ad_hoc_workflow                |
| Workflow namespace |                                      |
| Description        |                                      |
| Task Execution ID  | <none>                               |
| State              | RUNNING                              |
| State info         | None                                 |
| Created at         | 2019-07-19 08:31:51                  |
| Updated at         | 2019-07-19 08:31:51                  |
+--------------------+--------------------------------------+
```
#### 查看task執行狀態
``` shell
$ mistral task-list d218d295-d61d-4052-8c8b-bc92b507896c
+--------------------------------------+-------------+-----------------------+--------------------+--------------------------------------+---------+------------+---------------------+---------------------+
| ID                                   | Name        | Workflow name         | Workflow namespace | Execution ID                         | State   | State info | Created at          | Updated at          |
+--------------------------------------+-------------+-----------------------+--------------------+--------------------------------------+---------+------------+---------------------+---------------------+
| 4fddb7cb-3931-4a7b-a898-371e994ef8ee | hello-task1 | hello_Ad_hoc_workflow |                    | d218d295-d61d-4052-8c8b-bc92b507896c | SUCCESS | None       | 2019-07-19 08:31:51 | 2019-07-19 08:31:51 |
+--------------------------------------+-------------+-----------------------+--------------------+--------------------------------------+---------+------------+---------------------+---------------------+
```
#### 查看task執行結果（即hello_Ad_hoc）
```shell
$ mistral task-get-result 4fddb7cb-3931-4a7b-a898-371e994ef8ee
"Hello Titan"
```


## 可以透過運行來更改此設置
```
$ dpkg-reconfigure -plow mistral-common
```

## 問題解決
### E: Sub-process /usr/bin/dpkg returned an error code (1)
[http://yanue.net/post-123.html](http://yanue.net/post-123.html)
```
$ sudo mv /var/lib/dpkg/info /var/lib/dpkg/info.bak
$ sudo mkdir /var/lib/dpkg/info
$ sudo apt-get update

$ apt-get -f install vim
$ sudo mv /var/lib/dpkg/info/* /var/lib/dpkg/info.bak
$ sudo rm -rf /var/lib/dpkg/info
```