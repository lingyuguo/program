#!/usr/bin/python
#!-*-coding=utf-8-*-
import csv
import threading
from pyhive import hive
from pyhdfs import HdfsClient
from PoolTask import Pool,Task   #多线程
from TCLIService.ttypes import TOperationState


table_name = ["battery_pack","test"] #数据表
HIVE_IP = "192.168.132.3"
HDFS_IP = "192.168.132.9:50070"
local_csv_dir = "/home/guolingyu"

#csv格式
def hive_to_csv(tablename):
	file = open("%s.csv"%tablename, "w")
        
	#headers = ["time","value1","value2","value3"]
        #f_csv = csv.DictWriter(file, headers)  #标题行
	#f_csv.writeheader()

	row = pyhive_query(tablename)
	file = open("%s.csv"%tablename, "w") 
	writer = csv.writer(file)
	writer.writerows(row)
	file.close()
	print "%s导出成功!数据%d行"%(tablename,len(row))
#hive查询
def pyhive_query(tablename):
	sql = 'select * from default.%s limit 4'%tablename
	cursor = hive.connect(HIVE_IP).cursor()
	cursor.execute(sql, async=True)
	#得到语句查询状态
	status = cursor.poll().operationState
	while status in (TOperationState.INITIALIZED_STATE, TOperationState.RUNNING_STATE):
    		status = cursor.poll().operationState
    		# If needed, an asynchronous query can be cancelled at any time with:
    		# cursor.cancel()
	# 获取数据
	try:
    		rows = cursor.fetchall()
	except:
    	        rows = ('null')
		return rows
	else:
		return rows
	# 关闭hive连接
    	cursor.close()
    	#hiveConn.close()

#导入到HDFS
def csv_to_hdfs(tablename):
	client = HdfsClient(hosts=HDFS_IP)
	client.copy_from_local('%s/%s.csv'%(local_csv_dir,tablename), '/hivecsv-%s'%tablename) #本地文件绝对路径,HDFS目录必须不存在


#多线程
def exe(tablename):
	rLock = threading.RLock()
	rLock.acquire()
	table_name.remove(tablename)
	rLock.release()
	hive_to_csv(tablename)
	#csv_to_hdfs(tablename)
		
def main():
	pool = Pool(size=5)
	pool.add_tasks([(exe, (tablename,)) for tablename in table_name])
	pool.run()	

if __name__ == "__main__":
	while len(table_name) != 0:
		print("查询数据开始")
		main()
		print("查询数据结束")
