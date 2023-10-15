# IST_labo2
Authors: Valzino Benjamin, Urizar Pablo
### TASK 1 : CREATE PHYSICAL VOLUMES

**1. Reset your external disk. Using parted remove all partitions, or simply write a new partition table.**
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

**2. Create four partitions with these characteristics: primary, 25 MB size, type ext4**
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

**3. List the available LVM commands. They belong to the Debian package lvm2 which should already be installed. Use dpkg
with the -L option to list the content of the package. The commands are all located in the /sbin directory. Use grep to
filter and sort to sort alphabetically.**
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

**4. List all partitions that could potentially host a Physical Volume by using pvs with the --all option**
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

**5. On the four partitions of your external disk, create four Physical Volumes using pvcreate. Add the -vv option so
that it tells you in detail what it is doing. For the first partition copy the output of the command into the report,
but copy only the lines about the partition that receives the Physical Volume and ignore the other messages**
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

**6. Display detailed information about the first Physical Volume using pvdisplay**
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
### TASK 2: CREATE TWO VOLUME GROUPS

**1. Create a first Volume Group lab-vg1 that contains only the first Physical Volume. Display the Physical Volume again with pvdisplay. What has changed?**

First we can see that the Physical Volume is now associated with the lab-vg1 volume group. 
It is also marked as allocatable,
it's PE size is specified at 4MB, the total PE is now 5 which indicates that it has been divided into 5 physical extents.
Free PE indicates that no space is allocated yet since it's at 5.
And Allocated PE is at 0 confirming that no extents are allocated to any logical volume yet.

```shell
ben@ben-virtual-machine:~/Desktop$ sudo vgcreate lab-vg1 /dev/sdb1
  Volume group "lab-vg1" successfully created
ben@ben-virtual-machine:~/Desktop$ sudo pvdisplay /dev/sdb1
  --- Physical volume ---
  PV Name               /dev/sdb1
  VG Name               lab-vg1
  PV Size               <23.83 MiB / not usable <3.83 MiB
  Allocatable           yes 
  PE Size               4.00 MiB
  Total PE              5
  Free PE               5
  Allocated PE          0
  PV UUID               9mpimn-1iAu-aZFl-1mQd-LbcF-j9Kb-YP5rx7
```

**2. Create a second Volume Group lab-vg2 that contains Physical Volumes 2 and 3.**


```shell
ben@ben-virtual-machine:~/Desktop$ sudo vgcreate lab-vg2 /dev/sdb2 /dev/sdb3
  Volume group "lab-vg2" successfully created
ben@ben-virtual-machine:~/Desktop$ sudo vgdisplay lab-vg2
  --- Volume group ---
  VG Name               lab-vg2
  System ID             
  Format                lvm2
  Metadata Areas        2
  Metadata Sequence No  1
  VG Access             read/write
  VG Status             resizable
  MAX LV                0
  Cur LV                0
  Open LV               0
  Max PV                0
  Cur PV                2
  Act PV                2
  VG Size               40.00 MiB
  PE Size               4.00 MiB
  Total PE              10
  Alloc PE / Size       0 / 0   
  Free  PE / Size       10 / 40.00 MiB
  VG UUID               4lnev9-VysM-ecmZ-Tadh-Y7oN-mh0Q-TnyL4A
```

**3. List all Volume Groups with vgs. Then list all Physical Volumes with pvs. What do you see?**

We can see that the physical partitions that are in logical volume groups now have 20mb of free space instead of roughly 25mb it had previously.
(ADD MORE, IDK )

```shell
ben@ben-virtual-machine:~/Desktop$ sudo vgs
  VG      #PV #LV #SN Attr   VSize  VFree 
  lab-vg1   1   0   0 wz--n- 20.00m 20.00m
  lab-vg2   2   0   0 wz--n- 40.00m 40.00m
ben@ben-virtual-machine:~/Desktop$ sudo pvs
  PV         VG      Fmt  Attr PSize  PFree 
  /dev/sdb1  lab-vg1 lvm2 a--  20.00m 20.00m
  /dev/sdb2  lab-vg2 lvm2 a--  20.00m 20.00m
  /dev/sdb3  lab-vg2 lvm2 a--  20.00m 20.00m
  /dev/sdb4          lvm2 ---  23.00m 23.00m
```

