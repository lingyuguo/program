#!/usr/bin/python
import smtplib
import string 
HOST = "smtp.163.com"
SUBJECT = "Test emaile from python" 
TO = "**@qq.com"
FROM = "**@163.com"
text = "Python rules them all !"
BODY = string.join ((
		"FROM : %s"%FROM,
		"TO : %s"%TO,
		"Subject : %s"%SUBJECT,
		"",
		text
		),"\r\n")
server = smtplib.SMTP()
server.connect (HOST,"25")
server.starttls()
server.login("***@163.com","******") 
server.sendmail(FROM,[TO],BODY)
server.quit() 
