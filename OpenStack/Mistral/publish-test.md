# publish
## 新增workflow檔案
```yaml
$ vim publish-test.yaml

---
version: '2.0'

publish-test:
  tasks:
    publish-test:
      action: std.noop
      on-success:
        publish:
          global:
            my_var: "global value"
          branch:
            my_var: "branch value"
        next:
          - A
    A:
      action: std.echo output='global=><% global(my_var) %>  branch=><% $.my_var%>'

    B:
      # 等待前方task執行完畢，否則global my_var會是null
      wait-before: 2
      action: std.echo output='global=><% global(my_var) %>  branch=><% $.my_var%>'
```
## 建立workflow
```s
$ mistral workflow-create publish-test.yaml
+--------------------------------------+--------------+-----------+----------------------------------+--------+-------+---------------------+------------+
| ID                                   | Name         | Namespace | Project ID                       | Tags   | Input | Created at          | Updated at |
+--------------------------------------+--------------+-----------+----------------------------------+--------+-------+---------------------+------------+
| 1e61f442-c7e8-498a-a54f-68f700b908d8 | publish-test |           | aeee8a0d64ba46a78b5664b994d8a16d | <none> |       | 2019-07-26 06:01:22 | None       |
+--------------------------------------+--------------+-----------+----------------------------------+--------+-------+---------------------+------------+
```
## 執行workflow
```s
$ mistral execution-create publish-test
+--------------------+--------------------------------------+
| Field              | Value                                |
+--------------------+--------------------------------------+
| ID                 | 53bad20d-c2f6-4cf3-885f-21c3de33c42c |
| Workflow ID        | 1e61f442-c7e8-498a-a54f-68f700b908d8 |
| Workflow name      | publish-test                         |
| Workflow namespace |                                      |
| Description        |                                      |
| Task Execution ID  | <none>                               |
| State              | RUNNING                              |
| State info         | None                                 |
| Created at         | 2019-07-26 06:01:41                  |
| Updated at         | 2019-07-26 06:01:42                  |
+--------------------+--------------------------------------+
```
## 查看task list
```s
$ mistral task-list 53bad20d-c2f6-4cf3-885f-21c3de33c42c
+--------------------------------------+--------------+---------------+--------------------+--------------------------------------+---------+------------+---------------------+---------------------+
| ID                                   | Name         | Workflow name | Workflow namespace | Execution ID                         | State   | State info | Created at          | Updated at          |
+--------------------------------------+--------------+---------------+--------------------+--------------------------------------+---------+------------+---------------------+---------------------+
| 03ad3f5a-88b9-4424-b5e0-738e658a62bb | A            | publish-test  |                    | 53bad20d-c2f6-4cf3-885f-21c3de33c42c | SUCCESS | None       | 2019-07-26 06:01:42 | 2019-07-26 06:01:42 |
| 1dd90bee-d276-4f5d-9857-a4a0190e461c | publish-test | publish-test  |                    | 53bad20d-c2f6-4cf3-885f-21c3de33c42c | SUCCESS | None       | 2019-07-26 06:01:42 | 2019-07-26 06:01:42 |
| d87b9add-6449-4b09-9d2c-340991a550d2 | B            | publish-test  |                    | 53bad20d-c2f6-4cf3-885f-21c3de33c42c | SUCCESS | None       | 2019-07-26 06:01:42 | 2019-07-26 06:01:43 |
+--------------------------------------+--------------+---------------+--------------------+--------------------------------------+---------+------------+---------------------+---------------------+
```
## 查看task結果
```s
# A task 輸出結果
$ mistral task-get-result 03ad3f5a-88b9-4424-b5e0-738e658a62bb
"global=>global value  branch=>branch value"

# B task 輸出結果
$ mistral task-get-result d87b9add-6449-4b09-9d2c-340991a550d2
"global=>global value  branch=>global value"
```