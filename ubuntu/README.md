# Ubuntu
----

## Table of Contents
* [密碼設定](#密碼設定)
* [設定IP](#設定ip)
* [設定網路CLI](#設定網路cli)
* [Ubuntu 18.04](#ubuntu-18.04)
  - [DNS](#dns)
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
* [Wake on LAN](#wake-on-lan)
* [問題解決](#問題解決)
  - [E: Sub-process /usr/bin/dpkg returned an error code](#e-sub-process-usrbindpkg-returned-an-error-code)
----

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

## 設定網路CLI
```shell
$ sudo ifconfig eno1 192.168.2.99 netmask 255.255.254.0
$ sudo route add default gw 192.168.3.254 eno1
$ route -n
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
```
方法二：

[https://jermine.vdo.pub/linux/ubuntu18.04%E4%BF%AE%E6%94%B9dns/](https://jermine.vdo.pub/linux/ubuntu18.04%E4%BF%AE%E6%94%B9dns/)

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

## 指令
### sed
> 將filename中abc取代為xyz
```shell
$ sed -i 's/abc/xyz/g' filename.txt
```
### netstat-列出所有連接Port
```shell
$ netstat -a
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

## 問題解決
### E: Sub-process /usr/bin/dpkg returned an error code
```
$ sudo mv /var/lib/dpkg/info /var/lib/dpkg/info.bak
$ sudo mkdir /var/lib/dpkg/info
$ sudo apt-get update
```