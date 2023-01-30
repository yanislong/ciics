#!/usr/bin/env python3

from scapy.all import *
import time, os, random

host = "11.2.77.3"  #请求地址
#host = "10.0.20.91"  #请求地址
port = 30088
#port = 8088
sp = 12787 + random.randint(1,10000)  #自己使用tcp的源端口

'''
try:
    os.system("iptables -D OUTPUT 1")
except:
    print("iptables role not ")
os.system("iptables -A OUTPUT -p tcp --tcp-flags RST RST -d 172.16.9.238 -j DROP")   #添加防火墙规则
'''

def run():
    sp = 12787 + random.randint(1,40000)  #自己使用tcp的源端口
    request = IP(dst=host)/TCP(dport=port,sport=sp,flags="S")   #定义syn包
    response = sr1(request)  #发送syn包,并保存返回包，存在request中
    #response.show()
#    print(response[0].res[0][1].show())
    print(response[1].seq)
    print(response[1].ack)
    request2 = IP(dst=host)/TCP(dport=port,sport=sp,flags='A',ack=response[1].seq+1,seq=response[1].ack)  
    #time.sleep(7) #tcp三次握手，服务端最后接受应答ack的时间大概7秒，超过7秒就过期，会返回RST
    send(request2)
    request2.show()
    
    request3 = IP(dst=host)/TCP(dport=port,sport=sp,flags='PA',ack=response[1].seq+1,seq=response[1].ack)/Raw('GET / HTTP/1.1\r\nHost: 11.2.77.3:30088\r\n\r\nHost_a: 123') #定义http请求包
    #request3 = IP(dst=host)/TCP(dport=port,sport=sp,flags='PA',ack=response[1].seq+1,seq=response[1].ack)/Raw('GET / HTTP/1.1\r\nHost: 10.0.20.91:8088\r\n\r\n') #定义http请求包
    
    #send(request3)
    #response2 = sr(request3)
    send(request3)
    #for i in response2[0].res[0]:
    #    print(hexdump(i))
    #    print(i[2].fields)
    #print(hexdump(response2))
    

for i in range(1):
    run()
