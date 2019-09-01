#!/usr/bin/env python3
# coding: utf-8

from websocket_server import WebsocketServer
from socket import socket, AF_INET, SOCK_STREAM
from email.mime.text import MIMEText

import configparser
import smtplib
import threading
import sqlite3
import re
import os.path

### 変数
SKT_HOST = "localhost"
SKT_PORT = 12345
WS_HOST = "0.0.0.0"
WS_PORT = 6789

MAX_CON_COUNT  = 8
MAX_MSG_LENGTH = 128

server = None

def websocket_main():
    global server

    server = WebsocketServer(WS_PORT, host=WS_HOST)
    server.run_forever()

def getEmailFromDatabase():
    
    conn = sqlite3.connect('/var/www/html/mail-DB/mail.db')
    c = conn.cursor()
    
    #値を連続して表示
    c.execute('select group_concat(email) from data')
    
    value = c.fetchall()
    print(value)
    formatted = ""
    for elem in value[0]:
        formatted += elem
    
    return formatted

def main():
    
    from_email = ""
    from_passwd = ""
    

    config = configparser.ConfigParser()
    config.read('passwd.ini')
    from_email = config["SMTP"]["email"]
    from_passwd =config["SMTP"]["passwd"]

    websocket_thread = threading.Thread(target=websocket_main)
    websocket_thread.start()
    
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind((SKT_HOST, SKT_PORT))
    sock.listen(MAX_MSG_LENGTH)

    while True:
        try:
            conn, addr = sock.accept()
            req = conn.recv(MAX_MSG_LENGTH).decode('utf-8')
            conn.close()
            
            print("received; ")
            print(req)

            server.send_message_to_all(req)

            req_elems = req.split("#")
            
            print(req_elems)
            print(req_elems[0])
            if req_elems[0] != "AED-OPEN":
                continue
            
            node_name = req_elems[1]
            map_url = "https://www.google.com/maps/?q=%f,%f" % (float(req_elems[2]), float(req_elems[3]))

            to_email = getEmailFromDatabase()
            
            message = "TEST MAIL 応急救護の協力をお願いします<br>AEDの場所<br>" + map_url
            subject = "test mail[複数送信]"
            
            msg = MIMEText(message, "html")
            msg["Subject"] = subject
            msg["To"] = to_email
            msg["From"] = from_email

            yahoo = smtplib.SMTP("smtp.mail.yahoo.co.jp", 587)

            #mail.starttls()
            yahoo.login(from_email, from_passwd)
            yahoo.helo()
            yahoo.send_message(msg)

            print("Mail was sent!")
            

        except Exception as e:
            # HAX: 2回 Ctrl-c を叩く必要がある。プロセス停止の方法がわからない！
            print("Connection Error, may be keyboard interruption?")
            print("Program will be terminated.")

            print(str(type(e)))
            print(str(e.args))
            print(str(e))

            break
    
if __name__ == "__main__":
    main()

