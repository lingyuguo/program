#!/usr/bin/python
import xlsxwriter
import os
import re
##########excel#############
workbook  = xlsxwriter.Workbook('env.xlsx')
worksheet_env = workbook.add_worksheet("ENV")
worksheet_Threshold = workbook.add_worksheet("Threshold")
##########excel.write#################
worksheet_env.write('A1',"host")
worksheet_env.write('B1',"system.cpu")
worksheet_env.write('C1',"system.ram")
worksheet_Threshold.write('A1',"host")
worksheet_Threshold.write('A2',"warning")
worksheet_Threshold.write('A3',"unusual")
worksheet_Threshold.write('B1',"system.cpu")
worksheet_Threshold.write('C1',"system.ram")
worksheet_Threshold.write('B2',90)
worksheet_Threshold.write('B3',100)
worksheet_Threshold.write('C2',80)
worksheet_Threshold.write('C3',90)
##########excle.write.variable#######
count = os.popen("cat env.txt|grep success|wc -l").read()
env= os.popen('cat env.txt').read().split('----------------------------------------\n')
disk_number = 0
for number in range(int(count)):
	line = number+2
	machine = env[number].strip('\n').split('\n')
	host = machine[1]
	cpu  = machine[2]
	mem  = machine[3].strip('G')
	worksheet_env.write('A%s'%line,host)
	worksheet_env.write('B%s'%line,int(cpu))
	worksheet_env.write('C%s'%line,int(mem))
#######################disk#########################################
	dick_size={}
	disk_mount={}
	mount_size={}
        for  disk in machine[4].lstrip('{').rstrip('}').split(', '):
                pattern = re.compile(r'\d+')
                size = pattern.findall(disk)
                dick_size[disk[1:4]]="".join(size)
        for  disk in machine[5].lstrip("[").rstrip("]").split(', '):
                pattern = re.compile(r'disk\d+')
                result = pattern.findall(disk)
                disk_mount[disk[3:6]]="".join(result)
        for disk_k, disk_v in dick_size.items():
	        mount_k=disk_mount.get(disk_k,"")
		mount_size[mount_k]=disk_v
	if len(mount_size) > disk_number:
		disk_number=len(mount_size)
	for i in range(disk_number):
		end=mount_size.keys()
		title_key=end[i]
		if title_key != "":
			title_number=int(end[i].lstrip("disk"))
			worksheet_env.write(0,title_number+3,"disk_space._%s"%title_key)
			worksheet_env.write(number+1,title_number+3,int(mount_size[title_key]))
			worksheet_Threshold.write(0,title_number+3,"disk_space._%s"%title_key)	
			worksheet_Threshold.write(1,title_number+3,60)	
			worksheet_Threshold.write(2,title_number+3,80)	
		elif title_key == "":
			worksheet_env.write(0,3,"disk_space._%s"%title_key)	
			worksheet_env.write(number+1,3,int(mount_size[title_key]))
			worksheet_Threshold.write(0,3,"disk_space._%s"%title_key)	
			worksheet_Threshold.write(1,3,70)
			worksheet_Threshold.write(2,3,80)
workbook.close()
