# kolla-ansible
[openstack/kolla-ansible](https://github.com/openstack/kolla-ansible)

## Install dependencies
master、node
```shell
$ sudo apt-get update
$ sudo apt-get install -y python-dev libffi-dev gcc libssl-dev python-selinux python-setuptools
```

## Install python
master、node
```shell
$ sudo apt-get install -y python-pip
$ pip --version
# $ sudo su
# $ pip install -U pip
```

## pip版本高於10.0.0
master、node
```shell
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
```shell
root@titan1:/home/ubuntu# ssh-keygen
root@titan1:/home/ubuntu# cat /root/.ssh/id_rsa.pub
root@titan1:/home/ubuntu# vim /root/.ssh/authorized_keys
root@titan2:/home/ubuntu# vim /root/.ssh/authorized_keys
```

## Install dependencies using a virtual environment
master
```shell
$ sudo apt-get install -y python-virtualenv
$ sudo su
$ virtualenv env
$ source env/bin/activate
# virtualenv /path/to/virtualenv
# source /path/to/virtualenv/bin/activate
```

## Install ansible
master
```shell
$ sudo apt-get install -y ansible
$ pip install ansible
```

## Configure Ansible
master
```shell
$ vim /etc/ansible/ansible.cfg
[defaults]
host_key_checking=False
pipelining=True
forks=100
```

## Install Kolla
master
```shell
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
```shell
$ vim /etc/hosts
127.0.0.1 localhost
10.0.1.97 controller1
10.0.1.98 compute1
```

## 編輯DNS
master、node
```shell
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
```shell
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
```shell
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
```shell
$ pip install python-openstackclient python-glanceclient python-neutronclient --ignore-installed PyYAML
$ kolla-ansible/tools/kolla-ansible post-deploy
$ . /etc/kolla/admin-openrc.sh
```

## Upload image
master
```shell
# cirros
$ wget http://download.cirros-cloud.net/0.4.0/cirros-0.4.0-x86_64-disk.img
$ openstack image create "cirros" \
  --file cirros-0.4.0-x86_64-disk.img \
  --disk-format qcow2 --container-format bare \
  --public

# ubuntu
$ wget http://cloud-images.ubuntu.com/xenial/current/xenial-server-cloudimg-amd64-disk1.img
$ openstack image create "ubuntu" \
  --file xenial-server-cloudimg-amd64-disk1.img \
  --disk-format qcow2 --container-format bare \
  --public
```

## Create network
```shell
# Flat Physical Network
physical_interface_mappings = physnet1:{{ neutron_external_interface }
```

## 環境移除
[Operating Kolla](https://docs.openstack.org/kolla-ansible/rocky/user/operating-kolla.html)
```shell
#清理容器
$ kolla-ansible/tools/cleanup-containers

#清理配置
$ kolla-ansible/tools/cleanup-host

#清理docker镜像
$ kolla-ansible/tools/cleanup-images

#clean up containers and volumes in the cluster --all
#需stop all container(Controller、Compute)
$ docker stop $(docker ps -q)

$ kolla-ansible/tools/kolla-ansible destroy  -i kolla-ansible/ansible/inventory/multinode --yes-i-really-really-mean-it
```

## 進階功能
```shell
$ mysql -u haproxy -h <VIP>
```

## 問題解決
### TASK [prechecks : Checking docker SDK version]
```shell
deactivate
pip install -U docker
```

### Cinder
[https://blog.gtwang.org/linux/linux-add-format-mount-harddisk/](https://blog.gtwang.org/linux/linux-add-format-mount-harddisk/)

[https://blog.inkubate.io/configure-cinder-on-openstack-ocata-standalone-with-kolla/](https://blog.inkubate.io/configure-cinder-on-openstack-ocata-standalone-with-kolla/)

[https://www.jianshu.com/p/635cdd220f63](https://www.jianshu.com/p/635cdd220f63)
```shell
$ lsblk
```

### Mistral
```shell
$ vim /etc/kolla/globals.yml 
# 新增
enable_horizon_mistral: "{{ enable_mistral | bool }}"
enable_mistral: "yes"

$ pip install python-mistralclient

# mistral container內設定
[DEFAULT]
debug = False
log_dir = /var/log/kolla/mistral
use_stderr = False
transport_url = rabbit://openstack:dmjsV4JJmVT5AzaISfc7k1yELngPOoj7zEyKCQlD@10.0.1.13:5672//

[api]
host = 10.0.1.13
port = 8989
api_workers = 5

[database]
connection = mysql+pymysql://mistral:HdunpQn0m52CEa51FCPZZJU4Olz4bhcufdqw8Sq2@10.0.1.100:3306/mistral
max_retries = -1

[keystone_authtoken]
www_authenticate_uri = http://10.0.1.100:5000/v3
auth_url = http://10.0.1.100:35357/v3
auth_type = password
project_domain_id = default
user_domain_id = default
project_name = service
username = mistral
password = wVR48q9F02cWAzhvIFsjVoY2CgxhcUNUGzQYAodI
memcache_security_strategy = ENCRYPT
memcache_secret_key = gLbDatFrh3jHwGtAHmB4vQngMBIlCKyRJjsE6dF4
memcached_servers = 10.0.1.13:11211

[mistral]
url = http://10.0.1.100:8989

[openstack_actions]
os_actions_endpoint_type = internal
default_region = RegionOne

[oslo_messaging_notifications]
transport_url = rabbit://openstack:dmjsV4JJmVT5AzaISfc7k1yELngPOoj7zEyKCQlD@10.0.1.13:5672//
driver = noop

[coordination]
backend_url = redis://admin:N8cgBH4rbtHM7bLHabkUnlyWRIF7H0Y6PSCSPZ7L@10.0.1.13:26379?sentinel=kolla&socket_timeout=60&retry_on_timeout=yes

[pecan]
auth_enable=False
```

### Tacker
```shell
$ vim /etc/kolla/globals.yml 
# 新增
enable_tacker: "yes"
enable_barbican: "yes"
enable_mistral: "yes"
enable_redis: "yes"

$ pip install python-tackerclient
```