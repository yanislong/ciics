#!/usr/bin/env python3

from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email .header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib, socks

def sendMail(taddr="lihl@casjc.com"):
    msg = MIMEMultipart()
    
    faddr = "lihailong@ciics.com"
    passwd = "uK7bcoYyDXtAgDxH"
    emtitle = "测试组"
    
    ttt = open('tt.png','rb').read()
    image = MIMEImage(ttt)
    image.add_header("Content-ID",'imageid')
    msg.attach(image)
    
    #msg = MIMEText("<html><body><h1>测试结果</h1><p><img src='cid:imageid'></p><a href='http://10.9.19.179' target='_blank'>查看结果</a></body></html>",'plain',"utf-8")
    body = """<html><body><h1>测试结果</h1><p><img src='cid:imageid' /></p><a href='http://10.9.19.179' target='_blank'>查看结果</a></body></html>"""
    ssg = MIMEText(body,'html',"utf-8")
    msg.attach(ssg)
    
    msg['Subject'] = '线上系统紧急bug'
    msg['From'] = '<' + emtitle + '>'
    msg['To'] = '<' + taddr + '>'
    
    server = smtplib.SMTP("smtp.exmail.qq.com", 25)
    #server.ehlo()
    #server.starttls()
    server.set_debuglevel(1)
    server.login(faddr, passwd)
    server.sendmail(faddr, i, msg.as_string())
    server.quit()

    taddr = ["lihl@casjc.com","xul@ciics.com"]

if __name__ == "__main__":
    sendMail()
