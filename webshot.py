#!python
# -*- coding: UTF-8 -*-
import time
import string
from selenium import webdriver
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

#sites = [{'name':'www','url':'http://www.simuwang.com'},{'name':'pt','url':'http://pt.simuwang.com'},{'name':'news','url':'http://news.simuwang.com'},{'name':'dc','url':'http://dc.simuwang.com'},{'name':'mall','url':'http://mall.simuwang.com'},{'name':'m','url':'http://m.simuwang.com'},{'name':'mobile','url':'http://mobile.simuwang.com'}]
sites = [{'name':'www','url':'http://www.simuwang.com'}]
idfile = "./logs/id"
logifle = "./logs/check-logs.txt"
imagepath = "./images/"
filelist = []
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
    imgname = imagepath + site['name']+"_"+id+".png"
    browser.get(site['url'])
    time.sleep(2)
    browser.save_screenshot(imgname)
    filelist.append(imgname)
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
def addimg(src,imgid):
    fp = open(src, 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()
    msgImage.add_header('Content-ID', imgid)
    return msgImage
def smail(title,files):
    HOST = "smtp.126.com"
    TO = "goss@lunluoren.com"
    FROM = "cgx2625526@126.com"
    imgcontent = ''
    fno = 1
    msg = MIMEMultipart('related')
    
   
    for file in files:
        msg.attach(addimg(file,"file_"+str(fno)))
        fno +=1
        imgcontent += "<img src=\"cid:"+"file_"+str(fno)+"\" border=\"1\"><br />"
    msgtext = MIMEText("<font color=red>私募排排网网站截图:<br>"+imgcontent+"详细内容见附件。</font>","html","utf-8")
    msg.attach(msgtext)
    #attach = MIMEText(open("doc/week_report.xlsx", "rb").read(), "base64", "utf-8")
    #attach["Content-Type"] = "application/octet-stream"
    #attach["Content-Disposition"] = "attachment; filename=\"业务服务质量周报(12周).xlsx\"".decode("utf-8").encode("gb18030")
    #msg.attach(attach)

    msg['Subject'] = title
    msg['From']=FROM
    msg['To']=TO
    try:
        server = smtplib.SMTP()
        server.set_debuglevel(1)
        server.connect(HOST,"25")
        #server.docmd("EHLO server")
        #server.starttls()
        server.login("cgx2625526","chguoxi33651")
        server.sendmail(FROM, TO, msg.as_string())
        server.quit()
        print("邮件发送成功！")
    except Exception as e:  
        print("失败："+str(e))
smail("私募排排网站点截图",filelist)







