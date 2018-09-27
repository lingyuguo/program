#! /usr/bin/env python
#-*-coding:utf-8-*-

import json
import requests
import datetime,time
import mysql.connector

#token
def get_token():
        url='https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        values = {'corpid' : 'wx4c879f1cbd778cc7' ,
                  'corpsecret':'y8qAg29VO39ENWbY2zdjogioDouydHJlE_QGh3uiS54'}
        req = requests.post(url, params=values)
        data = json.loads(req.text)
        return data["access_token"]

#sed_wechat
def send_msg(alter_time,alterName,host,level,message):
	wechat_msg = "警告时间:"+alter_time+",AlterName:"+alterName+",主机名称:"+host+",level:"+level+",message:"+message
        url="https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token="+get_token()
        values = """{"touser" : "@ll" ,
                "toparty":"6",
                "msgtype":"text",
                "agentid":"1000002",
                "text":{"content":"%s"},
               "safe":"0"
               }""" %(str(wechat_msg))
        data = json.loads(values)
        req = requests.post(url, values)

#查数据#
def mysql_select():
    while True:
        db = mysql.connector.connect(host="192.168.206.140", db="influxd_mysql", user="root", password="guolingyu",
                                     port=3306, charset='utf8')
        start_time = (datetime.datetime.now() - datetime.timedelta(minutes=1)).strftime("%Y-%m-%d %H:%M:%S")
        end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        cursor = db.cursor()
        query = "SELECT * FROM alters where time >='%s' and time <'%s';" % (start_time, end_time)
        cursor.execute(query)
        results = cursor.fetchall()
	print query
	print results
        if results != []:
            for result_one in results:
                	alter_time = str(result_one[0])
                	alterName =  str(result_one[2])
                	host =  str(result_one[4])
                	level = str(result_one[5])
                	message = str(result_one[6])
			print alter_time,alterName,host,level,message
                	send_msg(alter_time,alterName,host,level,message)
            time.sleep(60)
            continue
        else:
            print("无数据")
            time.sleep(60)
            continue

if __name__ == '__main__':
        mysql_select()
