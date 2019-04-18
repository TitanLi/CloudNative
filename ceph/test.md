[[local|localrc]]

DEST=/opt/stack

# Logging
LOGFILE=$DEST/logs/stack.sh.log
VERBOSE=True
SCREEN_LOGDIR=$DEST/logs/screen
OFFLINE=False

HOST_IP=10.0.1.11
GIT_BASE=https://github.com
DATABASE_TYPE=mysql
MYSQL_HOST=$SERVICE_HOST
RABBIT_HOST=$SERVICE_HOST
GLANCE_HOSTPORT=$SERVICE_HOST:9292
ADMIN_PASSWORD=password
MYSQL_PASSWORD=$ADMIN_PASSWORD
RABBIT_PASSWORD=$ADMIN_PASSWORD
SERVICE_PASSWORD=$ADMIN_PASSWORD
SERVICE_TOKEN=$ADMIN_PASSWORD

enable_service q-svc
enable_service q-agt
enable_service q-dhcp
enable_service q-meta
enable_service q-l3

#ml2
Q_PLUGIN=ml2
Q_AGENT=openvswitch

# vxlan
Q_ML2_TENANT_NETWORK_TYPE=vxlan

# Networking
FLOATING_RANGE=10.0.1.0/24
Q_FLOATING_ALLOCATION_POOL=start=10.0.1.60,end=10.0.1.100
PUBLIC_NETWORK_GATEWAY=10.0.1.254

FIXED_RANGE=192.168.10.0/24
NETWORK_GATEWAY=192.168.10.254

PUBLIC_INTERFACE=eno1
FLAT_INTERFACE=ens3
# 關閉部署時自動建立Demo subnet功能
NEUTRON_CREATE_INITIAL_NETWORKS=False

# Khong can su dung tempest
disable_service tempest

# 禁用etcd
# disable_service etcd3

########
# CEPH #
########
enable_plugin ceph https://github.com/openstack/devstack-plugin-ceph

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


##########################
# GLANCE - IMAGE SERVICE #
##########################
ENABLED_SERVICES+=,g-api,g-reg


#################################
# CINDER - BLOCK DEVICE SERVICE #
#################################
ENABLED_SERVICES+=,cinder,c-api,c-vol,c-sch,c-bak
CINDER_DRIVER=ceph
CINDER_ENABLED_BACKENDS=ceph


##########################
# NOVA - COMPUTE SERVICE #
##########################
ENABLED_SERVICES+=,n-api,n-crt,n-cpu,n-cond,n-sch,n-net
DEFAULT_INSTANCE_TYPE=m1.micro

#vnc
enable_service n-novnc
enable_service n-cauth

MULTI_HOST=1