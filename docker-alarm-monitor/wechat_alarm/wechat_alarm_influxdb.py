#! /usr/bin/env python
#-*-coding:utf-8-*-

import os
import json
import requests
import datetime,time
import mysql.connector

env_dist = os.environ
#token
def get_token():
        url='https://qyapi.weixin.qq.com/cgi-bin/gettoken'
	values = {'corpid' : env_dist.get("CORPID") ,
                  'corpsecret': env_dist.get("CORPSECRET")}
        req = requests.post(url, params=values)
        data = json.loads(req.text)
        return data["access_token"]

#sed_wechat
def send_msg(alertTime,alertName,host,level,message):
	wechat_msg = "警告时间:"+str(alertTime)+",AlterName:"+str(alertName)+",主机名称:"+str(host)+",level:"+str(level)+",message:"+str(message)
        url="https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token="+get_token()
        values = """{"touser" : "@ll" ,
                "toparty":"%s",
                "msgtype":"text",
                "agentid":"%s",
                "text":{"content":"%s"},
               "safe":"0"
               }""" %(env_dist.get("TOPARTY"),env_dist.get("AGENTID"),str(wechat_msg))
        data = json.loads(values)
        req = requests.post(url, values)

#查数据#
def influxdb_select():
  while True:
    start_time = int((int(time.time()) - 6000 * 10000) * 10 ** 9)
    stop_time = int(int(time.time()) * 10 ** 9)
    select_time = "time >= %s and time < %s" % (start_time, stop_time)
    influxd_url = 'http://%s:8086/query?db=chronograf&q=SELECT *  FROM "chronograf"."autogen"."alerts" where %s'%(env_dist.get("DB_HOST"),select_time)
    print influxd_url
    influxd_content = requests.get(influxd_url)
    url_content= influxd_content.content  
    url_json = json.loads(url_content)
    results = url_json["results"]
    if results[0].has_key("series"):
        series = results[0]["series"]
	print series
        for values in series[0]["values"]:
  	    alertTime = values[0]
            alertName = values[2]
            host = values[4]
            level = values [5]
            message = values [6]
            send_msg(alertTime,alertName,host,level,message)
	time.sleep(60)
    else:
        print("无数据")
        time.sleep(60)
        continue

if __name__ == '__main__':
        influxdb_select()
