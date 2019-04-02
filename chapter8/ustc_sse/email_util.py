# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from chapter8.ustc_sse.config import *

sender = MAIL_USER

def send_email(receivers, news):
    message = MIMEText(news.get('content'), 'plain', 'utf-8')
    message['From'] = sender
    message['To'] = ';'.join(receivers)
    message['Subject'] = Header('[新通知]' + news.get('title'), 'utf-8')
    try:
        smtp_obj = smtplib.SMTP(MAIL_HOST, port=25)
        smtp_obj.login(MAIL_USER, MAIL_PASS)
        smtp_obj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print('邮件发送失败', e)
