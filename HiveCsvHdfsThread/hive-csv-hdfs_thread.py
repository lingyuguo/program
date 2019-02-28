#!/usr/bin/python
#!-*-coding=utf-8-*-
import csv
import threading
from pyhive import hive
from pyhdfs import HdfsClient
from PoolTask import Pool,Task   #多线程
from TCLIService.ttypes import TOperationState


tablename = "test" #数据表
HIVE_IP = "****"
HDFS_IP = "***"
local_csv_dir = "****"
pool_size = 5


#csv格式
def hive_to_csv(row):
        start = time.time()
        file = open("%s%s%s.csv"%(local_csv_dir,tablename,row), "w")  
        #headers = ["time","value1","value2","value3"]
        #f_csv = csv.DictWriter(file, headers)  #标题行
	#f_csv.writeheader()
	
	writer = csv.writer(file)
        row_wri = rows[row*100000:(row+1)*100000]
        writer.writerows(row_wri)
        file.close()
        end = time.time()
        print "%s%s%s.csv write time %0.2f s\n"%(local_csv_dir,tablename,row,end-start)

#hive查询
def pyhive_query():
	sql = 'select * from default.%s'%tablename
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
		print "%s table count %d row"%(tablename,len(rows))
		return rows
	# 关闭hive连接
    	cursor.close()
    	#hiveConn.close()

#导入到HDFS
def csv_to_hdfs(row):
        client = HdfsClient(hosts=HDFS_IP)
        client.copy_from_local("%s%s%s.csv"%(local_csv_dir,tablename,row), '/hivecsv-%s%s'%(tablename,row))  #本地文件绝对路径,HDFS目录必须不存在


#多线程
def main():
        csv_start = time.time()
        pool = Pool(size=pool_size)
        pool.add_tasks([(hive_to_csv, (row,)) for row in range(len(rows)/100000+1)])
        pool.run()
        csv_end = time.time()
        print "csv write all spend %0.2f s"%(csv_end-csv_start)

if __name__ == "__main__":

        print("查询数据开始")
        query_start = time.time()
        rows = pyhive_query()
        query_end = time.time()
        print "hive query time %0.2f s"%(query_end-query_start)
        main()
        print("查询数据结束")
		
