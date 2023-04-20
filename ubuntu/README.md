# Ubuntu
----

## Table of Contents
* [密碼設定](#密碼設定)
* [Ubuntu sudo NoPassWD 不用輸入密碼設定](#ubuntu-sudo-noPasswd-不用輸入密碼設定)
* [設定IP](#設定ip)
* [package list](#package-list)
* [設定網路CLI](#設定網路cli)
* [修改網卡名稱](#修改網卡名稱)
* [Ubuntu 18.04](#ubuntu-1804)
  - [DNS](#dns)
  - [host rename](#host-rename)
* [格式化硬碟](#格式化硬碟)
* [時間設定](#時間設定)
* [安裝](#安裝)
  - [Mac](#1-mac)
    - [dd](#11-dd)
    - [格式化](#12-格式化)
* [查看CPU的溫度](#查看cpu的溫度)
* [CPU資訊](#cpu資訊)
* [查看資源使用率](#查看資源使用率)
  - [Memory](#memory)
  - [CPU](#cpu)
  - [高級工具](#高級工具)
* [查看已使用的port](#查看已使用的port)
* [指令](#指令)
  - [sed](#sed)
  - [netstat-列出所有連接Port](#netstat-列出所有連接Port)
  - [telnet測試IP](#telnet測試IP)
  - [VM新增Remote Tunnel](#VM新增Remote-Tunnel)
  - [iptables VM封包轉發](#iptables-VM封包轉發)
* [iptables指令](#iptables指令)
* [Wake on LAN](#wake-on-lan)
* [remove cloud-init](#remove-cloud-init)
* [誤刪/etc/fstab](#誤刪/etc/fstab)
* [問題解決](#問題解決)
  - [E: Sub-process /usr/bin/dpkg returned an error code](#e-sub-process-usrbindpkg-returned-an-error-code)

## 密碼設定
```shell
$ sudo su

# 改密碼
$ passwd ubuntu
Enter new UNIX password: ubuntu
Retype new UNIX password: ubuntu
passwd: password updated successfully

$ sudo vim /etc/ssh/sshd_config
編輯
PasswordAuthentication yes

# 重啟ssh服務
$ systemctl restart sshd.service
```

## Ubuntu sudo NoPassWD 不用輸入密碼設定
```
$ sudo visudo
將
%sudo   ALL=(ALL:ALL) ALL
改成
%sudo   ALL=(ALL:ALL) NOPASSWD:ALL
```

## 設定IP
```shell
$ vim /etc/network/interfaces
auto eno1
iface eno1 inet static # 固定 (靜態) IP
address 192.168.2.99 # IP 位址
netmask 255.255.254.0 # 網路遮罩
gateway 192.168.3.254 # 預設閘道
dns-nameservers 8.8.8.8 #DNS

# 重開機
# $ sudo apt install ifupdown
# $ sudo /etc/init.d/networking restart
$ sudo service network-manager restart
```

## package list
```shell
$ apt list -a <package name>
```

## 設定網路CLI
```shell
$ sudo ifconfig eno1 192.168.2.99 netmask 255.255.254.0
$ sudo route add default gw 192.168.3.254 eno1
$ route -n
```

## 修改網卡名稱
```shell
$ vi /etc/default/grub
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash"
GRUB_CMDLINE_LINUX="net.ifnames=0 biosdevname=0"

# 更新grub
$ grub-mkconfig -o /boot/grub/grub.cfg

# 編輯網卡名稱
$ vim /etc/netplan/00-installer-config.yaml
network:
  ethernets:
    eth0:
      addresses:
      - 192.168.122.101/24
      gateway4: 192.168.122.1
  version: 2
$ sudo netplan apply
$ sudo init 6
```

## Ubuntu 18.04
### DNS
方法一：
```shell
$ vim /etc/netplan/*.yaml
network:
    version: 2
    ethernets:
        eth0:
            addresses:
            - 123.123.123.123/20
            - 10.0.0.0/16
            gateway4: 123.123.123.1
            match:
                macaddress: cc:8c:11:e1:1b:81
            nameservers:
                addresses:
                - 8.8.8.8
                - 8.8.4.4
                search: []
            set-name: eth0

$ sudo netplan apply
# 替换掉 systemd-resolved 生成的 resolv.conf 文件
$ sudo rm /etc/resolv.conf
$ sudo ln -s /run/systemd/resolve/resolv.conf /etc/resolv.conf
```
方法二：

[https://jermine.vdo.pub/linux/ubuntu18.04%E4%BF%AE%E6%94%B9dns/](https://jermine.vdo.pub/linux/ubuntu18.04%E4%BF%AE%E6%94%B9dns/)

方法三：
```shell
$ vim /etc/systemd/resolved.conf
[Resolve]
DNS=8.8.8.8

$ sudo systemctl restart systemd-resolved
```

### host rename
```shell
$ vim /etc/hostname
$ vim /etc/hosts
$ sudo init 6
```

## 格式化硬碟
```shell
# 查看disk資訊
$ sudo fdisk -l

# 格式化
$ sudo mkfs.ext4 /dev/sda
mke2fs 1.42.13 (17-May-2015)
/dev/sda contains a ext4 file system
	created on Sat Aug 10 06:44:12 2019
Proceed anyway? (y,n) y
Creating filesystem with 244190646 4k blocks and 61054976 inodes
Filesystem UUID: fc9ab4a8-b438-4b96-8be5-a4d7ea05628d
Superblock backups stored on blocks: 
	32768, 98304, 163840, 229376, 294912, 819200, 884736, 1605632, 2654208, 
	4096000, 7962624, 11239424, 20480000, 23887872, 71663616, 78675968, 
	102400000, 214990848

Allocating group tables: done                            
Writing inode tables: done                            
Creating journal (32768 blocks): done
Writing superblocks and filesystem accounting information: done
```
## 時間設定
```shell
$ date
$ timedatectl list-timezones
$ sudo timedatectl set-timezone Asia/Taipei
```
## 安裝
### 1. Mac
#### 1.1 dd
> 使用hdiutil指令將ISO檔轉為Mac的DMG檔
```shell
$ hdiutil convert -format UDRW -o ubuntu16.04 ubuntu-16.04.6-desktop-amd64.iso
```
> 列出disk列表
```shell
$ diskutil list
```
> 卸載USB
```shell
$ diskutil unmountDisk /dev/disk2
```
> 使用dd指令將ubuntu16.04.dmg寫入USB
```shell
$ sudo dd if=ubuntu16.04.dmg of=/dev/rdisk2 bs=1m
```
#### 1.2 格式化
```shell
$ diskutil list
$ diskutil eraseDisk ExFAT titan /dev/disk2
```
## 查看CPU的溫度
```shell
$ sudo apt-get install lm-sensors
$ yes | sudo sensors-detect
$ sensors
acpitz-virtual-0
Adapter: Virtual device
temp1:        +27.8°C  (crit = +105.0°C)
temp2:        +29.8°C  (crit = +105.0°C)

nouveau-pci-0100
Adapter: PCI adapter
fan1:        3090 RPM
temp1:        +48.0°C  (high = +95.0°C, hyst =  +3.0°C)
                       (crit = +105.0°C, hyst =  +5.0°C)
                       (emerg = +135.0°C, hyst =  +5.0°C)

coretemp-isa-0000
Adapter: ISA adapter
Physical id 0:  +37.0°C  (high = +80.0°C, crit = +100.0°C)
Core 0:         +37.0°C  (high = +80.0°C, crit = +100.0°C)
Core 1:         +36.0°C  (high = +80.0°C, crit = +100.0°C)
Core 2:         +35.0°C  (high = +80.0°C, crit = +100.0°C)
Core 3:         +36.0°C  (high = +80.0°C, crit = +100.0°C)
```

## CPU資訊
> Linux系統會將部分CPU的資訊即時地存在於記憶體中，對應的檔案路徑在「/proc/cpuinfo」
```shell
$ cat /proc/cpuinfo
processor	: 0
vendor_id	: GenuineIntel
cpu family	: 6
model		: 60
model name	: Intel(R) Xeon(R) CPU E3-1230 v3 @ 3.30GHz
stepping	: 3
microcode	: 0x27
cpu MHz		: 2998.230
cache size	: 8192 KB
physical id	: 0
siblings	: 8
core id		: 0
cpu cores	: 4
apicid		: 0
initial apicid	: 0
fpu		: yes
fpu_exception	: yes
cpuid level	: 13
wp		: yes
flags		: fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx pdpe1gb rdtscp lm constant_tsc arch_perfmon pebs bts rep_good nopl xtopology nonstop_tsc aperfmperf pni pclmulqdq dtes64 monitor ds_cpl vmx smx est tm2 ssse3 sdbg fma cx16 xtpr pdcm pcid sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand lahf_lm abm epb invpcid_single ssbd ibrs ibpb stibp pti tpr_shadow vnmi flexpriority ept vpid fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid xsaveopt dtherm ida arat pln pts md_clear flush_l1d
bugs		: cpu_meltdown spectre_v1 spectre_v2 spec_store_bypass l1tf mds
bogomips	: 6584.79
clflush size	: 64
cache_alignment	: 64
address sizes	: 39 bits physical, 48 bits virtual
power management:

......

processor	: 7
vendor_id	: GenuineIntel
cpu family	: 6
model		: 60
model name	: Intel(R) Xeon(R) CPU E3-1230 v3 @ 3.30GHz
stepping	: 3
microcode	: 0x27
cpu MHz		: 3131.132
cache size	: 8192 KB
physical id	: 0
siblings	: 8
core id		: 3
cpu cores	: 4
apicid		: 7
initial apicid	: 7
fpu		: yes
fpu_exception	: yes
cpuid level	: 13
wp		: yes
flags		: fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx pdpe1gb rdtscp lm constant_tsc arch_perfmon pebs bts rep_good nopl xtopology nonstop_tsc aperfmperf pni pclmulqdq dtes64 monitor ds_cpl vmx smx est tm2 ssse3 sdbg fma cx16 xtpr pdcm pcid sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand lahf_lm abm epb invpcid_single ssbd ibrs ibpb stibp pti tpr_shadow vnmi flexpriority ept vpid fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid xsaveopt dtherm ida arat pln pts md_clear flush_l1d
bugs		: cpu_meltdown spectre_v1 spectre_v2 spec_store_bypass l1tf mds
bogomips	: 6584.79
clflush size	: 64
cache_alignment	: 64
address sizes	: 39 bits physical, 48 bits virtual
power management:

#邏輯CPU個數
$ cat /proc/cpuinfo | grep "processor" | wc -l

#物理CPU個數：
$ cat /proc/cpuinfo | grep "physical id" | sort | uniq | wc -l
```

## 查看資源使用率
### memory
```shell
$ free -m
```
### CPU
```shell
$ top
```
### 高級工具
```shell
$ sudo apt-get install htop
$ htop
```

## 查看已使用的port
```
$ sudo netstat -tulpn
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 10.0.1.11:3306          0.0.0.0:*               LISTEN      10684/mysqld    
tcp        0      0 10.0.1.11:11211         0.0.0.0:*               LISTEN      24891/memcached 
tcp        0      0 0.0.0.0:9292            0.0.0.0:*               LISTEN      17043/python2   
tcp        0      0 0.0.0.0:4369            0.0.0.0:*               LISTEN      11712/epmd      
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      1528/sshd
```

```shell
$ netstat -nlpt | grep
```

## 指令
### sed
> 將filename中abc取代為xyz
```shell
$ sed -i 's/abc/xyz/g' filename.txt
```
### netstat-列出所有連接Port
```shell
$ netstat -a
# 本地port狀態
$ netstat -tnl
```
### telnet測試IP
```shell
$ telnet 127.0.0.1
```
### VM新增Remote Tunnel
> [https://linuxize.com/post/how-to-setup-ssh-tunneling/](https://linuxize.com/post/how-to-setup-ssh-tunneling/)

### iptables VM封包轉發
參考資料:
> [https://aboullaite.me/kvm-qemo-forward-ports-with-iptables/](https://aboullaite.me/kvm-qemo-forward-ports-with-iptables/)
> [https://linadonis.pixnet.net/blog/post/32506940](https://linadonis.pixnet.net/blog/post/32506940)
```shell
$ virsh net-list
 Name                 State      Autostart     Persistent
----------------------------------------------------------
 default              active     yes           yes

$ virsh net-dumpxml default
<network connections='4'>
  <name>default</name>
  <uuid>69b6304a-dcc4-4a89-9dca-ca5f32a0b3d2</uuid>
  <forward mode='nat'>
    <nat>
      <port start='1024' end='65535'/>
    </nat>
  </forward>
  <bridge name='virbr0' stp='on' delay='0'/>
  <mac address='52:54:00:e8:d7:fd'/>
  <ip address='192.168.122.1' netmask='255.255.255.0'>
    <dhcp>
      <range start='192.168.122.2' end='192.168.122.254'/>
    </dhcp>
  </ip>
</network>

$ iptables -I FORWARD -o virbr0 -d  192.168.122.17 -j ACCEPT
root@monitor-server:/home/ubuntu# iptables -L -v -n | more
Chain INPUT (policy ACCEPT 45 packets, 75456 bytes)
 pkts bytes target     prot opt in     out     source               destination
  665 48936 ACCEPT     udp  --  virbr0 *       0.0.0.0/0            0.0.0.0/0            udp dpt:53
    0     0 ACCEPT     tcp  --  virbr0 *       0.0.0.0/0            0.0.0.0/0            tcp dpt:53
  750  238K ACCEPT     udp  --  virbr0 *       0.0.0.0/0            0.0.0.0/0            udp dpt:67
    0     0 ACCEPT     tcp  --  virbr0 *       0.0.0.0/0            0.0.0.0/0            tcp dpt:67

Chain FORWARD (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination
    1   156 ACCEPT     all  --  *      virbr0  0.0.0.0/0            192.168.122.17
1101K   12G ACCEPT     all  --  *      virbr0  0.0.0.0/0            192.168.122.0/24     ctstate RELATED,ESTABLISHED
1087K   69M ACCEPT     all  --  virbr0 *       192.168.122.0/24     0.0.0.0/0
    0     0 ACCEPT     all  --  virbr0 virbr0  0.0.0.0/0            0.0.0.0/0
  319 16588 REJECT     all  --  *      virbr0  0.0.0.0/0            0.0.0.0/0            reject-with icmp-port-unreachable
    0     0 REJECT     all  --  virbr0 *       0.0.0.0/0            0.0.0.0/0            reject-with icmp-port-unreachable

Chain OUTPUT (policy ACCEPT 35 packets, 149K bytes)
 pkts bytes target     prot opt in     out     source               destination
  750  247K ACCEPT     udp  --  *      virbr0  0.0.0.0/0            0.0.0.0/0            udp dpt:68

$ iptables -t nat -A PREROUTING -p tcp -i eth0 --dport 3000 -j DNAT --to-destination 192.168.122.17:3000
$ iptables -A INPUT -i eth0 -p tcp --dport 3000 -j ACCEPT

```

```shell
# ssh 服務器偵聽端口8080，並將所有流量從此端口隧道傳輸到端口上的本地計算機3000
$ ssh -R 8080:127.0.0.1:3000 -N -f user@remote.host
```

## iptables指令
### 列出所有規則，前面加上行號
```shell
$ iptables -L INPUT -n --line-numbers
```

### 刪除某一行的規則
```shell
$ iptables -D INPUT {預計刪除規則行數1}
```

## Wake on LAN
> Ubuntu 18.04
1. Install ethtool with
```shell
$ sudo apt-get install ethtool
```
2. Run the command
```shell
$ sudo ethtool -s eno1 wol g
```
3. On Ubuntu 18.04, you need to create a systemd service as opposed to enabling, creating and/or modifying rc.local as you would’ve done on previous versions. So, navigate to
```shell
$ cd /etc/systemd/system
$ sudo vim wol.service
[Unit]
Description=Configure Wake-up on LAN

[Service]
Type=oneshot
ExecStart=/sbin/ethtool -s eno1 wol g

[Install]
WantedBy=basic.target
```
4. Once you’ve created your file, you need to add it to the systemd services so you should run
```shell
$ sudo systemctl daemon-reload
$ sudo systemctl enable wol.service
$ sudo systemctl start wol.service
```
## remove cloud-init
> Ubuntu 18.04
```shell
$ echo 'datasource_list: [ None ]' | sudo -s tee /etc/cloud/cloud.cfg.d/90_dpkg.cfg
$ sudo apt-get purge cloud-init
$ sudo rm -rf /etc/cloud/; sudo rm -rf /var/lib/cloud/
$ reboot
```

## 誤刪/etc/fstab
```
$ mount -o remount rw /
$ 更改回去
$ sudo init 6
```

## 問題解決
### E: Sub-process /usr/bin/dpkg returned an error code
```
$ sudo mv /var/lib/dpkg/info /var/lib/dpkg/info.bak
$ sudo mkdir /var/lib/dpkg/info
$ sudo apt-get update
```
