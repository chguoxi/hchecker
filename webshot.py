#!python
# -*- coding: UTF-8 -*-
import time
import string
from selenium import webdriver

#sites = [{'name':'www','url':'http://www.simuwang.com'},{'name':'pt','url':'http://pt.simuwang.com'},{'name':'news','url':'http://news.simuwang.com'},{'name':'dc','url':'http://dc.simuwang.com'},{'name':'mall','url':'http://mall.simuwang.com'},{'name':'m','url':'http://m.simuwang.com'},{'name':'mobile','url':'http://mobile.simuwang.com'}]
sites = [{'name':'www','url':'http://www.simuwang.com'}]
idfile = "./logs/id"
logifle = "./logs/check-logs.txt"
imagepath = "./images/"
with open(idfile,"r") as f:
    id = f.read()
    if(id==''):
        id = 1
    else:
        id = int(id)+1
    id = str(id)
    
    f.close()
    f = open(idfile,"w")
    f.write(id)
    f.close()
    
browser = webdriver.Firefox()

log = "//-----------------------------------------------------------\r\n"
for site in sites:
    #browser.set_window_size(1024, 800)
    browser.get(site['url'])
    time.sleep(2)
    browser.save_screenshot(imagepath + site['name']+"_"+id+".png")
    logtext = "第"+id+"次检查"+site['name']+"站点完成\r\n";
    print(logtext)
    log += logtext;
browser.quit()
log += "//-----------------------------------------------------------\r\n"

# 日志
with open(logifle,"a") as f:
    f.write(log)
    f.close()

# 邮件
#coding: utf-8
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

HOST = "smtp.qq.com"
SUBJECT = u"官网业务服务质量周报"
TO = "goss@lunluoren.com"
FROM = "995306681@qq.com"

def addimg(src,imgid):
    fp = open(src, 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()
    msgImage.add_header('Content-ID', imgid)
    return msgImage
def smail(title,content,file):
    msg = MIMEMultipart('related')
    msgtext = MIMEText("<font color=red>私募排排网网站截图:<br><img src=\"cid:weekly\" border=\"1\"><br>详细内容见附件。</font>","html","utf-8")
    msg.attach(msgtext)
    msg.attach(addimg(file,"weekly"))
    #attach = MIMEText(open("doc/week_report.xlsx", "rb").read(), "base64", "utf-8")
    #attach["Content-Type"] = "application/octet-stream"
    #attach["Content-Disposition"] = "attachment; filename=\"业务服务质量周报(12周).xlsx\"".decode("utf-8").encode("gb18030")
    #msg.attach(attach)
    msg['Subject'] = SUBJECT
    msg['From']=FROM
    msg['To']=TO
    try:
        server = smtplib.SMTP()
        server.connect(HOST,"25")
        server.starttls()
        server.login("995306681@qq.com","chenguoxi33681")
        server.sendmail(FROM, TO, msg.as_string())
        server.quit()
        print("邮件发送成功！")
    except Exception(e):  
        print("失败："+str(e)) 







