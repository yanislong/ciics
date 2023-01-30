#!/usr/bin/env python
# -*-coding:utf-8 -*-

import socket
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

host = "0.0.0.0"
port = 8081

sl = socket.socket()
sl.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
sl.bind((host,port))
sl.listen(5)
recv_buff = sl.getsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF)
send_buff = sl.getsockopt(socket.SOL_SOCKET,socket.SO_SNDBUF)
#print(recv_buff)
#print(send_buff)

while True:
    conn, addr = sl.accept()
    print "connect:", addr
    cdata = conn.recv(2048)
    src = cdata.split(" ")[1]
    #print(src)
    #cc = cdata.split('\r\n\r\n')
    cc = src.split('?')
    if cc[0] == "/long":
        print cc[0]
        content = "HTTP/1.1 200 ok\r\nContent-Type: application/json;charset=utf8\r\nTip: casjc\r\n\r\n"
        content = content + '{"res":200,"msg":"ok"}'
        conn.sendall(content)
    else:
        conn.sendall('not allow')
    #conn.close()
    #sys.exit()