### TASK 3: CREATE LOGICAL VOLUMES

**1. On the Volume Group lab-vg1 create a Logical Volume of size 20 MB with the command lvcreate -L 20M lab-vg1.**

```shell
ben@ben-virtual-machine:~/Desktop$ sudo lvcreate -L 20M -n lvtest lab-vg1
  Logical volume "lvtest" created.
ben@ben-virtual-machine:~/Desktop$ sudo lvdisplay
  --- Logical volume ---
  LV Path                /dev/lab-vg1/lvtest
  LV Name                lvtest
  VG Name                lab-vg1
  LV UUID                b7M2CP-RkrY-PQ5L-1Jib-CXCo-emN4-CeYiRX
  LV Write Access        read/write
  LV Creation host, time ben-virtual-machine, 2023-10-15 08:52:46 +0200
  LV Status              available
  # open                 0
  LV Size                20.00 MiB
  Current LE             5
  Segments               1
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     256
  Block device           253:0
```

**2. Verify hat the new volume appears when you use lvs to list Logical Volumes. Also verify that it appears when you use lsblk to list the block devices. What is the name of the special file in /dev that represents the volume?**

```shell
ben@ben-virtual-machine:~/Desktop$ sudo lvs
  LV     VG      Attr       LSize  Pool Origin Data%  Meta%  Move Log Cpy%Sync Convert
  lvtest lab-vg1 -wi-a----- 20.00m    
```

```shell
sdb                   8:16   0     1G  0 disk 
├─sdb1                8:17   0  23.8M  0 part 
│ └─lab--vg1-lvtest 253:0    0    20M  0 lvm  
```

As we can see below, the name of the special file is simply lab-vg1 in /dev

```shell
ben@ben-virtual-machine:/dev$ ls -ls /dev | grep lab-vg1
0 drwxr-xr-x  2 root root          60 Okt 15 08:52 lab-vg1
```

**3. Create an ext4 file system on the volume. Mount the volume. Fill the file system with a 14 MB file using dd (Google it).**

```shell
ben@ben-virtual-machine:/dev$ sudo mkfs.ext4 /dev/lab-vg1/lvtest
mke2fs 1.46.5 (30-Dec-2021)
Creating filesystem with 5120 4k blocks and 5120 inodes

Allocating group tables: done                            
Writing inode tables: done                            
Creating journal (1024 blocks): done
Writing superblocks and filesystem accounting information: done

ben@ben-virtual-machine:/dev$ sudo mkdir /mnt/lvtest
ben@ben-virtual-machine:/dev$ sudo mount /dev/lab-vg1/lvtest /mnt/lvtest/
ben@ben-virtual-machine:/dev$ sudo dd if=/dev/zero of=/mnt/lvtest/14MBfile bs=1M count=14
14+0 records in
14+0 records out
14680064 bytes (15 MB, 14 MiB) copied, 0.0132928 s, 1.1 GB/s
```

**4. On the Volume Group lab-vg2 create another Logical Volume of size 20 MB, create an ext4 file system on it and mount it. Create a file named foo that contains the text 111.**

```shell
ben@ben-virtual-machine:/dev$ sudo mkfs.ext4 /dev/lab-vg2/lvtest2 
mke2fs 1.46.5 (30-Dec-2021)
Creating filesystem with 5120 4k blocks and 5120 inodes

Allocating group tables: done                            
Writing inode tables: done                            
Creating journal (1024 blocks): done
Writing superblocks and filesystem accounting information: done

ben@ben-virtual-machine:/dev$ sudo mkdir /mnt/lvtest2
ben@ben-virtual-machine:/dev$ sudo mount /dev/lab-vg2/lvtest2 /mnt/lvtest2
ben@ben-virtual-machine:/dev$ echo "111" | sudo tee /mnt/lvtest2/foo
111
ben@ben-virtual-machine:/dev$ cat /mnt/lvtest2/foo
111
```

### TASK 4: GROW A FILE SYSTEM WHILE IT IS IN USE

**1. Verify that the file system is indeed full (use df -h).**

