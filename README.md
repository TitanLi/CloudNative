# OpenStack
> 學習筆記翻譯參考於[OpenStack官方網站](https://docs.openstack.org/install-guide/)
## Step 1 (Networking):
設定OpenStack Cluster相關節點網路

安裝教學：[OpenStack-Networking](https://hackmd.io/s/BJiZ4ZYWE)

範例：[Host-Networking](https://github.com/TitanLi/OpenStack/blob/master/Host-Networking)

## Step 2 (OpenStack Packages):
在所有節點安裝OpenStack Packages

安裝教學：[OpenStack-Packages](https://hackmd.io/s/rJNvbN5-V)

## Step 3 (MariaDB):
在Controller Node上安裝Database來儲存OpenStack服務相關資料，此選擇MariaDB

安裝教學：[OpenStack-Use-Database-MariaDB](https://hackmd.io/s/HJTQaGoWV)

範例：[Database-MariaDB](https://github.com/TitanLi/OpenStack/blob/master/Database-MariaDB)

## Step 4 (Message Queue):
在Controller Node上安裝Message queue來協調服務之間的操作和狀態資訊

安裝教學：[OpenStack-Message-Queue](https://hackmd.io/s/BkVnFs3W4)

## Step 5 (Memcached):
在Controller Node上安裝Memcached，通常使用Memcached來做身分驗證機制服務cache tokens

安裝教學：[OpenStack-Memcached](https://hackmd.io/s/HJ3H1uXzV)

## Step 6 (Keystone):
在Controller Node上安裝Keystone，Keystone提供單一節點整合管理用於管理身份驗證、授權和目錄服務

安裝教學：[OpenStack-Keystone](https://hackmd.io/s/HkdBONtN4)

範例：[OpenStack-Keystone](https://github.com/TitanLi/OpenStack/blob/master/keystone)