#!/usr/bin/python
import smtplib
import string 
HOST = "smtp.163.com"
SUBJECT = "Test emaile from python" 
TO = "986702758@qq.com"
FROM = "lingyuguo6240@163.com"
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
server.login("lingyuguo6240@163.com","******") 
server.sendmail(FROM,[TO],BODY)
server.quit() 
