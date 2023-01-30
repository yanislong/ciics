#!/usr/bin/env python3
# -*-coding=utf-8 -*- 

import random, time, queue
from multiprocessing.managers import BaseManager
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from decimal import Decimal


threadTotal = 0
timeoutNumber = 0
tot = 0
sec_3 = 0
clientName = []
templl = []
host = "0.0.0.0"
# 发送任务的队列:
task_queue = queue.Queue()
# 接收结果的队列:
result_queue = queue.Queue()
rept_queue = queue.Queue()
err_queue = queue.Queue()

# 从BaseManager继承的QueueManager:
class QueueManager(BaseManager):
    pass

# 把两个Queue都注册到网络上, callable参数关联了Queue对象:
QueueManager.register('get_task_queue', callable=lambda: task_queue)
QueueManager.register('get_result_queue', callable=lambda: result_queue)
QueueManager.register('get_rept_queue', callable=lambda: rept_queue)
QueueManager.register('get_err_queue', callable=lambda: err_queue)
# 绑定端口5000, 设置验证码'abc':
manager = QueueManager(address=(host, 5000), authkey=b'abc')
# 启动Queue:
manager.start()
# 获得通过网络访问的Queue对象:
task = manager.get_task_queue()
result = manager.get_result_queue()
rept = manager.get_rept_queue()
err = manager.get_err_queue()

# 放几个任务进去:
while True:
    try:
        processNumber = int(input("please input process Numbers:(输入进程数量)\n"))
        threadNumber = int(input("please input threading Numbers:(输入线程数量)\n"))
        iterationTimes = int(input("please input iteration Times:(输入迭代次数)\n"))
        #waitingTime = int(input("please input waiting time:(输入等待时间)\n"))
        waitingTime = 1
        #ccn = int(input("please input client connect Numbers:(输入客户端链接数量)\n"))
        ccn = 1
        break
    except:
        print("input errer, only input numbers")
        continue
taskParam = {"processNumber": processNumber,
             "iterationTimes": iterationTimes,
             "waitingTime": waitingTime,
             "threadNumber": threadNumber,
             "clientConnectNumber": ccn}

for i in range(taskParam['clientConnectNumber']):
    task.put(taskParam)

print("waiting client connect...")
while True:
    try:
        #tt = result.get(timeout=(taskParam['waitingTime'] + 10))
        tt = result.get(timeout=10)
        print(tt)
        threadTotal += 1
        templl.append(tt[0])
        if tt[0] < 3.1:
            sec_3 += 1
    except queue.Empty:
        break
    tot += Decimal(str(tt[0]))
'''
    if tt[1].split("_")[0] not in clientName:
        clientName.append(tt[1].split("_")[0])
'''
cli = {"client":templl}
resdf = pd.DataFrame(cli)
try:
    resdf.plot()
except TypeError:
    cli = {"None":pd.Series([1,3,1])}
    resdf = pd.DataFrame(cli)
    resdf.plot()
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.xlabel("request client total")
plt.ylabel('reponse time(sec)')
plt.title("portal table")
plt.show()

print("#" * 14)
while not err.empty():
    s = err.get(timeout=10)
    print(s)
    timeoutNumber += 1

print("#" * 14)
print("total reponse time:%s"%tot)
#print("avg:%s"%(str(Decimal(tot/rt).quantize(Decimal(0.0000)))))
if threadTotal != 0:
    #print("avg:%s"%(str(tot/threadTotal)))
    print("所有完成响应的请求平均响应时间：%s"%(str(tot/threadTotal)))
if sec_3==0 or threadTotal==0:
    per = 0
#    print("connect time in 3 second: %d, percen %.2f%%" %(sec_3,per))
    print("请求响应完成时间在3秒钟以内的数量：0，占整体响应 %0")
else:
    per = round(Decimal(sec_3)/Decimal(threadTotal),2) * 100
#    print("connect time in 3 second: %d, percen %% %d" %(sec_3,per))
    print("请求响应完成时间在3秒钟以内的数量：%d，占整体响应 %% %d" %(sec_3,per))
#print("connect timeout total: %d" %timeoutNumber)
print("请求响应超时数量： %d" %timeoutNumber)
#print("Concurrent number: %d" %(taskParam['processNumber']*taskParam['threadNumber']*taskParam['clientConnectNumber']))
print("设置并发数量： %d" %(taskParam['processNumber']*taskParam['threadNumber']*taskParam['clientConnectNumber']))
#print("actual total: %d" %threadTotal)
print("实际完成的请求数量： %d" %threadTotal)
#print("server total requests: %d" %(taskParam['processNumber']*taskParam['iterationTimes']*taskParam['threadNumber']*taskParam['clientConnectNumber']))
print("任务总共设置发起的请求数量: %d" %(taskParam['processNumber']*taskParam['iterationTimes']*taskParam['threadNumber']*taskParam['clientConnectNumber']))

# 从result队列读取结果:
print('Try get results...')
for i in range(taskParam['iterationTimes']*taskParam['clientConnectNumber']):
    try:
        r = rept.get(timeout=10)
        print('Result: %s' % r)
    except queue.Empty:
        break
# 关闭:
manager.shutdown()
print('master exit.')
