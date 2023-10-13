# IST_labo2

## TASK 1 : CREATE PHYSICAL VOLUMES

1) Reset your external disk. Using parted remove all partitions, or simply write a new partition table.
```shell
ubuntu@IST:~$ sudo parted /dev/loop3
GNU Parted 3.4
Using /dev/loop3
Welcome to GNU Parted! Type 'help' to view a list of commands.
(parted) print                                                            
Model: Loopback device (loopback)
Disk /dev/loop3: 1258MB
Sector size (logical/physical): 512B/512B
Partition Table: loop
Disk Flags: 

Number  Start  End     Size    File system  Flags
 1      0.00B  1258MB  1258MB  ext4

(parted) mklabel gpt
Warning: Partition(s) on /dev/loop3 are being used.
Ignore/Cancel? Ignore                                                     
Warning: The existing disk label on /dev/loop3 will be destroyed and all data on this disk will be lost. Do you want to
continue?
Yes/No? Yes                                                               
(parted) print                                                            
Model: Loopback device (loopback)
Disk /dev/loop3: 1258MB
Sector size (logical/physical): 512B/512B
Partition Table: gpt
Disk Flags: 

Number  Start  End  Size  File system  Name  Flags

```

2) Create four partitions with these characteristics: primary, 25 MB size, type ext4
```shell
ubuntu@IST:~$ sudo parted /dev/loop3
GNU Parted 3.3
Using /dev/loop3
Welcome to GNU Parted! Type 'help' to view a list of commands.
(parted) unit MB
(parted) mkpart primary ext4 1 25                                         
(parted) mkpart primary ext4 25 50                              
(parted) mkpart primary ext4 50 75                                     
(parted) mkpart primary ext4 75 100
(parted) print
Model: Loopback device (loopback)
Disk /dev/loop3: 1258MB
Sector size (logical/physical): 512B/512B
Partition Table: gpt
Disk Flags: 

Number  Start   End     Size    File system  Name     Flags
 1      1.05MB  25.2MB  24.1MB  ext4         primary
 2      25.2MB  50.3MB  25.2MB  ext4         primary
 3      50.3MB  75.5MB  25.2MB  ext4         primary
 4      75.5MB  99.6MB  24.1MB  ext4         primary
```

3) List the available LVM commands. They belong to the Debian package lvm2 which should already be installed. Use dpkg
with the -L option to list the content of the package. The commands are all located in the /sbin directory. Use grep to
filter and sort to sort alphabetically.
```shell
ubuntu@IST:~$ dpkg -L lvm2 | grep -E '^/sbin/' | sort | column
/sbin/fsadm		/sbin/lvmpolld		/sbin/pvck		/sbin/vgchange		/sbin/vgmknodes
/sbin/lvchange		/sbin/lvmsadc		/sbin/pvcreate		/sbin/vgck		/sbin/vgreduce
/sbin/lvconvert		/sbin/lvmsar		/sbin/pvdisplay		/sbin/vgconvert		/sbin/vgremove
/sbin/lvcreate		/sbin/lvreduce		/sbin/pvmove		/sbin/vgcreate		/sbin/vgrename
/sbin/lvdisplay		/sbin/lvremove		/sbin/pvremove		/sbin/vgdisplay		/sbin/vgs
/sbin/lvextend		/sbin/lvrename		/sbin/pvresize		/sbin/vgexport		/sbin/vgscan
/sbin/lvm		/sbin/lvresize		/sbin/pvs		/sbin/vgextend		/sbin/vgsplit
/sbin/lvmconfig		/sbin/lvs		/sbin/pvscan		/sbin/vgimport
/sbin/lvmdiskscan	/sbin/lvscan		/sbin/vgcfgbackup	/sbin/vgimportclone
/sbin/lvmdump		/sbin/pvchange		/sbin/vgcfgrestore	/sbin/vgmerge
```

4) List all partitions that could potentially host a Physical Volume by using pvs with the --all option
```shell
ubuntu@IST:~$ sudo pvs --all
  PV           VG Fmt Attr PSize PFree
  /dev/loop0          ---     0     0 
  /dev/loop1          ---     0     0 
  /dev/loop2          ---     0     0 
  /dev/loop3          ---     0     0 
  /dev/loop3p1        ---     0     0 
  /dev/loop3p2        ---     0     0 
  /dev/loop3p3        ---     0     0 
  /dev/loop3p4        ---     0     0 
  /dev/sda1           ---     0     0 
  /dev/sda15          ---     0     0 
```

5) On the four partitions of your external disk, create four Physical Volumes using pvcreate. Add the -vv option so
that it tells you in detail what it is doing. For the first partition copy the output of the command into the report,
but copy only the lines about the partition that receives the Physical Volume and ignore the other messages
```shell
ubuntu@IST:~$ sudo pvcreate -vv /dev/loop3p1
  Locking /run/lock/lvm/P_global WB
  /dev/loop3p1: size is 47104 sectors
  /dev/loop3p1: using cached size 47104 sectors
  /dev/loop3p1: using cached size 47104 sectors
  /dev/loop3p1: No lvm label detected
  Processing device /dev/loop3p1.
  /dev/loop3p1: No lvm label detected
  Wiping signatures on new PV /dev/loop3p1.
  /dev/loop3p1: using cached size 47104 sectors
  devices/default_data_alignment not found in config: defaulting to 1
  Device /dev/loop3p1: queue/minimum_io_size is 512 bytes.
  Device /dev/loop3p1: queue/optimal_io_size is 0 bytes.
  Device /dev/loop3p1: alignment_offset is 0 bytes.
  Set up physical volume for "/dev/loop3p1" with 47104 available sectors.
  Scanning for labels to wipe from /dev/loop3p1
  Zeroing start of device /dev/loop3p1.
  Writing physical volume data to disk "/dev/loop3p1".
  /dev/loop3p1: Writing label to sector 1 with stored offset 32.
  Physical volume "/dev/loop3p1" successfully created.
  Unlocking /run/lock/lvm/P_global
```

```shell
ubuntu@IST:~$ sudo pvcreate /dev/loop3p2
  Physical volume "/dev/loop3p2" successfully created.
```

```shell
ubuntu@IST:~$ sudo pvcreate /dev/loop3p3
  Physical volume "/dev/loop3p3" successfully created.
```

```shell
ubuntu@IST:~$ sudo pvcreate /dev/loop3p4
  Physical volume "/dev/loop3p4" successfully created.
```

6) Display detailed information about the first Physical Volume using pvdisplay
```shell
ubuntu@IST:~$ sudo pvdisplay /dev/loop3p1
  "/dev/loop3p1" is a new physical volume of "23.00 MiB"
  --- NEW Physical volume ---
  PV Name               /dev/loop3p1
  VG Name               
  PV Size               23.00 MiB
  Allocatable           NO
  PE Size               0   
  Total PE              0
  Free PE               0
  Allocated PE          0
  PV UUID               2MRxkY-8phV-DYhk-vS56-EQnI-OWMN-JK5o8M
```
