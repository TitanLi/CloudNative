# Linux network
## Table of Contents
* [如何建立veth pair](#如何建立veth-pair)
* [如何建立linux bridge](#如何建立linux-bridge)
## 如何建立veth pair
```shell
# 建立namespace ns1、ns2
$ ip netns add ns1
$ ip netns add ns2
# 查詢namespace列表
$ ip netns list
# ip命令創建一個network namespace時，會默認創建一個回環設備（loopback interface:lo）
# 該設備默認不啟動，最好將其啟動
$ ip netns exec ns1 ip link set dev lo up
$ ip netns exec ns2 ip link set dev lo up
# 查看網路介面狀態
$ ip netns exec ns1 ip addr
$ ip netns exec ns2 ip addr
# 建立veth pair
# 可以把 veth pair 當做是雙向的 pipe(管道),從一個方向傳送的網路資料,可以直接被另外一端接收到
# 也可以想象成兩個 namespace 直接通過一個特殊的虛擬網絡卡連線起來,可以直接通訊
# veth pair 無法單獨存在,刪除其中一個,另一個也會自動消失
# 新增兩張虛擬網卡vethtest1、vethtest2
$ ip link add vethtest1 type veth peer name vethtest2
# 查看link列表
$ ip link
# 將veth pair放到已經建立的namespace裡面
$ ip link set vethtest1 netns ns1
$ ip link set vethtest2 netns ns2
# 啟動
$ ip netns exec ns1 ip link set vethtest1 up
$ ip netns exec ns2 ip link set vethtest2 up
# 指定IP
$ ip netns exec ns1 ip addr add 10.20.0.1/24 dev vethtest1
$ ip netns exec ns2 ip addr add 10.20.0.2/24 dev vethtest2
# 查看網路介面狀態
$ ip netns exec ns1 ip addr
$ ip netns exec ns2 ip addr
# 給兩張網卡配置了IP後，會在各自的network namespace中生成一條路由，用ip route 或者 route -n查看
# 查看ns1 route table建立結果
$ ip netns exec ns1 ip route
or 
$ ip netns exec ns1 route -n
# 驗證使用ns1 ping 10.20.0.2
$ ip netns exec ns1 ping -c 3 10.20.0.2
# 建立namespace
$ ip netns delete ns1
$ ip netns delete ns2
# 刪除link
$ ip link delete vethtest1
```
## 如何建立linux bridge
```shell
# 建立namespace
$ ip netns add ns1
$ ip netns add ns2
# 建立橋接器
$ BRIDGE=br-test
$ brctl addbr $BRIDGE
# 進用橋接器STP
$ brctl stp $BRIDGE off
# 啟用橋接器
$ ip link set dev $BRIDGE up
# 建立兩張veth類型的tap裝置tap1、br-tap1，並設定他們的peer
$ ip link add tap1 type veth peer name br-tap1
# 將br-tap1加到橋接器br-test上的介面
$ brctl addif br-test br-tap1
# 將tap1加入到namespace n1
$ ip link set tap1 netns ns1
# 啟動tap1和br-tap1
$ ip netns exec ns1 ip link set dev tap1 up
$ ip link set dev br-tap1
# $ ip netns exec ns1 ip addr add 10.20.0.1/24 dev tap1
# $ ifconfig br-tap1 0.0.0.0 up
# $ ifconfig br-test 10.20.0.2 netmask 255.255.255.0 up
# $ ip netns exec ns1 ping 10.20.0.2
# 重複步驟建立tap2、bt-tap2
$ ip link add tap2 type veth peer name br-tap2
$ brctl addif br-test br-tap2
$ ip link set tap2 netns ns2
$ ip netns exec ns2 ip link set dev tap2 up
$ ip link set dev br-tap2 up
# 驗證
# 列出命名空間
$ ip netns list
ns2 (id: 1)
ns1 (id: 0)
# 列出網路介面卡
$ ip addr
24: br-test: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
    link/ether 02:72:5b:5e:74:ca brd ff:ff:ff:ff:ff:ff
    inet6 fe80::80c8:59ff:fed8:a51d/64 scope link 
       valid_lft forever preferred_lft forever
25: br-tap1@if26: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master br-test state UP group default qlen 1000
    link/ether 02:72:5b:5e:74:ca brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet6 fe80::72:5bff:fe5e:74ca/64 scope link 
       valid_lft forever preferred_lft forever
27: br-tap2@if28: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master br-test state UP group default qlen 1000
    link/ether 26:a5:1e:67:e9:8c brd ff:ff:ff:ff:ff:ff link-netnsid 1
    inet6 fe80::24a5:1eff:fe67:e98c/64 scope link 
       valid_lft forever preferred_lft forever
# 顯示橋接器br-test
$ brctl show br-test
bridge name	  bridge id		      STP enabled	interfaces
br-test		  8000.02725b5e74ca	  no		    br-tap1
							                    br-tap2
# 刪除namespace
$ ip netns delete ns1
$ ip netns delete ns2
# 刪除veth pair
$ ip link delete br-tap1
# 刪除bridge
$ ip link set dev br-test down
$ brctl delbr br-test
```