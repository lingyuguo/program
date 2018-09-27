#!/usr/bin/python
import os
import re
#####disk############################
precision=0
def phy_size():
  with open('/proc/partitions','r') as dp:
    res = {}
    for disk in dp.readlines():
      if re.search(r'[s,h,v]d[a-z]\n',disk):
        blknum = disk.strip().split(' ')[-2]
        dev = disk.strip().split(' ')[-1]
        size = int(blknum)*1024
	total = '%.*fGB'%(precision,(round(float(size) / 10**9)))
        res[dev]=total
    return res
#####base monitor###########
host   = os.popen("cat /etc/hostname").read()
memory = os.popen("free -h|awk 'NR==2{print $2}'").read()
cpu    = os.popen('cat /proc/cpuinfo |grep "processor"| wc -l').read()
mount  = os.popen("lsblk |grep /disk|awk '{print $1,$7}'").read().rstrip("\n").split("\n")
##########end##############
print host,cpu,memory,phy_size()
print mount
print "-"*40 
