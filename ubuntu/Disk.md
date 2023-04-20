# Disk
## (1) lsblk -o NAME,FSTYPE,SIZE,MOUNTPOINT,LABEL

```shell
NAME   FSTYPE  SIZE MOUNTPOINT LABEL
sda            3.7T
├─sda1 vfat    512M /boot/efi
├─sda2         100G
├─sda3 swap     64G [SWAP]
└─sda4 ext4      3T /
```

## (2) fdisk -l
參考資料: http://www.j4.com.tw/comp-qna/ubuntu-%E6%96%B0%E5%A2%9E%E7%A1%AC%E7%A2%9F%EF%BC%88%E7%A3%81%E7%A2%9F%E5%88%86%E5%89%B2%E3%80%81%E6%A0%BC%E5%BC%8F%E5%8C%96%E8%88%87%E6%8E%9B%E8%BC%89%EF%BC%89/

```shell
Disk /dev/sda: 3.7 TiB, 3999688294400 bytes, 7811891200 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: gpt
Disk identifier: D4A7E96E-600D-41AC-B3DF-EA0DDF3121DF

Device         Start        End    Sectors  Size Type
/dev/sda1       2048    1050623    1048576  512M EFI System
/dev/sda2    1050624  210765823  209715200  100G Linux filesystem
/dev/sda3  210765824  344983551  134217728   64G Linux swap
/dev/sda4  344983552 6787434495 6442450944    3T Linux filesystem
```

## (3)	sudo parted -l
參考資料: https://superuser.com/questions/1352065/gpt-pmbr-size-mismatch-will-be-corrected-by-write

```shell
Model: DELL PERC H710 (scsi)
Disk /dev/sda: 4000GB
Sector size (logical/physical): 512B/512B
Partition Table: gpt
Disk Flags:

Number  Start   End     Size    File system     Name  Flags
 1      1049kB  538MB   537MB   fat32                 boot, esp
 2      538MB   108GB   107GB
 3      108GB   177GB   68.7GB  linux-swap(v1)
 4      177GB   3475GB  3299GB  ext4
```

## (4) fdisk /dev/sda
```shell
Welcome to fdisk (util-linux 2.31.1).
Changes will remain in memory only, until you decide to write them.
Be careful before using the write command.


Command (m for help): n
Partition number (5-128, default 5): 5
First sector (6787434496-7811891166, default 6787434496): 6787434496
Last sector, +sectors or +size{K,M,G,T,P} (6787434496-7811891166, default 7811891166): +20G

Created a new partition 5 of type 'Linux filesystem' and of size 20 GiB.

Command (m for help): w
The partition table has been altered.
Syncing disks.
```