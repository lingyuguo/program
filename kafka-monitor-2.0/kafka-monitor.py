#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
import json
from influxdb import InfluxDBClient

def _send_to_influxd(consumer_group_name,datatime,topic_name,partition_num,current_offset,log_end_offset,log):
	insert_sql = [{
                                "measurement":consumer_group_name,
                                "tags":{"topic":topic_name},
                                "fields":{"partition":partition_num,"current_offset":current_offset,"log_end_offset":log_end_offset,"log":log},
                                "time":datatime}]
	client.write_points(insert_sql)
def _kafka_select(kafka_ip,consumer_group_name,topic_name):
        lines = os.popen(" /kafka_2.11-1.0.1/bin/kafka-consumer-groups.sh --bootstrap-server "+kafka_ip+" --group "+consumer_group_name+" --describe|awk 'NR>2'")
        lines = lines.readlines()
	partition_num = 0
	current_offset = 0
	log_end_offset = 0
	log = 0	
        for line in lines:
                line = line.split()
                datatime = int(int(time.time()) * 10 ** 9)
		if line[0] == topic_name:
			partition_num += 1
                	current_offset += int(line[2])
                	log_end_offset += int(line[3])
               		log += int(line[4])
	print datatime,topic_name,partition_num,current_offset,log_end_offset,log
	_send_to_influxd(consumer_group_name,datatime,topic_name,partition_num,current_offset,log_end_offset,log)

if __name__ == '__main__':
	while True:
                env_dist = os.environ
                client = InfluxDBClient(env_dist.get('HOST'),env_dist.get('PORT'),env_dist.get('USERNAME'),env_dist.get('PASSWORD'),env_dist.get('DBNAME'))
				#client = InfluxDBClient("IP",port,"user","password","opentsdb")
                kafka_ip = env_dist.get('KAFKA_IP')
                #kafka_ip = "test"
                consumer_group_name = env_dist.get('CONSUMER_GROUP_NAME')
                #consumer_group_name = 'test'
				topic_name = env_dist.get('TOPIC_NAME')
                #topic_name = 'test'

                _kafka_select(kafka_ip,consumer_group_name,topic_name)
		time.sleep(60)
