#
#

import requests
import re
import json
import socket
import os

# basic api

#send message
def send_msg(resp_dict):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    ip = '127.0.0.1'
    client.connect(ip, 5700)

    msg_type = resp_dict['msg_type']
    number = resp_dict['number'] # QQid
    msg = resp_dict['msg']

    #encoding special chars
    msg = msg.replace(" ", "%20")
    msg = msg.replace("\n", "%0a")

    if msg_type == 'group':
        payload = "GET /send_group_msg?group_id=" + str(number)
        + "&message=" + msg + " HTTP/1.1\r\nHost:"
        + ip + ":5700\r\nConnection: close\r\n\r\n"
    #elif msg_type == 'private'

    print("send" + payload)
    client.send(payload.encode("utf-8"))
    client.close()

def send_face(msg):
    msgs = '[CQ:face, id=' + msg + ']'
    return msgs

#image record video

def send_at(msg):
    if len(msg) == 0:
        msg = "all"
    msgs = '[CO:at.aa=' + msg + '['
    return msgs

# customized api