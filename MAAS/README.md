# MAAS
## Install MAAS
```shell
$ sudo apt-get update
$ sudo apt install maas
```
## Create admin user
```shell
$ sudo maas init
Create first admin account:
Username: admin
Password: admin
Again: admin
Email: admin@gmail.com
Import SSH keys [] (lp:user-id or gh:user-id):
```
## Ubuntu MAAS 2.2 Wake on LAN Driver Patch
```shell
$ sudo visudo
新增
maas ALL= NOPASSWD: /usr/sbin/etherwake

$ sudo apt-get install -y etherwake
$ git clone https://github.com/TitanLi/MAAS-WoL-driver.git
$ cd MAAS-WoL-driver
$ PATCH_DIR="/usr/lib/python3/dist-packages/provisioningserver/"
$ sudo patch -p1 -d ${PATCH_DIR} < maas-etherwake.diff
$ sudo systemctl restart maas-rackd.service maas-regiond.service
```
## 開啟DHCP
1. 點選Subnets
2. 設定Reserve range
3. 點選Subnets
4. 點選要開啟DHCP功能Subnet的VLAN
5. 點選右上角Take action
6. 點選Provide DHCP
7. 完成設定
## Commission
1. 點選Interfaces
2. 點選MAC
3. 複製MAC位址
4. 點選Configuration
5. Power type選擇Wake on LAN Power
6. 貼上MAC位址
7. 點選Interfaces
8. Actions -> Edit Physical
9. 設定IP
10. 點選右上角Take action
11. 執行Commission