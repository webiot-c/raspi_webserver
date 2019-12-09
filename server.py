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
import textformatter

import RPi.GPIO as GPIO
import time

### 変数
SKT_HOST = "localhost"
SKT_PORT = 12345
WS_HOST = "0.0.0.0"
WS_PORT = 6789

MAX_CON_COUNT  = 8
MAX_MSG_LENGTH = 128

GPIO_RED    = 26
GPIO_YELLOW = 19
GPIO_GREEN  = 13
GPIO_BUTTON = 12

server = None

def initialize_leds():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_RED, GPIO.OUT) # Green  LED ( Working Normally )
    GPIO.setup(GPIO_YELLOW, GPIO.OUT) # Yellow LED ( Request working )
    GPIO.setup(GPIO_GREEN, GPIO.OUT) # Red    LED ( Error )
    GPIO.setup(GPIO_BUTTON, GPIO.IN)  # Button     ( Clear Error Indicator )
    
    GPIO.output(GPIO_RED, GPIO.HIGH)
    GPIO.output(GPIO_YELLOW, GPIO.HIGH)
    GPIO.output(GPIO_GREEN, GPIO.HIGH)
    
    time.sleep(0.5)

    GPIO.output(GPIO_RED, GPIO.LOW)
    # Keep Yellow LED
    GPIO.output(GPIO_GREEN, GPIO.LOW)

def turn_on_led(gpio):
    GPIO.output(GPIO_RED, GPIO.LOW)
    GPIO.output(GPIO_YELLOW, GPIO.LOW)
    GPIO.output(GPIO_GREEN, GPIO.LOW)
    
    GPIO.output(gpio, GPIO.HIGH)

def terminate_leds():
    GPIO.output(GPIO_RED, GPIO.LOW)
    GPIO.output(GPIO_YELLOW, GPIO.LOW)
    GPIO.output(GPIO_GREEN, GPIO.LOW)
    GPIO.cleanup()

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

def getSendHTML(aed_node, lat, lon, url):
    html = ""
    with open("mail_template.html") as f:
        html = f.read()
    html = textformatter.formatText(html, {"node_id": aed_node, "lat":lat, "lon":lon, "url":url})

    return html

def main():
    
    initialize_leds()

    from_email = ""
    from_passwd = ""

    config = configparser.ConfigParser()
    config.read('/var/www/html/passwd.ini')
    from_email = config["SMTP"]["email"]
    from_passwd =config["SMTP"]["passwd"]

    websocket_thread = threading.Thread(target=websocket_main)
    websocket_thread.start()
    
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind((SKT_HOST, SKT_PORT))
    sock.listen(MAX_MSG_LENGTH)

    while True:
        try:
            turn_on_led(GPIO_GREEN)
            
            conn, addr = sock.accept()
            req = conn.recv(MAX_MSG_LENGTH).decode('utf-8')
            conn.close()
            
            turn_on_led(GPIO_YELLOW)
            
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
            
            message = getSendHTML(node_name, float(req_elems[2]), float(req_elems[3]), map_url)
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
            
            turn_on_led(GPIO_GREEN)
        
        except KeyboardInterrupt:
            terminate_leds()
            print("Detected KeyboardInterruption (Pushed Ctrl-c?)")
            print("The program has ** NOT ** finished yet.")
            print("Please push ctrl-c TWICE.")
            
            break

        except:
            import traceback
            # HAX: 2回 Ctrl-c を叩く必要がある。プロセス停止の方法がわからない！
            print("Error occured!")
            traceback.print_exc()
            
            turn_on_led(GPIO_RED)

if __name__ == "__main__":
    main()

