# -*- coding: utf-8 -*-
__author__ = 'liuxuexue'

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import time

class SendEmail():

    def __init__(self, report_path):
        self.report_path = report_path

    def new_report_path(self):
        lists = os.listdir(self.report_path)
        lists.sort(key=lambda fn:os.path.getmtime(self.report_path+'\\'+fn))
        new_report_path = os.path.join(self.report_path, lists[-1])
        return new_report_path

    #发送邮件
    def send_email(self):
        f = open(self.new_report_path(), 'rb')
        mail_body = f.read()
        f.close()
        # 发送邮箱服务器
        smtpserver = 'smtp.qiye.aliyun.com'
        # 发送邮箱用户名/密码
        user = 'liuxuexue@swifthealth.cn'
        password = 'Liuxue123'
        # 发送邮箱
        sender = 'liuxuexue@swifthealth.cn'
        # 多个接收邮箱，单个收件人的话，直接是receiver='XXX@126.com'
        receiver = ['liuxuexue@swifthealth.cn', 'chenyi@swifthealth.cn']
        # receiver = 'liuxuexue@swifthealth.cn'
        # 发送邮件主题
        subject = '患者端自动化测试报告'
        # 编写 HTML类型的邮件正文
        # MIMEText这个效果和下方用MIMEMultipart效果是一致的，已通过。
        #    msg = MIMEText(mail_body,'html','utf-8')

        msg = MIMEMultipart('mixed')

        # 注意：由于msg_html在msg_plain后面，所以msg_html以附件的形式出现
        #    text = "Dear all!\nThe attachment is new testreport.\nPlease check it."
        # 中文测试ok
        #    text = "Dear all!\n附件是最新的测试报告。\n麻烦下载下来看，用火狐浏览器打开查看。\n请知悉，谢谢。"
        #    msg_plain = MIMEText(text,'plain', 'utf-8')
        #    msg.attach(msg_plain)

        # msg_html1 = MIMEText(mail_body, 'html', 'utf-8')
        # msg.attach(msg_html1)

        msg_html = MIMEText(mail_body, 'html', 'utf-8')
        msg_html["Content-Disposition"] = 'attachment; filename="TestReport.html"'
        msg.attach(msg_html)

        # 以附件的方式发送：但是会报554，倍163退信。--此路不通。
        #    msg_html = MIMEText(mail_body,'base64','utf-8')
        #    msg_html["Content-Type"] = 'application/octet-stream'
        #    msg_html.add_header('Content-Disposition', 'attachment', filename='testreport.html')
        #    msg.attach(msg_html)

        # 要加上msg['From']这句话，否则会报554的错误。
        # 要在163有限设置授权码（即客户端的密码），否则会报535
        msg['From'] = sender
        #    msg['To'] = 'XXX@doov.com.cn'
        # 多个收件人
        msg['To'] = ';'.join(receiver)
        msg['Subject'] = Header(subject, 'utf-8')

        # 连接发送邮件
        smtp = smtplib.SMTP()
        smtp.connect(smtpserver, 25)
        smtp.login(user, password)
        smtp.sendmail(sender, receiver, msg.as_string())
        smtp.quit()