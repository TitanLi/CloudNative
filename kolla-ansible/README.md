# kolla-ansible
[openstack/kolla-ansible](https://github.com/openstack/kolla-ansible)

## Install dependencies
master、node
```
$ sudo apt-get update
$ sudo apt-get install -y python-dev libffi-dev gcc libssl-dev python-selinux python-setuptools
```

## Install python
master、node
```
$ sudo apt-get install -y python-pip
$ pip --version
$ sudo su
$ pip install -U pip
```

## pip版本高於10.0.0
master、node
```
$ vim /usr/bin/pip
將以下
#from pip import main
#if __name__ == '__main__':
#    sys.exit(main())
更新成
from pip import __main__
if __name__ == '__main__':
    sys.exit(__main__._main())
```

## 加入ssh key
master、node
```
root@titan1:/home/ubuntu# ssh-keygen
root@titan1:/home/ubuntu# cat /root/.ssh/id_rsa.pub
root@titan1:/home/ubuntu# vim /root/.ssh/authorized_keys
root@titan2:/home/ubuntu# vim /root/.ssh/authorized_keys
```

## Install dependencies using a virtual environment
master
```
$ sudo apt-get install -y python-virtualenv
$ virtualenv env
$ source env/bin/activate
# virtualenv /path/to/virtualenv
# source /path/to/virtualenv/bin/activate
```

## Install ansible
master
```
$ sudo apt-get install -y ansible
$ pip install ansible
```

## Configure Ansible
master
```
$ vim /etc/ansible/ansible.cfg
[defaults]
host_key_checking=False
pipelining=True
forks=100
```

## Install Kolla
master
```
$ git clone https://github.com/openstack/kolla -b stable/rocky
$ git clone https://github.com/openstack/kolla-ansible -b stable/rocky

$ pip install -r kolla/requirements.txt --ignore-installed PyYAML
$ pip install -r kolla-ansible/requirements.txt

$ sudo mkdir -p /etc/kolla
$ sudo chown $USER:$USER /etc/kolla

$ cp -r kolla-ansible/etc/kolla/* /etc/kolla
> 部署中使用的密碼
/etc/kolla/passwords.yml
> 隨機產生密碼
$ python kolla-ansible/tools/generate_passwords.py
```

## 編輯/etc/hosts
master、node
```
$ vim /etc/hosts
127.0.0.1 localhost
10.0.1.97 controller1
10.0.1.98 compute1
```

## 編輯DNS
master、node
```
$ vim /etc/resolv.conf
nameserver 8.8.8.8
```

## Prepare initial configuration(multinode)
master
> neutron_external_interface

> network_interface

> api_interface

> tunnel_interface

> storage_interface

> ansible_user=root  
```
$ vim kolla-ansible/ansible/inventory/multinode
[control]
controller1 neutron_external_interface=ens3 api_interface=eno1 network_interface=eno1 tunnel_interface=eno1 ansible_user=root

[network]
controller1 neutron_external_interface=ens3 api_interface=eno1 network_interface=eno1 tunnel_interface=eno1 ansible_user=root

[external-compute]
compute1 neutron_external_interface=ens3 api_interface=eno1 network_interface=eno1 tunnel_interface=eno1 ansible_user=root

[monitoring]
#monitoring01
compute1 neutron_external_interface=ens3 api_interface=eno1 network_interface=eno1 tunnel_interface=eno1 ansible_user=root

[storage]
compute1 neutron_external_interface=ens3 api_interface=eno1 network_interface=eno1 tunnel_interface=eno1 ansible_user=root

[deployment]
controller1       ansible_connection=local

$ ansible -i kolla-ansible/ansible/inventory/multinode all -m ping
$ ansible -i kolla-ansible/ansible/inventory/multinode all -m raw -a "apt-get -y install python-dev"
```

## Prepare initial configuration(globals)
master
```
$ vim /etc/kolla/globals.yml 
kolla_base_distro: "ubuntu"
kolla_install_type: "source"
openstack_release: "rocky"
kolla_internal_vip_address: "10.0.1.100"
network_interface: "eno1"
neutron_external_interface: "ens3"
keepalived_virtual_router_id: "96"
#enable_cinder: "yes"
#enable_cinder_backend_lvm: "yes"

$ kolla-ansible/tools/kolla-ansible -i kolla-ansible/ansible/inventory/multinode bootstrap-servers
$ kolla-ansible/tools/kolla-ansible -i kolla-ansible/ansible/inventory/multinode prechecks
$ kolla-ansible/tools/kolla-ansible -i kolla-ansible/ansible/inventory/multinode deploy
```

## Use OpenStack
master
```
$ pip install python-openstackclient python-glanceclient python-neutronclient --ignore-installed PyYAML
$ kolla-ansible/tools/kolla-ansible post-deploy
$ . /etc/kolla/admin-openrc.sh
```

## Upload image
master
```
$ wget http://download.cirros-cloud.net/0.4.0/cirros-0.4.0-x86_64-disk.img
$ openstack image create "cirros" \
  --file cirros-0.4.0-x86_64-disk.img \
  --disk-format qcow2 --container-format bare \
  --public
```

## Create network
```
# Flat Physical Network
physical_interface_mappings = physnet1:{{ neutron_external_interface }
```

## 環境移除
[Operating Kolla](https://docs.openstack.org/kolla-ansible/rocky/user/operating-kolla.html)
```
#清理容器
$ kolla-ansible/tools/cleanup-containers

#清理配置
$ kolla-ansible/tools/cleanup-host

#清理docker镜像
$ kolla-ansible/tools/cleanup-images

#clean up containers and volumes in the cluster --all
$ kolla-ansible/tools/kolla-ansible destroy  -i kolla-ansible/ansible/inventory/multinode --yes-i-really-really-mean-it
```

## 問題解決
### TASK [prechecks : Checking docker SDK version]
```
deactivate
pip install -U docker
```

### Cinder
[https://blog.gtwang.org/linux/linux-add-format-mount-harddisk/](https://blog.gtwang.org/linux/linux-add-format-mount-harddisk/)

[https://blog.inkubate.io/configure-cinder-on-openstack-ocata-standalone-with-kolla/](https://blog.inkubate.io/configure-cinder-on-openstack-ocata-standalone-with-kolla/)

[https://www.jianshu.com/p/635cdd220f63](https://www.jianshu.com/p/635cdd220f63)
```
$ lsblk
```

沒有為Mistral設置數據庫以供使用。在繼續之前，您應該確保您擁有以下││信息：││││*您要使用的數據庫類型; ││*數據庫服務器主機名（該服務器必須允許來自此│機器的TCP連接）; ││*用於訪問數據庫的用戶名和密碼。 ││││││如果缺少其中一些要求，請不要選擇此選項並使用常規SQLite支持運行。 ││││您可以稍後通過運行“dpkg-reconfigure -plow mistral-common”來更改此設置。 ││││為米斯特拉爾建立數據庫？