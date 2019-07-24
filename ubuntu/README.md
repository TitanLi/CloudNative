# Ubuntu
## password
```
$ sudo su

# 改密碼
$ passwd ubuntu
Enter new UNIX password: ubuntu
Retype new UNIX password: ubuntu
passwd: password updated successfully

$ sudo vim /etc/ssh/sshd_config
編輯
PasswordAuthentication yes

# 重啟ssh服務
$ systemctl restart sshd.service
```