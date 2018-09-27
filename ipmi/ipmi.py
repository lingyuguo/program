#!/usr/bin/python
import os
from influxdb import InfluxDBClient
##############global##################
IPMI_IP = ["192.168.255.254"]
IPMI_USER = "ADMIN"
IPMI_PASSWD = "11111111"
client = InfluxDBClient("192.168.206.142","8086","root","","opentsdb")
#client = InfluxDBClient(env_dist.get('HOST'),env_dist.get('PORT'),env_dist.get('USERNAME'),env_dist.get('PASSWORD'),env_dist.get('DBNAME'))
##############value_number###########
def judge_value():
	if  items[1] in ["on","active","always-on","true"]:
		return 1
	else:
		return 2
##############collect#################
#os.popen("ipmitool -H %s -U %s -P %s -I lan chassis status > impi.txt"%(IPMI_IP,IPMI_USER,IPMI_PASSWD)).read()
collect_chassis = open("ipmi.txt")
collect_line = collect_chassis.readlines()
for line in collect_line:
        items=line.rstrip().split(": ")
	try:
		values=judge_value()
		print values
		insert_sql = [{
                                "measurement":"mon_item",
                                "tags":{"status":items[0]},
                                "fields":{"value":values}}]
		client.write_points(insert_sql)
		print insert_sql
	except IndexError:
                insert_sql = [{
                                "measurement":"mon_item",
                                "tags":{"status":items[0]},
                                "fields":{"value":2}}]
                client.write_points(insert_sql)
                print insert_sql
collect_chassis.close()	