```shell
ben@ben-virtual-machine:/dev$ df -h
Filesystem                    Size  Used Avail Use% Mounted on
/dev/mapper/lab--vg1-lvtest    15M   15M     0 100% /mnt/lvtest
```

**2. Verify that the Volume Group is full (use vgs).**


```shell
ben@ben-virtual-machine:/dev$ sudo vgs
  VG      #PV #LV #SN Attr   VSize  VFree 
  lab-vg1   1   1   0 wz--n- 20.00m     0 
```

**3. Extend the Volume group using vgextend and verify with vgs.**


```shell
ben@ben-virtual-machine:/dev$ sudo vgextend lab-vg1 /dev/sdb4
  Volume group "lab-vg1" successfully extended
ben@ben-virtual-machine:/dev$ sudo vgs
  VG      #PV #LV #SN Attr   VSize  VFree 
  lab-vg1   2   1   0 wz--n- 40.00m 20.00m
```

**4. Extend the Logical Volume by an additional 20 MB using lvextend --size <new_size> <volume_group>/<logical_volume>.**

```shell
ben@ben-virtual-machine:/dev$ sudo lvextend --size +20M /dev/lab-vg1/lvtest
  Size of logical volume lab-vg1/lvtest changed from 20.00 MiB (5 extents) to 40.00 MiB (10 extents).
  Logical volume lab-vg1/lvtest successfully resized.
ben@ben-virtual-machine:/dev$ sudo vgs
  VG      #PV #LV #SN Attr   VSize  VFree 
  lab-vg1   2   1   0 wz--n- 40.00m     0 
  lab-vg2   2   1   0 wz--n- 40.00m 20.00m
ben@ben-virtual-machine:/dev$ sudo lvdisplay /dev/lab-vg1/lvtest
  --- Logical volume ---
  LV Path                /dev/lab-vg1/lvtest
  LV Name                lvtest
  VG Name                lab-vg1
  LV UUID                b7M2CP-RkrY-PQ5L-1Jib-CXCo-emN4-CeYiRX
  LV Write Access        read/write
  LV Creation host, time ben-virtual-machine, 2023-10-15 08:52:46 +0200
  LV Status              available
  # open                 1
  LV Size                40.00 MiB
  Current LE             10
  Segments               2
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     256
  Block device           253:0
```

**5. Grow the file system while it is mounted using resize2fs and verify its new capacity with df -h. Note: not all file systems support growing while being mounted. In that case you have to stop all applications using the file system, unmount, grow, remount, and restart the applications.**

```shell
ben@ben-virtual-machine:/dev$ sudo resize2fs /dev/lab-vg1/lvtest 
resize2fs 1.46.5 (30-Dec-2021)
Filesystem at /dev/lab-vg1/lvtest is mounted on /mnt/lvtest; on-line resizing required
old_desc_blocks = 1, new_desc_blocks = 1
The filesystem on /dev/lab-vg1/lvtest is now 10240 (4k) blocks long.

ben@ben-virtual-machine:/dev$ df -h
Filesystem                    Size  Used Avail Use% Mounted on
tmpfs                         388M  2.0M  386M   1% /run
/dev/sda3                      20G   13G  5.3G  72% /
tmpfs                         1.9G     0  1.9G   0% /dev/shm
tmpfs                         5.0M  4.0K  5.0M   1% /run/lock
/dev/sda2                     512M  6.1M  506M   2% /boot/efi
tmpfs                         388M  108K  388M   1% /run/user/1000
/dev/sr1                      4.7G  4.7G     0 100% /media/ben/Ubuntu 22.04.3 LTS amd64
/dev/sr0                      156M  156M     0 100% /media/ben/CDROM
/dev/mapper/lab--vg1-lvtest    35M   15M   20M  43% /mnt/lvtest
/dev/mapper/lab--vg2-lvtest2   15M   28K   14M   1% /mnt/lvtest2
```

### TASK 5: CREATE A SNAPSHOT

**1. Create a snapshot volume using the --snapshot option of lvcreate. Use the --name option to give it the name snap. You also need to specify a size for the snapshot with the --size option. Remember that initially a snapshot does not consume any storage blocks as the data in the original volume and the snapshot volume is identical. It is only when the data in the two volumes starts deviating that storage blocks are needed. The size of the snapshot determines how many data blocks can be different.**

