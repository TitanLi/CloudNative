# Ceph常用Command
# ceph health
```
$ ceph -w
$ ceph health detail
```
## pool not enabled
問題
```
$ ceph -w
health: HEALTH_WARN
            application not enabled on 1 pool(s)
```
解決方式
```
$ ceph health detail
HEALTH_WARN application not enabled on 1 pool(s)
POOL_APP_NOT_ENABLED application not enabled on 1 pool(s)
    application not enabled on pool 'images'
    use 'ceph osd pool application enable <pool-name> <app-name>', where <app-name> is 'cephfs', 'rbd', 'rgw', or freeform for custom applications.

$ ceph osd pool application enable images rbd
enabled application 'rbd' on pool 'images'
```
# pool
## pool list
```
$ sudo ceph osd lspools
1 backup,2 images,3 vms,4 volumes,
```
## 建立pool
```
ceph osd pool create <poolname> <pg_num>
```
## 檢查pool pg,pgp數量
```
$ sudo ceph osd pool get <poolname> pg_num

# 全部資訊
<poolname> => volumes
$ sudo ceph osd dump |grep <poolname>
pool 4 'volumes' replicated size 1 min_size 1 crush_rule 0 object_hash rjenkins pg_num 8 pgp_num 8 last_change 22 flags hashpspool stripe_width 0
```
## 變更pool pg、pgp大小
Pool大小設置有兩種說法
第一種：
> 每個pool應該分配多少個PG，與OSD數量、複本數量、Pool數量有關，公式如下
>> Total PGs = ((Total_number_of_OSD * 100) / max_replication_count) / pool_count
> 算出的結果取比它大最靠近2的N次方的值。比如說總共OSD數量是3，複本數3，pool數量也是3，那麼按造公式計算出來的結果是33.333333。取最靠近的2的N次方是64，那麼每個pool分配到的PG數量就是64
> 在更改PG數量時，建議同時更改PGP數量
第二種：
> 若少於5個OSD，pg設128
> 5~10個OSD，pg設512
> 10~50個OSD，pg設4096
> 超過50個OSD，可參考pgcalc計算
```
$ ceph osd pool set <poolname> pg_num 64
$ ceph osd pool set <poolname> pgp_num 64
```
## 變更replica大小
```
$ ceph osd pool set <poolname> size <replica size>
```
# rbd
```
$ rbd ls images
```