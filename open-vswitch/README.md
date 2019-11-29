# open vswitch
## 新增網路橋接
ovs-vsctl add-br br0
## 將 interface(eno1) 綁定 Bridge br0 並設定type=internel
ovs-vsctl add-port br0 eno1 -- set interface  interface type=internel
## 查看 switch 的狀態
ovs-vsctl show
## 新增Flow Entry
> 若是沒有符合的條件，則丟棄封包
ovs-ofctl add-flow br0 "table=0,priority=0,actions=drop"
## 查詢Bridge Flow Entry
ovs-ofctl dump-flows br0
## 列出Bridge所有Port
ovs-vsctl list-ports br0