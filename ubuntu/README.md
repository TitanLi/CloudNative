# Ubuntu
----

## Table of Contents
* [密碼設定](#密碼設定)
* [格式化硬碟](#格式化硬碟)
* [查看CPU的溫度](#查看CPU的溫度)
* [CPU資訊](#CPU資訊)

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