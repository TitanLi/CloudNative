# Heat
## 安裝
### create database
```shell
$ mysql -u root -p
MariaDB [(none)]> CREATE DATABASE heat;
MariaDB [(none)]> GRANT ALL PRIVILEGES ON heat.* TO 'heat'@'localhost' \
  IDENTIFIED BY 'HEAT_DBPASS';
MariaDB [(none)]> GRANT ALL PRIVILEGES ON heat.* TO 'heat'@'%' \
  IDENTIFIED BY 'HEAT_DBPASS';
```
### create the service credentials
``` shell
$ . admin-openrc
$ openstack user create --domain default --password-prompt heat
User Password: HEAT_PASS
Repeat User Password: HEAT_PASS
+---------------------+----------------------------------+
| Field               | Value                            |
+---------------------+----------------------------------+
| domain_id           | default                          |
| enabled             | True                             |
| id                  | 96280077ddd44044994b6626d5ea726e |
| name                | heat                             |
| options             | {}                               |
| password_expires_at | None                             |
+---------------------+----------------------------------+

$ openstack role add --project service --user heat admin
$ openstack service create --name heat \
>   --description "Orchestration" orchestration
+-------------+----------------------------------+
| Field       | Value                            |
+-------------+----------------------------------+
| description | Orchestration                    |
| enabled     | True                             |
| id          | d753195457a047f381cbe13b22705695 |
| name        | heat                             |
| type        | orchestration                    |
+-------------+----------------------------------+

$ openstack service create --name heat-cfn \
>   --description "Orchestration"  cloudformation
+-------------+----------------------------------+
| Field       | Value                            |
+-------------+----------------------------------+
| description | Orchestration                    |
| enabled     | True                             |
| id          | 9347dfc66ac74c4eaa6332e02e3136fd |
| name        | heat-cfn                         |
| type        | cloudformation                   |
+-------------+----------------------------------+
```
### Create the Orchestration service API endpoints:
``` shell
$ openstack endpoint create --region RegionOne \
>   orchestration public http://controller:8004/v1/%\(tenant_id\)s
+--------------+-----------------------------------------+
| Field        | Value                                   |
+--------------+-----------------------------------------+
| enabled      | True                                    |
| id           | de5cda9f3b6a404b973466a37f82fac0        |
| interface    | public                                  |
| region       | RegionOne                               |
| region_id    | RegionOne                               |
| service_id   | d753195457a047f381cbe13b22705695        |
| service_name | heat                                    |
| service_type | orchestration                           |
| url          | http://controller:8004/v1/%(tenant_id)s |
+--------------+-----------------------------------------+

$ openstack endpoint create --region RegionOne \
>   orchestration internal http://controller:8004/v1/%\(tenant_id\)s
+--------------+-----------------------------------------+
| Field        | Value                                   |
+--------------+-----------------------------------------+
| enabled      | True                                    |
| id           | e70f36fb00a6420fb518c3bf80bb570e        |
| interface    | internal                                |
| region       | RegionOne                               |
| region_id    | RegionOne                               |
| service_id   | d753195457a047f381cbe13b22705695        |
| service_name | heat                                    |
| service_type | orchestration                           |
| url          | http://controller:8004/v1/%(tenant_id)s |
+--------------+-----------------------------------------+

$ openstack endpoint create --region RegionOne \
>   orchestration admin http://controller:8004/v1/%\(tenant_id\)s
+--------------+-----------------------------------------+
| Field        | Value                                   |
+--------------+-----------------------------------------+
| enabled      | True                                    |
| id           | 20ff3e17c85c4a8babc8babee572354c        |
| interface    | admin                                   |
| region       | RegionOne                               |
| region_id    | RegionOne                               |
| service_id   | d753195457a047f381cbe13b22705695        |
| service_name | heat                                    |
| service_type | orchestration                           |
| url          | http://controller:8004/v1/%(tenant_id)s |
+--------------+-----------------------------------------+

$ openstack endpoint create --region RegionOne \
>   cloudformation public http://controller:8000/v1
+--------------+----------------------------------+
| Field        | Value                            |
+--------------+----------------------------------+
| enabled      | True                             |
| id           | a92131fff80248ffad6623e4d12b043f |
| interface    | public                           |
| region       | RegionOne                        |
| region_id    | RegionOne                        |
| service_id   | 9347dfc66ac74c4eaa6332e02e3136fd |
| service_name | heat-cfn                         |
| service_type | cloudformation                   |
| url          | http://controller:8000/v1        |
+--------------+----------------------------------+

$ openstack endpoint create --region RegionOne \
>   cloudformation internal http://controller:8000/v1
+--------------+----------------------------------+
| Field        | Value                            |
+--------------+----------------------------------+
| enabled      | True                             |
| id           | b26fe261b9724af28631e8b15132a968 |
| interface    | internal                         |
| region       | RegionOne                        |
| region_id    | RegionOne                        |
| service_id   | 9347dfc66ac74c4eaa6332e02e3136fd |
| service_name | heat-cfn                         |
| service_type | cloudformation                   |
| url          | http://controller:8000/v1        |
+--------------+----------------------------------+

$ openstack endpoint create --region RegionOne \
>   cloudformation admin http://controller:8000/v1
+--------------+----------------------------------+
| Field        | Value                            |
+--------------+----------------------------------+
| enabled      | True                             |
| id           | 56a2469c4e3e42b7b1e5c7200f88e13b |
| interface    | admin                            |
| region       | RegionOne                        |
| region_id    | RegionOne                        |
| service_id   | 9347dfc66ac74c4eaa6332e02e3136fd |
| service_name | heat-cfn                         |
| service_type | cloudformation                   |
| url          | http://controller:8000/v1        |
+--------------+----------------------------------+
```
### Orchestration requires additional information in the Identity service to manage stacks
```shell
$ openstack domain create --description "Stack projects and users" heat
+-------------+----------------------------------+
| Field       | Value                            |
+-------------+----------------------------------+
| description | Stack projects and users         |
| enabled     | True                             |
| id          | 2e9ece6f51ca4c7d96200186303c55b2 |
| name        | heat                             |
| tags        | []                               |
+-------------+----------------------------------+

$ openstack user create --domain heat --password-prompt heat_domain_admin
User Password: HEAT_PASS
Repeat User Password: HEAT_PASS
+---------------------+----------------------------------+
| Field               | Value                            |
+---------------------+----------------------------------+
| domain_id           | 2e9ece6f51ca4c7d96200186303c55b2 |
| enabled             | True                             |
| id                  | c47fbd39e005452c8c67c3eaca9811c1 |
| name                | heat_domain_admin                |
| options             | {}                               |
| password_expires_at | None                             |
+---------------------+----------------------------------+

$ openstack role add --domain heat --user-domain heat --user heat_domain_admin admin
$ openstack role create heat_stack_owner
+-----------+----------------------------------+
| Field     | Value                            |
+-----------+----------------------------------+
| domain_id | None                             |
| id        | c0636a54a5b54e09832a4b443517e801 |
| name      | heat_stack_owner                 |
+-----------+----------------------------------+

$ openstack role add --project demo --user demo heat_stack_owner
$ openstack role create heat_stack_user
+-----------+----------------------------------+
| Field     | Value                            |
+-----------+----------------------------------+
| domain_id | None                             |
| id        | ff0e375d360745d1bfc6eef7b3d32933 |
| name      | heat_stack_user                  |
+-----------+----------------------------------+
```
### Install and configure components
```shell
$ apt-get install -y heat-api heat-api-cfn heat-engine
$ vim /etc/heat/heat.conf
[DEFAULT]
transport_url = rabbit://openstack:RABBIT_PASS@controller
heat_metadata_server_url = http://controller:8000
heat_waitcondition_server_url = http://controller:8000/v1/waitcondition
stack_domain_admin = heat_domain_admin
stack_domain_admin_password = HEAT_DOMAIN_PASS
stack_user_domain_name = heat

[database]
connection = mysql+pymysql://heat:HEAT_DBPASS@controller/heat

[keystone_authtoken]
auth_uri = http://controller:5000
auth_url = http://controller:5000
memcached_servers = controller:11211
auth_type = password
project_domain_name = default
user_domain_name = default
project_name = service
username = heat
password = HEAT_PASS

[trustee]
auth_type = password
auth_url = http://controller:35357
username = heat
password = HEAT_PASS
user_domain_name = default

[clients_keystone]
auth_uri = http://controller:5000
```
### Populate the Orchestration database
```shell
$ su -s /bin/sh -c "heat-manage db_sync" heat
```
### Restart the Orchestration services
```shell
$ service heat-api restart
$ service heat-api-cfn restart
$ service heat-engine restart
```
## Verify operation
```shell
$ . admin-openrc
$ heat service-list
WARNING (shell) "heat service-list" is deprecated, please use "openstack orchestration service list" instead
+----------+-------------+--------------------------------------+--------+--------+----------------------------+--------+
| hostname | binary      | engine_id                            | host   | topic  | updated_at                 | status |
+----------+-------------+--------------------------------------+--------+--------+----------------------------+--------+
| titan4   | heat-engine | 0d56880c-2eb5-429d-8ed7-390da08b90cf | titan4 | engine | 2019-08-14T03:31:08.000000 | up     |
| titan4   | heat-engine | 4f0110fa-eee1-4526-af2b-807470246bbd | titan4 | engine | 2019-08-14T03:31:08.000000 | up     |
| titan4   | heat-engine | 5085ab21-a69c-4ea4-9b1c-29a1785cd6ac | titan4 | engine | 2019-08-14T03:31:08.000000 | up     |
| titan4   | heat-engine | 7ae08436-895a-4031-acb5-6b5817b0a50d | titan4 | engine | 2019-08-14T03:31:08.000000 | up     |
| titan4   | heat-engine | 8a8b439d-b5ab-4f4f-b839-ab3a279f7756 | titan4 | engine | 2019-08-14T03:31:08.000000 | up     |
| titan4   | heat-engine | bb9115ca-c1aa-45e4-9a91-d5e522b2a421 | titan4 | engine | 2019-08-14T03:31:08.000000 | up     |
| titan4   | heat-engine | ce9df40e-65d6-4095-ae9e-22073e4f6a25 | titan4 | engine | 2019-08-14T03:31:08.000000 | up     |
| titan4   | heat-engine | de0f3f5f-f75a-48fb-9836-ec9c68b74445 | titan4 | engine | 2019-08-14T03:31:08.000000 | up     |
+----------+-------------+--------------------------------------+--------+--------+----------------------------+--------+
```
## 技巧
### heat-engine status down
```shell
$ openstack orchestration service list
+----------+-------------+--------------------------------------+--------+--------+----------------------------+--------+
| Hostname | Binary      | Engine ID                            | Host   | Topic  | Updated At                 | Status |
+----------+-------------+--------------------------------------+--------+--------+----------------------------+--------+
| titan4   | heat-engine | 20ee8e75-e035-4bb2-92e9-562aef47cdc9 | titan4 | engine | 2019-08-14T03:28:33.000000 | down   |
| titan4   | heat-engine | f485c4b4-73f2-41d7-8a69-838032407a48 | titan4 | engine | 2019-08-14T03:29:50.000000 | up     |
| titan4   | heat-engine | 8a8b439d-b5ab-4f4f-b839-ab3a279f7756 | titan4 | engine | 2019-08-14T03:30:08.000000 | up     |
| titan4   | heat-engine | 4d92a24a-7a25-44be-961d-9144f0b22101 | titan4 | engine | 2019-08-14T03:29:50.000000 | up     |
| titan4   | heat-engine | d1f272db-f42c-4d2a-a8d2-41107913b50d | titan4 | engine | 2019-08-14T03:28:33.000000 | down   |
| titan4   | heat-engine | 0d56880c-2eb5-429d-8ed7-390da08b90cf | titan4 | engine | 2019-08-14T03:30:08.000000 | up     |
| titan4   | heat-engine | e7e9ad73-f7b6-4bf8-b10e-d79ffdbb455e | titan4 | engine | 2019-08-14T03:28:33.000000 | down   |
| titan4   | heat-engine | 8e52d6d0-71c1-4c9f-80bc-923f6afa2da6 | titan4 | engine | 2019-08-14T03:29:50.000000 | up     |
| titan4   | heat-engine | 7ae08436-895a-4031-acb5-6b5817b0a50d | titan4 | engine | 2019-08-14T03:30:08.000000 | up     |

$ heat-manage service clean
Dead engines are removed.

$ heat service-list
WARNING (shell) "heat service-list" is deprecated, please use "openstack orchestration service list" instead
+----------+-------------+--------------------------------------+--------+--------+----------------------------+--------+
| hostname | binary      | engine_id                            | host   | topic  | updated_at                 | status |
+----------+-------------+--------------------------------------+--------+--------+----------------------------+--------+
| titan4   | heat-engine | 0d56880c-2eb5-429d-8ed7-390da08b90cf | titan4 | engine | 2019-08-14T03:31:08.000000 | up     |
| titan4   | heat-engine | 4f0110fa-eee1-4526-af2b-807470246bbd | titan4 | engine | 2019-08-14T03:31:08.000000 | up     |
| titan4   | heat-engine | 5085ab21-a69c-4ea4-9b1c-29a1785cd6ac | titan4 | engine | 2019-08-14T03:31:08.000000 | up     |
| titan4   | heat-engine | 7ae08436-895a-4031-acb5-6b5817b0a50d | titan4 | engine | 2019-08-14T03:31:08.000000 | up     |
| titan4   | heat-engine | 8a8b439d-b5ab-4f4f-b839-ab3a279f7756 | titan4 | engine | 2019-08-14T03:31:08.000000 | up     |
| titan4   | heat-engine | bb9115ca-c1aa-45e4-9a91-d5e522b2a421 | titan4 | engine | 2019-08-14T03:31:08.000000 | up     |
| titan4   | heat-engine | ce9df40e-65d6-4095-ae9e-22073e4f6a25 | titan4 | engine | 2019-08-14T03:31:08.000000 | up     |
| titan4   | heat-engine | de0f3f5f-f75a-48fb-9836-ec9c68b74445 | titan4 | engine | 2019-08-14T03:31:08.000000 | up     |
+----------+-------------+--------------------------------------+--------+--------+----------------------------+--------+
```