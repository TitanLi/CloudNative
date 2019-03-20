# Ceph

# 手動部署ceph
## ceph-deploy setup(deploy node)
```
$ sudo su
$ wget -q -O- 'https://download.ceph.com/keys/release.asc' | sudo apt-key add -
$ echo deb https://download.ceph.com/debian-luminous/ $(lsb_release -sc) main | sudo tee /etc/apt/sources.list.d/ceph.list
$ sudo apt update
$ sudo apt install ceph-deploy
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
127.0.0.1 localhost titan1
10.0.1.98 titan2
10.0.1.99 titan3
```
## 建立ssh key讓電腦間彼此不需要密碼即可登入
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
$ apt-get install python
```
## 建立ceph叢集(deploy node)
```
$ ceph-deploy new titan1
```
## 安裝ceph(deploy node)
```
$ ceph-deploy install --release luminous titan1 titan2 titan3
```
## 建立並初始化MON(deploy node)
```
$ ceph-deploy mon create-initial
```
## 建立admin(deploy node)
```
$ ceph-deploy admin ceph-10
```
## 建立osd
[硬碟資訊](http://samwhelp.github.io/blog/read/linux/ubuntu/disk/info/)
```
# Ubuntu環境下，查詢硬碟資訊的指令
$ lsblk

# 加入osd
$ ceph-deploy osd create --data /dev/sdb1 titan2
$ ceph-deploy osd create --data /dev/sdb1 titan3
```
## 查看osd狀態
```
$ sudo ceph osd tree
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

# 問題解決
## 問題一：
### 錯誤訊息
```
sudo virsh secret-define --file secret.xml
error: Failed to set attributes from secret.xml
error: internal error: a secret with UUID 3f5a433b-c3b4-4651-b062-816d37324525 already defined for use with client.cinder secret
```
### 解決方法
```
$ virsh secret-undefine 3f5a433b-c3b4-4651-b062-816d37324525
```