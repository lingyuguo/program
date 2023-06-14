#!/usr/bin/env python
#coding:utf-8
import smtplib
from email.mime.text import MIMEText
import mysql.connector
import datetime,time

#邮箱#
HOST = "smtp.163.com"  # 163邮箱
SUBJECT = "asdf"
TO = "lingasd@163.com"
FROM = "lingyasfd6240@163.com"

#发送邮件#
def sendmail(alter_time,alterName,host,level,message):
    msg = MIMEText("""<table width="800" border="0" cellspacing="0" cellpadding="4"> 
            <tr> 
                <td bgcolor="#CECFAD" height="20" style="font-size:14px">CPU报警<a href="http://192.168.206.140:9092/kapacitor/v1/tasks/chronograf-v1-b5e67bb5-178e-403e-bfba-1367c8c5d465">more>></a></td> 
            </tr> 
            <tr> 
                <td bgcolor="#EFEBDE" height="100" style="font-size:13px"> 
                警告时间:%s<br> 
                AlterName:%s<br>  
                主机名称:%s<br> 
                level:%s<br> 
                message:%s<br>  
                </td> 
            </tr> 
        </table>"""%(alter_time,alterName,host,level,message),"html","utf-8")
    msg['Subject'] = SUBJECT
    msg['From'] = FROM
    msg['To'] = TO
    try:
        server = smtplib.SMTP()
        server.connect(HOST, "25")
        server.starttls()
        server.login("lafdsd.com", "XXXXX")
        server.sendmail(FROM, TO, msg.as_string())
        server.quit()
        print("send yes!")
    except:
        print("send file")

#查数据#
def mysql_select():
    while True:
        db = mysql.connector.connect(host="192.168.206.140", db="influxd_mysql", user="root", password="ga",
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
                	sendmail(alter_time,alterName,host,level,message)
            time.sleep(60)
            continue
        else:
            print("无数据")
            time.sleep(60)
            continue

if __name__ == '__main__':
    mysql_select()
