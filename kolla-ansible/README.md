# kolla-ansible

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
physical_interface_mappings = physnet1:{{ neutron_external_interface }
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