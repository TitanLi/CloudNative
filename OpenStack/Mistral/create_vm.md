# Create VM
1. 編輯workflow file
```s
$ vim create_vm.yaml

---
version: '2.0'

create_vm:
  description: Simple workflow example

  input:
    - vm_name
    - image_ref
    - flavor_ref
  output:
    vm_id: "{{ _.vm_id }}"
    vm_status: <% $.vm_status %>

  tasks:
    create_server:
      action: nova.servers_create name=<% $.vm_name %> image=<% $.image_ref %> flavor=<% $.flavor_ref %>
      publish:
        vm_id: <% task().result.id %>
      on-success:
        - wait_for_instance

    wait_for_instance:
      action: nova.servers_find id={{ _.vm_id }} status='ACTIVE'
      retry:
        delay: 5
        count: 15
      publish:
        vm_status: "{{ task().result.status }}"
```
2. 建立workflow
```s
$ mistral workflow-create create_vm.yaml 
```
3. 查詢OpenStack image ID、flavor ID
```s
$ openstack image list
+--------------------------------------+--------+--------+
| ID                                   | Name   | Status |
+--------------------------------------+--------+--------+
| d65d28af-e736-460f-a1a4-468d6f5b194e | cirros | active |
+--------------------------------------+--------+--------+
$ flavor list
+--------------------------------------+------+------+------+-----------+-------+-----------+
| ID                                   | Name |  RAM | Disk | Ephemeral | VCPUs | Is Public |
+--------------------------------------+------+------+------+-----------+-------+-----------+
| 2ab4ce77-41a0-4e16-a9d8-1e069e9b0f4f | test | 4096 |  100 |         0 |     4 | True      |
+--------------------------------------+------+------+------+-----------+-------+-----------+
```
4. 執行workflow
```s
$  mistral execution-create create_vm '{"vm_name":"test","image_ref":"d65d28af-e736-460f-a1a4-468d6f5b194e","flavor_ref":"2ab4ce77-41a0-4e16-a9d8-1e069e9b0f4f"}'
+--------------------+--------------------------------------+
| Field              | Value                                |
+--------------------+--------------------------------------+
| ID                 | 8f8f8455-2184-401d-a764-a844a50c9c67 |
| Workflow ID        | 64c73fc8-4f3d-4fe4-b1c9-ce04bdaa857b |
| Workflow name      | create_vm                            |
| Workflow namespace |                                      |
| Description        |                                      |
| Task Execution ID  | <none>                               |
| State              | RUNNING                              |
| State info         | None                                 |
| Created at         | 2019-07-26 01:49:32                  |
| Updated at         | 2019-07-26 01:49:32                  |
+--------------------+--------------------------------------+
```
5. 查看execution執行結果
```s
$ mistral execution-list
+--------------------------------------+--------------------------------------+---------------+--------------------+-------------+-------------------+---------+------------+---------------------+---------------------+
| ID                                   | Workflow ID                          | Workflow name | Workflow namespace | Description | Task Execution ID | State   | State info | Created at          | Updated at          |
+--------------------------------------+--------------------------------------+---------------+--------------------+-------------+-------------------+---------+------------+---------------------+---------------------+
| 8f8f8455-2184-401d-a764-a844a50c9c67 | 64c73fc8-4f3d-4fe4-b1c9-ce04bdaa857b | create_vm     |                    |             | <none>            | SUCCESS | None       | 2019-07-26 01:49:32 | 2019-07-26 01:49:47 |
+--------------------------------------+--------------------------------------+---------------+--------------------+-------------+-------------------+---------+------------+---------------------+---------------------+
```
6. 查看task執行結果
```s
$ mistral task-list 8f8f8455-2184-401d-a764-a844a50c9c67
+--------------------------------------+-------------------+---------------+--------------------+--------------------------------------+---------+------------+---------------------+---------------------+
| ID                                   | Name              | Workflow name | Workflow namespace | Execution ID                         | State   | State info | Created at          | Updated at          |
+--------------------------------------+-------------------+---------------+--------------------+--------------------------------------+---------+------------+---------------------+---------------------+
| 293d4f57-25eb-45b1-bafe-1998a8a61d2e | create_server     | create_vm     |                    | 8f8f8455-2184-401d-a764-a844a50c9c67 | SUCCESS | None       | 2019-07-26 01:49:32 | 2019-07-26 01:49:34 |
| b8ecf406-23c6-4d35-8bd7-d8a7c6443956 | wait_for_instance | create_vm     |                    | 8f8f8455-2184-401d-a764-a844a50c9c67 | SUCCESS | None       | 2019-07-26 01:49:34 | 2019-07-26 01:49:46 |
+--------------------------------------+-------------------+---------------+--------------------+--------------------------------------+---------+------------+---------------------+---------------------+
```
7. 查看task result
```s
$ mistral task-get-result 293d4f57-25eb-45b1-bafe-1998a8a61d2e
{
    "OS-EXT-STS:task_state": "scheduling", 
    "addresses": {}, 
    "links": [
        {
            "href": "http://controller:8774/v2.1/servers/eaa7d83a-51c5-4f17-a8a1-63a47d2f2a48", 
            "rel": "self"
        }, 
        {
            "href": "http://controller:8774/servers/eaa7d83a-51c5-4f17-a8a1-63a47d2f2a48", 
            "rel": "bookmark"
        }
    ], 
    "image": {
        "id": "d65d28af-e736-460f-a1a4-468d6f5b194e", 
        "links": [
            {
                "href": "http://controller:8774/images/d65d28af-e736-460f-a1a4-468d6f5b194e", 
                "rel": "bookmark"
            }
        ]
    }, 
    "manager": {
        "api": {
            "server_groups": null, 
            "keypairs": null, 
            "servers": null, 
            "server_external_events": null, 
            "server_migrations": null, 
            "agents": null, 
            "instance_action": null, 
            "glance": null, 
            "hypervisor_stats": null, 
            "virtual_interfaces": null, 
            "flavors": null, 
            "availability_zones": null, 
            "user_id": null, 
            "cloudpipe": null, 
            "os_cache": false, 
            "quotas": null, 
            "migrations": null, 
            "usage": null, 
            "logger": null, 
            "project_id": null, 
            "neutron": null, 
            "quota_classes": null, 
            "project_name": null, 
            "aggregates": null, 
            "flavor_access": null, 
            "services": null, 
            "list_extensions": null, 
            "limits": null, 
            "hypervisors": null, 
            "cells": null, 
            "versions": null, 
            "client": null, 
            "hosts": null, 
            "volumes": null, 
            "assisted_volume_snapshots": null, 
            "certs": null
        }
    }, 
    "OS-EXT-STS:vm_state": "building", 
    "OS-EXT-SRV-ATTR:instance_name": "", 
    "OS-SRV-USG:launched_at": null, 
    "flavor": {
        "id": "2ab4ce77-41a0-4e16-a9d8-1e069e9b0f4f", 
        "links": [
            {
                "href": "http://controller:8774/flavors/2ab4ce77-41a0-4e16-a9d8-1e069e9b0f4f", 
                "rel": "bookmark"
            }
        ]
    }, 
    "id": "eaa7d83a-51c5-4f17-a8a1-63a47d2f2a48", 
    "security_groups": [
        {
            "name": "default"
        }
    ], 
    "user_id": "1c10bb82a938411f98483ba6b85a8ad6", 
    "OS-DCF:diskConfig": "MANUAL", 
    "accessIPv4": "", 
    "accessIPv6": "", 
    "progress": 0, 
    "OS-EXT-STS:power_state": 0, 
    "OS-EXT-AZ:availability_zone": "", 
    "config_drive": "", 
    "status": "BUILD", 
    "updated": "2019-07-26T01:49:33Z", 
    "hostId": "", 
    "OS-EXT-SRV-ATTR:host": null, 
    "OS-SRV-USG:terminated_at": null, 
    "key_name": null, 
    "OS-EXT-SRV-ATTR:hypervisor_hostname": null, 
    "name": "test", 
    "adminPass": "yPgf6Byw8ufk", 
    "tenant_id": "aeee8a0d64ba46a78b5664b994d8a16d", 
    "created": "2019-07-26T01:49:33Z", 
    "x_openstack_request_ids": [
        "req-913776f8-871e-4e19-9ee1-c0947a325268", 
        "req-725d848f-a926-4c06-a194-1bc5bb0ac4d5"
    ], 
    "os-extended-volumes:volumes_attached": [], 
    "_info": {
        "OS-EXT-STS:task_state": "scheduling", 
        "addresses": {}, 
        "links": [
            {
                "href": "http://controller:8774/v2.1/servers/eaa7d83a-51c5-4f17-a8a1-63a47d2f2a48", 
                "rel": "self"
            }, 
            {
                "href": "http://controller:8774/servers/eaa7d83a-51c5-4f17-a8a1-63a47d2f2a48", 
                "rel": "bookmark"
            }
        ], 
        "image": {
            "id": "d65d28af-e736-460f-a1a4-468d6f5b194e", 
            "links": [
                {
                    "href": "http://controller:8774/images/d65d28af-e736-460f-a1a4-468d6f5b194e", 
                    "rel": "bookmark"
                }
            ]
        }, 
        "OS-EXT-STS:vm_state": "building", 
        "OS-EXT-SRV-ATTR:instance_name": "", 
        "OS-SRV-USG:launched_at": null, 
        "flavor": {
            "id": "2ab4ce77-41a0-4e16-a9d8-1e069e9b0f4f", 
            "links": [
                {
                    "href": "http://controller:8774/flavors/2ab4ce77-41a0-4e16-a9d8-1e069e9b0f4f", 
                    "rel": "bookmark"
                }
            ]
        }, 
        "id": "eaa7d83a-51c5-4f17-a8a1-63a47d2f2a48", 
        "security_groups": [
            {
                "name": "default"
            }
        ], 
        "user_id": "1c10bb82a938411f98483ba6b85a8ad6", 
        "OS-DCF:diskConfig": "MANUAL", 
        "accessIPv4": "", 
        "accessIPv6": "", 
        "progress": 0, 
        "OS-EXT-STS:power_state": 0, 
        "OS-EXT-AZ:availability_zone": "", 
        "config_drive": "", 
        "status": "BUILD", 
        "updated": "2019-07-26T01:49:33Z", 
        "hostId": "", 
        "OS-EXT-SRV-ATTR:host": null, 
        "OS-SRV-USG:terminated_at": null, 
        "key_name": null, 
        "OS-EXT-SRV-ATTR:hypervisor_hostname": null, 
        "name": "test", 
        "adminPass": "yPgf6Byw8ufk", 
        "tenant_id": "aeee8a0d64ba46a78b5664b994d8a16d", 
        "created": "2019-07-26T01:49:33Z", 
        "os-extended-volumes:volumes_attached": [], 
        "metadata": {}
    }, 
    "metadata": {}, 
    "_loaded": true
}
```