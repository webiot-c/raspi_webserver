#!/usr/bin/python3
# coding: utf-8

import cgi
import sys
import io

from socket import socket, AF_INET, SOCK_STREAM

request_types = {"START": "OPEN", "POLLING": "POLLING", "END": "CLOSE"}

HOST = "localhost"
PORT = 12345

form = cgi.FieldStorage()

def isFloat(test_data):
    # TODO: マイナス問題の解決
    return test_data.count(".") == 1 and test_data.replace(".", "").isdigit()

def sendToBroadcaster(req):
    while True:
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect((HOST, PORT))
        sock.send(req.encode('utf-8'))

        sock.close()
        break

def main():
    print("Content-type: text/plain\n")

    if ('node_id' not in form) or ('lat_data' not in form) or \
       ('long_data' not in form) or ('type' not in form):
        sys.stdout.write("ER!NOSET")
        sys.exit()

    prm_node_id   = form.getvalue("node_id", "")
    prm_lat_data  = form.getvalue("lat_data", "")
    prm_long_data = form.getvalue("long_data", "")
    prm_type      = form.getvalue("type", "")

    if not (isFloat(prm_lat_data) and isFloat(prm_long_data)):
        sys.stdout.write("ER!WRONG")
        sys.exit()
    
    if prm_type not in request_types:
        sys.stdout.write("ER!WRONG")
        sys.exit()
    
    request = "AED-%s#%s#%s#%s" % (request_types[prm_type], prm_node_id, prm_lat_data, prm_long_data)
    
    sendToBroadcaster(request)
    
    sys.stdout.write("OK!     ");

main()

