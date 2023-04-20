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

## 刪除本地commit並保留程式碼
```shell
$ git reset --soft HEAD^
```

## Changing Your Committer Name & Email
```shell
# Globally
$ git config --global user.name "John Doe"
$ git config --global user.email "john@doe.org"

# per Repository
$ git config user.name "John Doe"
$ git config user.email "john@doe.org"
```

## Git：git diff發現windows下會出現"^M"符號
```shell
$ git config --global core.autocrlf true
```

## 取消已經Add的file
```shell
$ git reset HEAD test1.java
```

## 更改branch名稱
```shell
$ git branch -m <oldname> <newname>
```

## GitLab https問題
```
$ git config --global http.sslVerify false
```