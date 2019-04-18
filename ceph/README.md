# Ceph

# 手動部署ceph
## ceph-deploy setup(deploy node)
```
$ sudo su
$ wget -q -O- 'https://download.ceph.com/keys/release.asc' | sudo apt-key add -
$ echo deb https://download.ceph.com/debian-luminous/ $(lsb_release -sc) main | sudo tee /etc/apt/sources.list.d/ceph.list
$ apt update
$ apt install ceph-deploy
```
## 建立ceph儲存檔案路徑(deploy node)
```
$ mkdir my-ceph
$ cd my-ceph
```
## 編輯/etc/hosts方便部署連線(deploy node)
```
$ vim /etc/hosts

新增
127.0.0.1 localhost titan6
10.0.1.13 titan6
10.0.1.14 titan7
```
## 建立ssh key讓電腦間彼此不需要密碼即可登入
> 原則上因之後ceph-deploy使用root權限，因此只要將Deploy node SSH key加入其他node **/root/.ssh/authorized_keys**
```
$ ssh-keygen
一般使用者
$ cat ~/.ssh/id_rsa.pub
root使用者
$ cat /root/.ssh/id_rsa.pub

將key新增至以下檔案
一般使用者
$ vim .ssh/authorized_keys
root使用者
$ vim /root/.ssh/authorized_keys
```
## 安裝python環境(全部node)
```
$ apt-get install -y python
```
## 安裝ceph(deploy node)
```
$ ceph-deploy install --release luminous titan6 titan7
```
## 建立要當任 Monitor 的節點(deploy node)
```
$ ceph-deploy new titan6
```
## 建立並初始化MON(deploy node)
```
$ ceph-deploy mon create titan6
$ ceph-deploy mon create-initial
```
## 將相關檔案複製至預設路徑/etc/ceph
```
$ pwd
/home/ubuntu/my-ceph

$ cp ./* /etc/ceph
```
## 查看MON狀態
```
$ ceph mon_status
```
## 在mon_server上創建名稱為mon_mgr的mgr服務
```
$ ceph-deploy mgr create titan6:mon_mgr
```
## 建立admin(deploy node)
```
$ ceph-deploy admin titan6
```
## 建立osd
[硬碟資訊](http://samwhelp.github.io/blog/read/linux/ubuntu/disk/info/)
```
# Ubuntu環境下，查詢硬碟資訊的指令
$ lsblk

# 加入osd
$ ceph-deploy osd create --data /dev/sdb1 titan7
```
## 查看osd狀態
```
$ sudo ceph osd tree
```
## 變更replica大小
> 若只有一個osd須執行此步驟
```
$ ceph osd pool set <poolname> size <replica size>
```

---
# 使用devstack部署OpenStack及Ceph
```conf
[[local|localrc]]
## CEPH #
#########
enable_plugin devstack-plugin-ceph https://github.com/openstack/devstack-plugin-ceph

HOST_IP=10.0.1.13
GIT_BASE=https://github.com
#DATABASE_TYPE=mysql
MYSQL_HOST=$SERVICE_HOST
RABBIT_HOST=$SERVICE_HOST
GLANCE_HOSTPORT=$SERVICE_HOST:9292
ADMIN_PASSWORD=password
MYSQL_PASSWORD=$ADMIN_PASSWORD
RABBIT_PASSWORD=$ADMIN_PASSWORD
SERVICE_PASSWORD=$ADMIN_PASSWORD
SERVICE_TOKEN=$ADMIN_PASSWORD

NEUTRON_CREATE_INITIAL_NETWORKS=False

# DevStack will create a loop-back disk formatted as XFS to store the
# Ceph data.
CEPH_LOOPBACK_DISK_SIZE=10G
# Ceph cluster fsid
CEPH_FSID=$(uuidgen)

# Glance pool, pgs and user
GLANCE_CEPH_USER=glance
GLANCE_CEPH_POOL=images
GLANCE_CEPH_POOL_PG=8
GLANCE_CEPH_POOL_PGP=8

# Nova pool and pgs
NOVA_CEPH_POOL=vms
NOVA_CEPH_POOL_PG=8
NOVA_CEPH_POOL_PGP=8

# Cinder pool, pgs and user
CINDER_CEPH_POOL=volumes
CINDER_CEPH_POOL_PG=8
CINDER_CEPH_POOL_PGP=8
CINDER_CEPH_USER=cinder
CINDER_CEPH_UUID=$(uuidgen)

# Cinder backup pool, pgs and user
CINDER_BAK_CEPH_POOL=backup
CINDER_BAK_CEPH_POOL_PG=8
CINDER_BAKCEPH_POOL_PGP=8
CINDER_BAK_CEPH_USER=cinder-bak

# How many replicas are to be configured for your Ceph cluster
CEPH_REPLICAS=${CEPH_REPLICAS:-1}

# Connect DevStack to an existing Ceph cluster
REMOTE_CEPH=False
REMOTE_CEPH_ADMIN_KEY_PATH=/etc/ceph/ceph.client.admin.keyring

#####################
## GLANCE – IMAGE SERVICE #
###########################
ENABLED_SERVICES+=,g-api,g-reg

##################################
## CINDER – BLOCK DEVICE SERVICE #
##################################
ENABLED_SERVICES+=,cinder,c-api,c-vol,c-sch,c-bak
CINDER_DRIVER=ceph
CINDER_ENABLED_BACKENDS=ceph

MULTI_HOST=1

FLAT_INTERFACE=enp5s2
PUBLIC_INTERFACE=enp2s0
```

---
# 使用devstack部署OpenStack及使用已存在Ceph
## ceph設定檔
```
將ceph叢集的/etc/ceph/ceph.client.admin.keyring複製一份本地
$ scp root@10.0.1.13:/etc/ceph/ceph.client.admin.keyring /etc/ceph

將ceph叢集的/etc/ceph/ceph.conf複製一份本地
$ scp root@10.0.1.13:/etc/ceph.conf /etc/ceph
$ sudo chmod 777 /etc/ceph/ceph.conf
```
## local.conf
```shell
[[local|localrc]]
## CEPH #
#########
enable_plugin devstack-plugin-ceph https://github.com/openstack/devstack-plugin-ceph

HOST_IP=10.0.1.11
GIT_BASE=https://github.com
#DATABASE_TYPE=mysql
MYSQL_HOST=$SERVICE_HOST
RABBIT_HOST=$SERVICE_HOST
GLANCE_HOSTPORT=$SERVICE_HOST:9292
ADMIN_PASSWORD=password
MYSQL_PASSWORD=$ADMIN_PASSWORD
RABBIT_PASSWORD=$ADMIN_PASSWORD
SERVICE_PASSWORD=$ADMIN_PASSWORD
SERVICE_TOKEN=$ADMIN_PASSWORD

NEUTRON_CREATE_INITIAL_NETWORKS=False
# DevStack will create a loop-back disk formatted as XFS to store the
# Ceph data.
CEPH_LOOPBACK_DISK_SIZE=10G
# Ceph cluster fsid
CEPH_FSID=$(uuidgen)

# Glance pool, pgs and user
GLANCE_CEPH_USER=glance
GLANCE_CEPH_POOL=images
GLANCE_CEPH_POOL_PG=8
GLANCE_CEPH_POOL_PGP=8

# Nova pool and pgs
NOVA_CEPH_POOL=vms
NOVA_CEPH_POOL_PG=8
NOVA_CEPH_POOL_PGP=8

# Cinder pool, pgs and user
CINDER_CEPH_POOL=volumes
CINDER_CEPH_POOL_PG=8
CINDER_CEPH_POOL_PGP=8
CINDER_CEPH_USER=cinder
CINDER_CEPH_UUID=$(uuidgen)

# Cinder backup pool, pgs and user
CINDER_BAK_CEPH_POOL=backup
CINDER_BAK_CEPH_POOL_PG=8
CINDER_BAKCEPH_POOL_PGP=8
CINDER_BAK_CEPH_USER=cinder-bak

# How many replicas are to be configured for your Ceph cluster
CEPH_REPLICAS=${CEPH_REPLICAS:-1}

# Connect DevStack to an existing Ceph cluster
REMOTE_CEPH=True
CEPH_CONF=/etc/ceph/ceph.conf
REMOTE_CEPH_ADMIN_KEY_PATH=/etc/ceph/ceph.client.admin.keyring

##################################
## CINDER – BLOCK DEVICE SERVICE #
##################################
CINDER_DRIVER=ceph
CINDER_ENABLED_BACKENDS=ceph

MULTI_HOST=1

FLAT_INTERFACE=ens3
PUBLIC_INTERFACE=eno1
```




```
[[local|localrc]]
## CEPH #
#########
enable_plugin devstack-plugin-ceph https://github.com/openstack/devstack-plugin-ceph

HOST_IP=10.0.1.11
GIT_BASE=https://github.com
#DATABASE_TYPE=mysql
MYSQL_HOST=$SERVICE_HOST
RABBIT_HOST=$SERVICE_HOST
GLANCE_HOSTPORT=$SERVICE_HOST:9292
ADMIN_PASSWORD=password
MYSQL_PASSWORD=$ADMIN_PASSWORD
RABBIT_PASSWORD=$ADMIN_PASSWORD
SERVICE_PASSWORD=$ADMIN_PASSWORD
SERVICE_TOKEN=$ADMIN_PASSWORD

NEUTRON_CREATE_INITIAL_NETWORKS=False

# DevStack will create a loop-back disk formatted as XFS to store the
# Ceph data.
CEPH_LOOPBACK_DISK_SIZE=10G
# Ceph cluster fsid
CEPH_FSID=$(uuidgen)

# Glance pool, pgs and user
GLANCE_CEPH_USER=glance
GLANCE_CEPH_POOL=images
GLANCE_CEPH_POOL_PG=8
GLANCE_CEPH_POOL_PGP=8

# Nova pool and pgs
NOVA_CEPH_POOL=vms
NOVA_CEPH_POOL_PG=8
NOVA_CEPH_POOL_PGP=8

# Cinder pool, pgs and user
CINDER_CEPH_POOL=volumes
CINDER_CEPH_POOL_PG=8
CINDER_CEPH_POOL_PGP=8
CINDER_CEPH_USER=cinder
CINDER_CEPH_UUID=$(uuidgen)

# Cinder backup pool, pgs and user
CINDER_BAK_CEPH_POOL=backup
CINDER_BAK_CEPH_POOL_PG=8
CINDER_BAKCEPH_POOL_PGP=8
CINDER_BAK_CEPH_USER=cinder-bak

# How many replicas are to be configured for your Ceph cluster
CEPH_REPLICAS=${CEPH_REPLICAS:-1}

# Connect DevStack to an existing Ceph cluster
REMOTE_CEPH=True
REMOTE_CEPH_ADMIN_KEY_PATH=/etc/ceph/ceph.client.admin.keyring

#####################
## GLANCE – IMAGE SERVICE #
###########################
ENABLED_SERVICES+=,g-api,g-reg

##################################
## CINDER – BLOCK DEVICE SERVICE #
##################################
ENABLED_SERVICES+=,cinder,c-api,c-vol,c-sch,c-bak
CINDER_DRIVER=ceph
CINDER_ENABLED_BACKENDS=ceph

MULTI_HOST=1

FLAT_INTERFACE=ens3
PUBLIC_INTERFACE=eno1
```

# 常用指令
```
查看健康狀態
> HEALTH_WARN或HEALTH_OK代表沒問題
$ ceph -s
查看使用者
$ sudo ceph auth list
更改權限
$ sudo ceph auth caps client.cinder mon 'allow rw'
查看volumes
$ rbd ls volumes
```

# ceph問題解決
## 問題一:
### 錯誤訊息:
```
$ ceph-deploy osd create --data /dev/sdb titan7
[titan7][ERROR ] RuntimeError: command returned non-zero exit status: 2
[ceph_deploy.osd][ERROR ] Failed to execute command: /usr/sbin/ceph-volume --cluster ceph lvm create --bluestore --data /dev/sdb
[ceph_deploy][ERROR ] GenericError: Failed to create 1 OSDs
```
### 解決方法
> 至osd node移除相關設定
第一步：
```
# 列出volume labels
$ lvdisplay

--- Logical volume ---
  LV Path                /dev/ceph-4b311820-1c06-4bdf-bf65-53bd3698730f/osd-block-4b5acc9c-efb4-4bbe-9bfb-32fd84737781
  LV Name                osd-block-4b5acc9c-efb4-4bbe-9bfb-32fd84737781
  VG Name                ceph-4b311820-1c06-4bdf-bf65-53bd3698730f
  LV UUID                V0cLby-HfHS-umxS-hJys-5E1h-otIW-DVU6ea
  LV Write Access        read/write
  LV Creation host, time titan7, 2019-03-19 09:57:46 +0000
  LV Status              available
  # open                 0
  LV Size                232.88 GiB
  Current LE             59616
  Segments               1
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     256
  Block device           252:1

# 刪除volume labels
$ lvremove --force /dev/ceph-4b311820-1c06-4bdf-bf65-53bd3698730f/osd-block-4b5acc9c-efb4-4bbe-9bfb-32fd84737781

  Logical volume "osd-block-4b5acc9c-efb4-4bbe-9bfb-32fd84737781" successfully removed
```
第二步：
```
# 列出volume groups
$ vgdisplay

  --- Volume group ---
  VG Name               ceph-4b311820-1c06-4bdf-bf65-53bd3698730f
  System ID             
  Format                lvm2
  Metadata Areas        1
  Metadata Sequence No  29
  VG Access             read/write
  VG Status             resizable
  MAX LV                0
  Cur LV                0
  Open LV               0
  Max PV                0
  Cur PV                1
  Act PV                1
  VG Size               232.88 GiB
  PE Size               4.00 MiB
  Total PE              59616
  Alloc PE / Size       0 / 0   
  Free  PE / Size       59616 / 232.88 GiB
  VG UUID               zxJkWR-TYY2-fZln-mkgd-QHTH-tIKh-32Czwz

# 刪除volume groups
$ vgremove ceph-4b311820-1c06-4bdf-bf65-53bd3698730f

  Volume group "ceph-4b311820-1c06-4bdf-bf65-53bd3698730f" successfully removed
```
## 問題二:
### 錯誤訊息
```
$ ceph -s
  cluster:
    id:     60125ebe-765c-4e51-9487-bc39dfb0c644
    health: HEALTH_WARN
            no active mgr
```
### 解決方法
> 應該在每個運行monitor的機器添加一個mgr，否則叢集會處於WARN狀態
> 在mon_server上創建名稱為mon_mgr的mgr服務
```
# ceph-deploy mgr create mon_server:mon_mgr
$ ceph-deploy mgr create titan6:mon_mgr
```

# Devstack問題解決
## 問題一：
### 錯誤訊息
```
sudo virsh secret-define --file secret.xml
error: Failed to set attributes from secret.xml
error: internal error: a secret with UUID 3f5a433b-c3b4-4651-b062-816d37324525 already defined for use with client.cinder secret
```
### 解決方法
```
$ sudo virsh secret-list
 UUID                                  Usage
--------------------------------------------------------------------------------
 d1f44e64-0d4c-423c-9091-45e83e6f0ae8  ceph client.cinder secret

$ sudo virsh secret-undefine d1f44e64-0d4c-423c-9091-45e83e6f0ae8

$ sudo virsh secret-set-value --secret 192ff8f8-2e80-4b5f-abcf-9792ccc5a91f --base64 AQAGGC1Y2J7kJRAACJD6Qw4SQN+ph0g7mwnUGA==
```
## 問題二:
### 錯誤訊息
```
502 Bad Gateway: Bad Gateway: The proxy server received an invalid: response from an upstream server.: Apache/2.4.18 (Ubuntu) Server at 10.0.1.12 Port 80 (HTTP 502) 
```
### 解決方法
```
可能是儲存有問題，可檢查ceph health
```