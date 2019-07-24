# std.ssh

## 新增ssh_workflow
```
$ vim ssh_workflow.yaml
version: '2.0'

ssh_workflow:
  input:
    - host
    - username
    - password

  tasks:
    task1:
      action: std.ssh host=<% $.host %> username=<% $.username %> \
              password=<% $.password %>
      input:
        cmd: "cd /home/ubuntu/ && ls"
      on-success: task2

    task2:
      action: std.echo output=<% task(task1).result %>
```

## 建立workflow
```
$ mistral workflow-create ssh_workflow.yaml
```

## 建立execution
```
$ mistral execution-create ssh_workflow '{"host":"10.0.1.99","username":"ubuntu","password":"ubuntu"}'
+--------------------+--------------------------------------+
| Field              | Value                                |
+--------------------+--------------------------------------+
| ID                 | 9db73b85-6e79-4d9f-b2cf-b86da9e70685 |
| Workflow ID        | 363d4e79-b96f-4db8-a2dd-06e12ed91d66 |
| Workflow name      | ssh_workflow                         |
| Workflow namespace |                                      |
| Description        |                                      |
| Task Execution ID  | <none>                               |
| State              | RUNNING                              |
| State info         | None                                 |
| Created at         | 2019-07-24 08:39:01                  |
| Updated at         | 2019-07-24 08:39:01                  |
+--------------------+--------------------------------------+
```

## 查看執行結果
```
$ mistral task-list 9db73b85-6e79-4d9f-b2cf-b86da9e70685
+--------------------------------------+-------+---------------+--------------------+--------------------------------------+---------+------------+---------------------+---------------------+
| ID                                   | Name  | Workflow name | Workflow namespace | Execution ID                         | State   | State info | Created at          | Updated at          |
+--------------------------------------+-------+---------------+--------------------+--------------------------------------+---------+------------+---------------------+---------------------+
| a5377958-7927-4880-b5e7-ebb7659919c3 | task1 | ssh_workflow  |                    | 9db73b85-6e79-4d9f-b2cf-b86da9e70685 | SUCCESS | None       | 2019-07-24 08:39:01 | 2019-07-24 08:39:02 |
| 43a8f4eb-a8da-43c8-bd91-1f9eb66e654f | task2 | ssh_workflow  |                    | 9db73b85-6e79-4d9f-b2cf-b86da9e70685 | SUCCESS | None       | 2019-07-24 08:39:02 | 2019-07-24 08:39:02 |
+--------------------------------------+-------+---------------+--------------------+--------------------------------------+---------+------------+---------------------+---------------------+

$ mistral task-get-result 43a8f4eb-a8da-43c8-bd91-1f9eb66e654f
"aaa.txt\n"
```

## 刪除環境
```
$ mistral execution-delete 9db73b85-6e79-4d9f-b2cf-b86da9e70685
$ mistral workflow-delete ssh_workflow
```