```shell
ben@ben-virtual-machine:/dev$ sudo lvcreate --snapshot --name snap --size 10M /dev/lab-vg2/lvtest2
  Rounding up size to full physical extent 12.00 MiB
  Logical volume "snap" created.
```

**2. Display an overview of all Logical Volumes using lvs. Which column shows the name of the original volume?**

The original column indicates the name of the original volume.

```shell
ben@ben-virtual-machine:/dev$ sudo lvs
  LV      VG      Attr       LSize  Pool Origin  Data%  Meta%  Move Log Cpy%Sync Convert
  lvtest  lab-vg1 -wi-ao---- 40.00m                                                     
  lvtest2 lab-vg2 owi-aos--- 20.00m                                                     
  snap    lab-vg2 swi-a-s--- 12.00m      lvtest2 0.10  
```

**3. Display the charactersticts of the snapshot volume using lvdisplay.**

Here's the whole ouput:

```shell
ben@ben-virtual-machine:/dev$ sudo lvdisplay
  --- Logical volume ---
  LV Path                /dev/lab-vg2/lvtest2
  LV Name                lvtest2
  VG Name                lab-vg2
  LV UUID                xAapOO-IeDs-alPk-aK6v-wfbP-NRyf-Hdhtbf
  LV Write Access        read/write
  LV Creation host, time ben-virtual-machine, 2023-10-15 08:59:44 +0200
  LV snapshot status     source of
                         snap [active]
  LV Status              available
  # open                 1
  LV Size                20.00 MiB
  Current LE             5
  Segments               1
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     256
  Block device           253:1
   
  --- Logical volume ---
  LV Path                /dev/lab-vg2/snap
  LV Name                snap
  VG Name                lab-vg2
  LV UUID                yynHiC-qiPm-8KKI-FxA2-1G78-udIL-ls1cjw
  LV Write Access        read/write
  LV Creation host, time ben-virtual-machine, 2023-10-15 09:12:58 +0200
  LV snapshot status     active destination for lvtest2
  LV Status              available
  # open                 0
  LV Size                20.00 MiB
  Current LE             5
  COW-table size         12.00 MiB
  COW-table LE           3
  Allocated to snapshot  0.10%
  Snapshot chunk size    4.00 KiB
  Segments               1
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     256
  Block device           253:4
   
  --- Logical volume ---
  LV Path                /dev/lab-vg1/lvtest
  LV Name                lvtest
  VG Name                lab-vg1
  LV UUID                b7M2CP-RkrY-PQ5L-1Jib-CXCo-emN4-CeYiRX
  LV Write Access        read/write
  LV Creation host, time ben-virtual-machine, 2023-10-15 08:52:46 +0200
  LV Status              available
  # open                 1
  LV Size                40.00 MiB
  Current LE             10
  Segments               2
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     256
  Block device           253:0
   
```

**What line shows the name of the original volume?**

```shell
LV snapshot status     active destination for lvtest2
```

**What line shows the size of the original volume?**

```shell
  LV Size                20.00 MiB
```

**What line shows the space allocated for the snapshot volume?**

```shell
Allocated to snapshot  0.10%
```

**What does COW stand for?**

COW stands for Copy-on-Write. It's a technique used in storage systems and file systems, where data is only copied when it is modified.
It's essentially used to minimize data duplication and optimize storage space usage.

**4. Mount the snapshot volume. Using the file foo you created earlier verify that the two volumes behave like independent copies.**

```shell
ben@ben-virtual-machine:/dev$ sudo mkdir /mnt/snap
ben@ben-virtual-machine:/dev$ sudo mount /dev/lab-vg2/snap /mnt/snap
ben@ben-virtual-machine:/dev$ cat /mnt/lvtest2/foo
111
ben@ben-virtual-machine:/dev$ cat /mnt/snap/foo
111
ben@ben-virtual-machine:/dev$ echo "222" | sudo tee /mnt/snap/foo
222
ben@ben-virtual-machine:/dev$ cat /mnt/lvtest2/foo
111
ben@ben-virtual-machine:/dev$ cat /mnt/snap/foo
222
```

