#!/usr/bin/env python3

import socket

sk = socket.socket()
address = ('10.0.20.167',8000)
print(sk)
sk.connect(address)
while True:
    inp = input('>>>>>.')
    if inp == 'exit':
        break
    sk.send(bytes(inp,'utf8'))
    result_len = int(str(sk.recv(1024),'utf8'))
    print(result_len)
    data = bytes()
    while len(data) != result_len:
        recv = sk.recv(1024)
        data += recv
    print(str(data,'gbk'))
sk.close()
