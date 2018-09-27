#!/usr/bin/env python
# coding:utf-8
import requests
import json
import mysql.connector
import time
#数据库
db = mysql.connector.connect(host="192.168.206.140",db="influxd_mysql",user="root",password="guolingyu",port=3306,charset='utf8')
#创建表
#create table hearbeat(alarm int(10),time Datetime);
#create table  alters(time Datetime,alertID char(100),alertName char(100),duration char(100),host char(100),level char(100),message char(100),value float(5,3));
def insert_values_mysql():
  while True:
    start_time = int((int(time.time()) - 60 * 1000) * 10 ** 9)
    stop_time = int(int(time.time()) * 10 ** 9)
    select_time = "time > %s and time < %s" % (start_time, stop_time)
    influxd_url = 'http://192.168.206.140:8086/query?db=chronograf&q=SELECT *  FROM "chronograf"."autogen"."alerts" where %s'%select_time
    influxd_content = requests.get(influxd_url)
    url_content= influxd_content.content  
    url_json = json.loads(url_content)
    results = url_json["results"]
    if results[0] =="series":
        series = results[0]["series"]
        columns = series[0]["columns"]
        for values in series[0]["values"]:
            now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            alertID  = values[1]
            alertName=values[2]
            duration =values[3]
            host     = values[4]
            level    = values [5]
            message  = values [6]
            value    = values[8]
            #sql='INSERT INTO alters (alertName,duration,host)VALUES ("%s","%s","%s")'%(alertName,duration,host)
            sql1 = 'INSERT INTO alters VALUES ("%s","%s","%s","%s","%s","%s","%s","%s")' \
                  %(now,alertID,alertName,duration,host,level,message,value)
	    sql2 = 'INSERT INTO hearbeat VALUES(1,"%s")'%now
            try:
                cursor = db.cursor()
                cursor.execute(sql1)
		cursor.execure(sql2)
                db.commit()
            except:
                # Rollback in case there is any error
                print ('插入数据失败!')
                db.rollbacki()
	time.sleep(60)
    else:
        print("无数据")
	now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	sql = 'INSERT INTO hearbeat VALUES(0,"%s")'%now
	try:
                cursor = db.cursor()
                cursor.execute(sql)
                db.commit()
        except:
                # Rollback in case there is any error
                print ('插入数据失败!')
                db.rollback()
        time.sleep(60)
        continue
if __name__ == '__main__':
    insert_values_mysql()
