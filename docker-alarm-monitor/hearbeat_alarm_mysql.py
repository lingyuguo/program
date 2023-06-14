#!/usr/bin/env python
# coding:utf-8
import smtplib
from email.mime.text import MIMEText
import mysql.connector
import datetime,time

#邮箱#
HOST = "smtp.163.com"  # 163邮箱
SUBJECT = "sdfas"
TO = "lasdfa0@163.com"
FROM = "fsadfa@163.com"

#发送邮件#
def sendmail(end_time):
    msg = MIMEText("""
        <table width="800" border="0" cellspacing="0" cellpadding="4"> 
            <tr> 
                <td bgcolor="#CECFAD" height="20" style="font-size:14px">报警脚本出错</td> 
            </tr> 
            <tr> 
                <td bgcolor="#EFEBDE" height="100" style="font-size:13px"> 
                警告时间:%s<br> 
                执行脚本可能出现错误，请排查<br>
                </td> 
            </tr> 
        </table>"""%end_time,"html","utf-8")
    msg['Subject'] = SUBJECT
    msg['From'] = FROM
    msg['To'] = TO
    try:
        server = smtplib.SMTP()
        server.connect(HOST, "25")
        server.starttls()
        server.login("lingyuguo6240@163.com", "042621gen")
        server.sendmail(FROM, TO, msg.as_string())
        server.quit()
        print("send yes!")
    except:
        print("send file")

#查数据#
def mysql_select():
    while True:
        db = mysql.connector.connect(host="192.168.206.140", db="influxd_mysql", user="root", password="adfa,
                                     port=3306, charset='utf8')
        start_time = (datetime.datetime.now() - datetime.timedelta(minutes=1)).strftime("%Y-%m-%d %H:%M:%S")
        end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        cursor = db.cursor()
        query = "SELECT * FROM hearbeat where time >'%s' and time <'%s';" % (start_time, end_time)
        cursor.execute(query)
        results = cursor.fetchall()
        if results == []:
            sendmail(end_time)
            time.sleep(60)
            continue
        else:
            print("正常运行")
            time.sleep(60)
            continue

if __name__ == '__main__':
    mysql_select()
