#!/usr/bin/python
import time
import re
import os
from influxdb import InfluxDBClient
##############global##################
table_judge = {"netdata.system.cpu.user":(80.0,90.0),"netdata.system.ram.used":(80.0,100.0),"netdata.disk_space._.used":(80.0,90.0),"netdata.disk_space._disk1.used":(70.0,80.0),"netdata.disk_space._disk2.used":(70.0,80.0),"netdata.disk_space._disk3.used":(70.0,80.0),"netdata.disk_space._disk4.used":(70.0,80.0),"netdata.disk_space._disk5.used":(70.0,80.0),"netdata.disk_space._disk6.used":(70.0,80.0),"netdata.disk_space._disk7.used":(70.0,80.0),"netdata.disk_space._disk8.used":(70.0,80.0),"netdata.disk_space._disk9.used":(70.0,80.0),"netdata.disk_space._disk10.used":(70.0,80.0),"netdata.disk_space._disk11.used":(70.0,80.0),"netdata.disk_space._disk12.used":(70.0,80.0)}
##############write_def##############
def write_def():
	end_list=every_table.values()
	normal = 0
	warning = 0
	unusual = 0
	for number in end_list:
		if number == 0:
			normal+=1
		elif number == 1:
			warning+=1
		elif number == 2:
			unusual+=1
	end_table={"normal":normal,"warning":warning,"unusual":unusual}
	for table,len_table in end_table.items():
                insert_sql = [{
                                "measurement":table,
                                "tags":{"status":table},
                                "fields":{"value":len_table*1.0},
                                "time":stop_time}]
                client.write_points(insert_sql)
		print(insert_sql)
##############every_value_host#######
def every_value_host(value_normal,value_unusual,value_list,host_list):
	for number in range(len(value_list)):
		value = float(value_list[number].lstrip("value':"))
		host = host_list[number].lstrip("host':")
		status = compare_value(value,value_normal,value_unusual)
		if every_table.get(host) is not None:
			if every_table.get(host) < status:
				every_table[host]=status
		else:
			every_table[host]=status
##############compare_value###############
def compare_value(value,value_normal,value_unusual):
	if  value < value_normal:
		return 0
	elif value > value_normal and value < value_unusual:
		return 1
	elif value > value_unusual:
		return 2
###############judge_table###########
def judge_table(table,value_list,host_list):
	value_normal,value_unusual = table_judge.get(table)
	every_value_host(value_normal,value_unusual,value_list,host_list)
#############judge_result#######
def judge_result(result,talbe):
	value_rule=re.compile(r'value\'\:\ \d*\.\d*')
	host_rule=re.compile(r'host\'\:\ u\'\w*')
	value_list=value_rule.findall(result)
	host_list=host_rule.findall(result)
	judge_table(table,value_list,host_list)
############main#################
if __name__ == '__main__':
    ##########initialize_influxdb########
    env_dist = os.environ
    #client = InfluxDBClient("192.168.206.131",8086,"root","","opentsdb")
    client = InfluxDBClient(env_dist.get('HOST'),env_dist.get('PORT'),env_dist.get('USERNAME'),env_dist.get('PASSWORD'),env_dist.get('DBNAME'))
    ##########select_table###############
    table_name  = {"netdata.system.cpu.user":'percentile("value", 95)',"netdata.system.ram.used":'last("value")/(256*1024)*100',"netdata.disk_space._.used":'last("value")/549*100',"netdata.disk_space._disk1.used":'last("value")/(22*1024)*100',"netdata.disk_space._disk2.used":'last("value")/(22*1024)*100',"netdata.disk_space._disk3.used":'last("value")/(22*1024)*100',"netdata.disk_space._disk4.used":'last("value")/(22*1024)*100',"netdata.disk_space._disk5.used":'last("value")/(22*1024)*100',"netdata.disk_space._disk6.used":'last("value")/(22*1024)*100',"netdata.disk_space._disk7.used":'last("value")/(22*1024)*100',"netdata.disk_space._disk8.used":'last("value")/(22*1024)*100',"netdata.disk_space._disk9.used":'last("value")/(22*1024)*100',"netdata.disk_space._disk10.used":'last("value")/(22*1024)*100',"netdata.disk_space._disk11.used":'last("value")/(22*1024)*100',"netdata.disk_space._disk12.used":'last("value")/(22*1024)*100'}
    every_table={}
    while True:
        ##########time#######################
        start_time = int((int(time.time()) - 60 * 1000) * 10 ** 9)
        stop_time = int(int(time.time()) * 10 ** 9)
        select_time = "time > %s and time < %s" % (start_time, stop_time)
	##########select####################
        for table,select in table_name.items():
            select_sql  = 'select  %s  as value from "%s" where %s group by host'%(select,table,select_time)
            result = str(client.query(select_sql))
            judge_result(result,table)
        write_def()
        time.sleep(60)
