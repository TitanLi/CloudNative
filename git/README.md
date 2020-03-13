# Git
## 查看目前remote位址
```shell
$ git remote -v
```
## 退回更動前版本
```shell
$ git checkout -- *

or

$ git reset --hard HEAD
```
## 刪除commit
```shell
$ git log
$ git reset --hard <commit_id>
$ git push origin HEAD:master --force
```

## 查詢Commit紀錄
```shell
$ git log --oneline

or 

$ git reflog
```

## 回覆到指定版本
```shell
$ git reset --hard commit_id
```

## 同步
```shell
$ git pull origin <branch-name>
```