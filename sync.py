#pip install psutil --index-url https://artifactory-iva.si.francetelecom.fr/artifactory/api/pypi/pythonproxy/simple

from dirsync import sync
import os
import psutil
import platform

source = ""
target = ""

label_name = 'BACKUPWORK'

source_win_dir = 'C:/_workdev'
source_lin_dir = '/home/opob7414/_dev'

target_win_dir = 'backup_workdev_eburo'
target_lin_dir = 'backup_workdev_linux'

nb_disks = len(psutil.disk_partitions())

if platform.uname().system=="Windows":  
    import win32api
    print("C'est Windows")
    source = source_win_dir
    target_dir = target_win_dir
    print(str(nb_disks) + " lecteurs")
    print("source : "+source)
    for i in range(0, nb_disks):
        target_drive = psutil.disk_partitions()[i].device
        print(str(psutil.disk_partitions()[i]))
        target_label = win32api.GetVolumeInformation(psutil.disk_partitions()[i].device)[0]
        print(str(target_label))
        if target_label==label_name:
            target = target_drive
            print("")
            #if "\\" in target:
            #    target = target.replace('\\', '/')
            print(target + " sur " + target_drive)
        else:
            target = "not available"
else:
    print("C'est Linux")
    source = source_lin_dir
    target_dir = target_lin_dir
    partitions = psutil.disk_partitions()
    print(str(nb_disks) + " partitions")
    print("source : "+source)
    for i in range(0, nb_disks):
        partition = psutil.disk_partitions()[i].device
        mount_point = psutil.disk_partitions()[i].mountpoint
        print(str(mount_point))
        if label_name in mount_point:
            target = mount_point + "/"
            print("")
            print(target + " sur " + partition)
        else:
            target = "not available"

print(target)
target_root = target
target = target + target_dir

if "not available" in target:
    print("target not available")
else:
    if os.path.exists(source):
        if os.path.exists(target_root):
            print("sync " + source + " to " + target)
            sync(source, target, 'sync', create = True, ctime = True, verbose = True) 
        else:
            print("Error : target directory '"+target_root+"' doesn't exist")
    else:
        print("Error : source directory '"+source+"' doesn't exist")
    
    