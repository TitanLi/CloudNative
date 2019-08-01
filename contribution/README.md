# contribution
官方教學：[https://docs.openstack.org/infra/manual/developers.html](https://docs.openstack.org/infra/manual/developers.html)

1. 建立Launchpad帳號
[https://launchpad.net/openstack](https://launchpad.net/openstack)

2. 註冊帳號成為Foundation Member
[https://www.openstack.org/profile](https://www.openstack.org/profile)
> 信箱需與1.建立Launchpad帳號一致

3. 註冊Girrit帳號
[https://review.opendev.org/#/q/status:open](https://review.opendev.org/#/q/status:open)

4. 進入填寫資訊
[https://review.opendev.org/#/settings/](https://review.opendev.org/#/settings/)

- Profile中Username
- 在Agreements中簽署協議（ICLA）
- 在Contact Infomation填寫資訊（需是Foundation Member）
- 在SSH Public Keys中新增key
- 在HTTP Password（Username、Password之後會用到，可按Generate Password產生密碼）

5. 安裝python、git、git-review

6. git初始化
```shell
$ git config --global user.name "user_name"
$ git config --global user.email "your_email@youremail.com"
$ git config --global gitreview.username "TitanLi"
```

> 常用指令
>> 查看配置內容：git config --list <br>
>> 配置檔路徑：~/.gitconfig <br>
>> 查看review URI（剛git clone可使用，若git remote add gerrit將會檢查git remote是否正確）：git review -s <br>
>> 查看git remote狀態：git remote -v <br>
>> remove this old remote：git remote rm gerrit <br>
>> 查看git review狀態：git review -n -v

7. 取得專案
```shell
$ git clone https://github.com/openstack/kuryr-kubernetes.git
$ cd kuryr-kubernetes/
$ git review -s
$ git pull
```

8. git remote
- 第一次：
```shell
$ git remote add gerrit https://<username>:<http-password>@review.opendev.org/openstack/kuryr-kubernetes.git
```
- 第二次：
```shell
$ git remote set-url gerrit https://<username>:<http-password>@review.opendev.org/openstack/kuryr-kubernetes.git
```

9. 更改檔案
```shell
$ git checkout -b bug/manual
$ vim doc/source/installation/manual.rst
$ git commit -a
$ git review
```