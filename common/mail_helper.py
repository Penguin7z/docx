#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Name: mail_helper.py
# Purpose: PyCharm
#
# Author: 企鹅(simon.dong)
#
# Created: 2017/7/25 下午7:58

# coding: utf-8

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import email.utils
from bson.objectid import ObjectId
import datetime
import time
import pytz

from common import pf

localtz = pytz.timezone('Asia/Shanghai')

smtpserver = 'smtp.exmail.qq.com'
username = 'admin@wehome.net.cn'
password = 'T@F7dSDFeCD3'


def send_mail(to_address, text, mail_id):
    from_address = username
    to_address = to_address
    cc_address = 'simon@dobechina.com'

    href_str = "https://www.wehome.net.cn/mailactive?mid=" + str(
        mail_id) + "&mail=" + to_address + "&from=" + "mail" + "&sourceType=" + "BindMail"

    htmlString = '''<html><head><base target="_blank">
    	<style type="text/css">
    	::-webkit-scrollbar{ display: none; }
    	</style>
    	<style id="cloudAttachStyle" type="text/css">
    	#divNeteaseBigAttach, #divNeteaseBigAttach_bak{display:none;}
    	</style>
    	</head>
    	<body>尊敬的先生/女士：（<a href="mailto:''' + to_address + '''">用户''' + to_address + '''</a> ）<br>
    	<br>
    	您好！感谢您注册 wehome admin！<br>
    	<br>
    	请点击“激活”按钮立即激活并使用 PalmLawyer，享受各项优质服务。如不是您本人操作，请忽略此邮件。<br>
    	<div style="padding-left:200px;padding-top:5px;"><a target="_blank" style="color:#FFF;font-size:14px;padding:5px 10px;border-radius:3px; text-decoration: none; background:#1689ff;" href="''' + href_str + '''">&nbsp;&nbsp;激&nbsp;&nbsp;&nbsp;&nbsp;活&nbsp;&nbsp;</a></div><br>
    	<br>
    	如果以上按钮点击无效，请把下面网页地址复制到浏览器地址栏中打开：<br>
    	<a target="_blank" href="''' + href_str + '''"> ''' + href_str + ''' </a>(链接有效期为24小时)
    	<table width="100%"><tbody><tr><td align="center"><img src="" border="0" type="footlog"></td></tr></tbody></table>


    	<style type="text/css">
    	body{font-size:14px;font-family:arial,verdana,sans-serif;line-height:1.666;padding:15;margin:0;overflow:auto;white-space:normal;word-wrap:break-word;min-height:100px}
    	td, input, button, select, body{font-family:Helvetica, 'Microsoft Yahei', verdana}
    	pre {white-space:pre-wrap;white-space:-moz-pre-wrap;white-space:-pre-wrap;white-space:-o-pre-wrap;word-wrap:break-word;width:95%}
    	th,td{font-family:arial,verdana,sans-serif;line-height:1.666}
    	img{ border:0}
    	header,footer,section,aside,article,nav,hgroup,figure,figcaption{display:block}
    	</style>

    	<style id="ntes_link_color" type="text/css">a,td a{color:#064977}</style>
    	</body></html>'''

    if not (len(mail_id) == 24):
        return

    msg = MIMEText(htmlString, 'html', 'utf-8')
    msg['Subject'] = u'账号注册成功！请充值密码 ###ID' + str(pf.get_utc_millis())
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Cc'] = cc_address

    sm = smtplib.SMTP_SSL(smtpserver, port=465, timeout=20)
    # sm.set_debuglevel(1)
    # sm.ehlo()
    # sm.starttls()
    # sm.ehlo()
    sm.login(username, password)

    sm.sendmail(from_address, to_address, msg.as_string())

    sm.quit()


if __name__ == "__main__":
    send_mail("simon@dobechina.com", "hhh", str(ObjectId()))
