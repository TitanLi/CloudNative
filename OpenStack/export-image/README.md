# Export Image
## Create a snapshot of the instance
```shell
$ nova list
+--------------------------------------+---------+--------+------------+-------------+-----------------------------------+
| ID                                   | Name    | Status | Task State | Power State | Networks                          |
+--------------------------------------+---------+--------+------------+-------------+-----------------------------------+
| 405cfb3f-b78c-4aca-9900-69f99b9e68d7 | testVM | ACTIVE | -          | Running     | net_mgmt=10.10.0.18, 192.168.2.73 |
+--------------------------------------+---------+--------+------------+-------------+-----------------------------------+

$ nova stop testVM
Request to stop server free5gc has been accepted.

$ nova list
+--------------------------------------+---------+---------+------------+-------------+---------------------+
| ID                                   | Name    | Status  | Task State | Power State | Networks            |
+--------------------------------------+---------+---------+------------+-------------+---------------------+
| 405cfb3f-b78c-4aca-9900-69f99b9e68d7 | testVM | SHUTOFF | -          | Shutdown    | net_mgmt=10.10.0.18 |
+--------------------------------------+---------+---------+------------+-------------+---------------------+

$ nova image-create --poll testVM testVM-image-name
Server snapshotting... 100% complete
Finished

$ openstack image list
+--------------------------------------+--------------------------+--------+
| ID                                   | Name                     | Status |
+--------------------------------------+--------------------------+--------+
| 1bd2292b-33bb-4054-bd38-adf3c1573854 | OpenWRT                  | active |
| cf2acf3d-bb11-4e17-bee2-ba17a7c15ea1 | cirros-0.4.0-x86_64-disk | active |
| cfe84117-7785-4000-8a74-6d0fdd4365f2 | testVM-image-name        | active |
| d065c1d9-abc2-4133-95f9-a30a12b1667b | ubuntu                   | active |
+--------------------------------------+--------------------------+--------+
```
## Download the snapshot as an image
```shell
$ openstack image list
+--------------------------------------+--------------------------+--------+
| ID                                   | Name                     | Status |
+--------------------------------------+--------------------------+--------+
| 1bd2292b-33bb-4054-bd38-adf3c1573854 | OpenWRT                  | active |
| cf2acf3d-bb11-4e17-bee2-ba17a7c15ea1 | cirros-0.4.0-x86_64-disk | active |
| cfe84117-7785-4000-8a74-6d0fdd4365f2 | testVM-image-name        | active |
| d065c1d9-abc2-4133-95f9-a30a12b1667b | ubuntu                   | active |
+--------------------------------------+--------------------------+--------+

$ glance image-download --file testVM-image-name.raw cfe84117-7785-4000-8a74-6d0fdd4365f2
```
## Import the snapshot to the new environment
```shell
$ openstack image create "testVM-image-name"   --file testVM-image-name.raw   --disk-format qcow2 --container-format bare   --public
```