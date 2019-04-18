# devstack-plugin-ceph

## configure_ceph_glance
> function
> if($GLANCE_RGW_BACKEND = "True" && $ENABLE_CEPH_RGW = "True") == False
>> default value
>> GLANCE_RGW_BACKEND == False
>> ENABLE_CEPH_RGW == N/A
1. ceph osd pool create
```
# Default value
# CEPH_CONF_DIR = /etc/ceph
# CEPH_CONF_FILE = ${CEPH_CONF_DIR}/ceph.conf
# GLANCE_CEPH_POOL = images
# GLANCE_CEPH_POOL_PG = 8
# GLANCE_CEPH_POOL_PGP = 8

$ sudo $DOCKER_EXEC ceph -c ${CEPH_CONF_FILE} osd pool create \
            ${GLANCE_CEPH_POOL} ${GLANCE_CEPH_POOL_PG} ${GLANCE_CEPH_POOL_PGP}
```
2. ceph auth get-or-create
```
# Default value
# CEPH_CONF_DIR = /etc/ceph
# CEPH_CONF_FILE = ${CEPH_CONF_DIR}/ceph.conf
# GLANCE_CEPH_USER = glance
# GLANCE_CEPH_POOL = GLANCE_CEPH_POOL

$ sudo $DOCKER_EXEC ceph -c ${CEPH_CONF_FILE} auth \
            get-or-create client.${GLANCE_CEPH_USER} \
            mon "allow r" \
            osd "allow class-read object_prefix rbd_children, \
            allow rwx pool=${GLANCE_CEPH_POOL}" | \
            sudo tee ${CEPH_CONF_DIR}/ceph.client.${GLANCE_CEPH_USER}.keyring
```
3. 更改權限
```
# Default value
# CEPH_CONF_DIR = /etc/ceph
# GLANCE_CEPH_USER = glance

$ sudo chown ${STACK_USER}:$(id -g -n $whoami) \
            ${CEPH_CONF_DIR}/ceph.client.${GLANCE_CEPH_USER}.keyring
```

## configure_ceph_nova
1. 
```
# Default value
# CEPH_CONF_DIR = /etc/ceph
# CEPH_CONF_FILE = ${CEPH_CONF_DIR}/ceph.conf
# NOVA_CEPH_POOL = vms
# NOVA_CEPH_POOL_PG = 8
# NOVA_CEPH_POOL_PGP = 8

$ sudo $DOCKER_EXEC ceph -c ${CEPH_CONF_FILE} osd pool create \
        ${NOVA_CEPH_POOL} ${NOVA_CEPH_POOL_PG} ${NOVA_CEPH_POOL_PGP}
```
2. 
```
# Default value
# CEPH_CONF_DIR = /etc/ceph
# CEPH_CONF_FILE = ${CEPH_CONF_DIR}/ceph.conf
# CINDER_CEPH_USER = cinder
# CINDER_CEPH_POOL = volumes
# NOVA_CEPH_POOL = vms
# GLANCE_CEPH_POOL = images

$ sudo $DOCKER_EXEC ceph -c ${CEPH_CONF_FILE} \
            auth get-or-create client.${CINDER_CEPH_USER} \
            mon "allow r" \
            osd "allow class-read object_prefix rbd_children, \
            allow rwx pool=${CINDER_CEPH_POOL}, \
            allow rwx pool=${NOVA_CEPH_POOL}, \
            allow rwx pool=${GLANCE_CEPH_POOL}" | \
            sudo tee \
            ${CEPH_CONF_DIR}/ceph.client.${CINDER_CEPH_USER}.keyring \
            > /dev/null
```
3. 
```
# Default value
# CEPH_CONF_DIR = /etc/ceph
# CINDER_CEPH_USER = cinder

$ sudo chown ${STACK_USER}:$(id -g -n $whoami) \
            ${CEPH_CONF_DIR}/ceph.client.${CINDER_CEPH_USER}.keyring
```
## configure_ceph_cinder
1. 
```
# Default value
# CEPH_CONF_DIR = /etc/ceph
# CINDER_CEPH_POOL = volumes
# CINDER_CEPH_POOL_PG = 8
# CINDER_CEPH_POOL_PGP = 8

$ sudo $DOCKER_EXEC ceph -c ${CEPH_CONF_FILE} osd pool create \
        ${CINDER_CEPH_POOL} ${CINDER_CEPH_POOL_PG} ${CINDER_CEPH_POOL_PGP}
```
2. 
```
# Default value
# CEPH_CONF_DIR = /etc/ceph
# CEPH_CONF_FILE = ${CEPH_CONF_DIR}/ceph.conf
# CINDER_CEPH_USER = cinder
# CINDER_CEPH_POOL = volumes
# NOVA_CEPH_POOL = vms
# GLANCE_CEPH_POOL = images

$ sudo $DOCKER_EXEC ceph -c ${CEPH_CONF_FILE} auth get-or-create \
        client.${CINDER_CEPH_USER} \
        mon "allow r" \
        osd "allow class-read object_prefix rbd_children, \
        allow rwx pool=${CINDER_CEPH_POOL}, allow rwx pool=${NOVA_CEPH_POOL}, \
        allow rwx pool=${GLANCE_CEPH_POOL}" | \
        sudo tee ${CEPH_CONF_DIR}/ceph.client.${CINDER_CEPH_USER}.keyring
```
3. 
```
# Default value
# CEPH_CONF_DIR = /etc/ceph
# CINDER_CEPH_USER = cinder

$ sudo chown ${STACK_USER}:$(id -g -n $whoami) \
        ${CEPH_CONF_DIR}/ceph.client.${CINDER_CEPH_USER}.keyring
```
## import_libvirt_secret_ceph
```
# Default value
# CINDER_CEPH_UUID = $(uuidgen)
# CINDER_CEPH_USER = cinder
# CEPH_CONF_DIR = /etc/ceph
# CEPH_CONF_FILE = ${CEPH_CONF_DIR}/ceph.conf

$ cat <<EOF | sudo tee secret.xml>/dev/null
    <secret ephemeral='no' private='no'>
    <uuid>${CINDER_CEPH_UUID}</uuid>
    <usage type='ceph'>
        <name>client.${CINDER_CEPH_USER} secret</name>
    </usage>
    </secret>
EOF

$ sudo virsh secret-define --file secret.xml
$ sudo virsh secret-set-value --secret ${CINDER_CEPH_UUID} \
        --base64 $(sudo ceph -c ${CEPH_CONF_FILE} \
        auth get-key client.${CINDER_CEPH_USER})
$ sudo rm -f secret.xml
```