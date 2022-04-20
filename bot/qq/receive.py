#!
#coding=utf-8

import socket
import json

ListenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ListenSocket.bind('127.0.0.1', 5700)
ListenSocket.listen(100)

HttpResponseHeader = '''HTTP/1.1 200 OK
Content-Type: text/html
'''

def request_to_json(msg):
    for i in range(len(msg)):
        if msg[i] == "{" and msg[-1] == "\n":
            return json.loads(msg[i:])
    return None

#need to be executed iterately,  the return value is in json format
def rev_msg():
    client, address = ListenSocket.accept()
    request = client.recv(1024).decode(encoding='utf-8')
    rev_json = request_to_json(request)
    client.sendall(HttpResponseHeader).encode(encoding = 'utf-8')
    client.close()
    return rev_json

