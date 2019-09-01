#!/usr/bin/env python3
# coding: utf-8

from email.mime.text import MIMEText
import smtplib
import sqlite3
import re

conn = sqlite3.connect('mail.db')
c = conn.cursor()

#値を連続して表示
c.execute('select group_concat(email) from data')

value = c.fetchall()
print(value)
formatted = ""
for elem in value[0]:
    formatted += elem

print(formatted)

conn.close

to_email = formatted
from_email = "webiot_c@yahoo.co.jp"
from_passwd = "bakuhatsuIoT2019"

message = "TEST MAIL 応急救護の協力をお願いします<br>AEDの場所<br>緯度　経度"
subject = "test mail[複数送信]"

msg = MIMEText(message, "html")
msg["Subject"] = subject
msg["To"] = to_email
msg["From"] = from_email

yahoo = smtplib.SMTP("smtp.mail.yahoo.co.jp", 587)

#mail.starttls()
yahoo.login(from_email, from_passwd)
yahoo.send_message(msg)
print("send")
