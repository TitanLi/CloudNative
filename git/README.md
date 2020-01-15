# Git
## 查看目前remote位址
```shell
$ git remote -v
```
## 退回更動前版本
```
$ git checkout -- *
```
## 刪除commit
```
$ git log
$ git reset --hard <commit_id>
$ git push origin HEAD:master --force
```