**5. Make the data of the original volume change completely by using the dd command to write a new file of 14 MB size. Run df -h to see how it affects the fullness of the original volume and the snapshot. What do you see?**

```shell
ben@ben-virtual-machine:/dev$ sudo dd if=/dev/zero of=/dev/lab-vg2/lvtest2 bs=1M count=14
14+0 records in
14+0 records out
14680064 bytes (15 MB, 14 MiB) copied, 0.0120891 s, 1.2 GB/s
ben@ben-virtual-machine:/dev$ df -h
Filesystem                    Size  Used Avail Use% Mounted on
tmpfs                         388M  2.0M  386M   1% /run
/dev/sda3                      20G   13G  5.3G  72% /
tmpfs                         1.9G     0  1.9G   0% /dev/shm
tmpfs                         5.0M  4.0K  5.0M   1% /run/lock
/dev/sda2                     512M  6.1M  506M   2% /boot/efi
tmpfs                         388M  108K  388M   1% /run/user/1000
/dev/sr1                      4.7G  4.7G     0 100% /media/ben/Ubuntu 22.04.3 LTS amd64
/dev/sr0                      156M  156M     0 100% /media/ben/CDROM
/dev/mapper/lab--vg1-lvtest    35M   15M   20M  43% /mnt/lvtest
/dev/mapper/lab--vg2-lvtest2   64Z   64Z   15M 100% /mnt/lvtest2
/dev/mapper/lab--vg2-snap      15M   28K   14M   1% /mnt/snap
```

*The way that you allocated it, is the snapshot volume able support a change of 14 MB of data?*
*What happened? Why?*

No. The snapshot volume size isn't able to accommodate the full 14MB since we defined it as 12MB max. 
When we changed the data in the original volume using dd, the 14MB exceed the available space in the snapshot.
As a result, the snapshot will most likely become invalid.


**6 .Remove the broken snapshot volume.**

```shell
ben@ben-virtual-machine:/dev$ sudo lvremove /dev/lab-vg2/snap
Do you really want to remove and DISCARD active logical volume lab-vg2/snap? [y/n]: y
  Logical volume "snap" successfully removed
```

**7. Redo the above, this time allocating sufficient space to the snapshot volume to support a complete change of data of the original volume.**

```shell
ben-virtual-machine:/dev$ sudo lvcreate --size 16M --snapshot --name snap /dev/lab-vg2/lvtest2
  Logical volume "snap" created.
ben@ben-virtual-machine:/dev$ sudo lvdisplay /dev/lab-vg2/snap
  --- Logical volume ---
  LV Path                /dev/lab-vg2/snap
  LV Name                snap
  VG Name                lab-vg2
  LV UUID                JeAwX5-xoPI-rTHe-7INc-EUmj-t21k-aQUCwu
  LV Write Access        read/write
  LV Creation host, time ben-virtual-machine, 2023-10-15 09:31:35 +0200
  LV snapshot status     active destination for lvtest2
  LV Status              available
  # open                 0
  LV Size                20.00 MiB
  Current LE             5
  COW-table size         16.00 MiB
  COW-table LE           4
  Allocated to snapshot  0.07%
  Snapshot chunk size    4.00 KiB
  Segments               1
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     256
  Block device           253:4
```

The rest is the same as previously but this time the snapshot is in working conditions.

TASK 6 (OPTIONAL): PROVISION A THIN VOLUME AND SNAPSHOT IT

Remove all Logical Volumes from Volume Group lab-vg2.

```shell
ben@ben-virtual-machine:/dev$ sudo lvremove /dev/lab-vg2/lvtest2
Do you really want to remove active origin logical volume lab-vg2/lvtest2 with 1 snapshot(s)? [y/n]: y
Do you really want to remove and DISCARD logical volume lab-vg2/snap? [y/n]: y
  Logical volume "snap" successfully removed
Do you really want to remove and DISCARD logical volume lab-vg2/lvtest2? [y/n]: y
  Logical volume "lvtest2" successfully removed
```

Follow the explanations in the Ubuntu manual on lvmthin to create

a thin data Logical Volume called pool0 of 28 MB



a thin metadata Logical Volume called pool0meta of 4 MB
