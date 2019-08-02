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
username、http-password取得[https://review.opendev.org/#/settings/](https://review.opendev.org/#/settings/)
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

10. 重新提交review
```shell
$ git commit -a --amend
$ git review
```

11. recheck
> 如果jenkins回報了failure，可以查看Logs除錯

> 如果確認不是自己的patch導致，可以在comment上留言recheck，重新再跑 Test

(1) 點選Reply

(2) 輸入"recheck"

(3) Code-Review選擇0

(4) Workflow選擇0

(5) 按Post送出

![recheck](https://i.imgur.com/fxuvW2B.png)

(6) 查看驗證過程

[https://zuul.openstack.org/status](https://zuul.openstack.org/status)

![zuul1](https://i.imgur.com/DBLl4i2.png)

(7) 可輸入Project名稱查詢驗證狀態

![zuul2](https://i.imgur.com/sqtGGhJ.png)

(8) successfully merged

![successfully merged](https://i.imgur.com/6gMnuVw.png)