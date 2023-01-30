#!/usr/bin/env python3

from multiprocessing.managers import BaseManager
from multiprocessing import Process, freeze_support
import time, sys, queue, os, re, json, logging, random
import threading, queue
import socket
import requests


# 从task队列取任务,并把结果写入result队列:
def prun(cname,result,errnum,tn,mytoken,testdata,k):
    cname = cname + "_" + str(os.getpid())
    threadingPool = []
    for i in range(tn):
        t = threading.Thread(target=modifyUserInfo,args=(cname,result,errnum,mytoken,testdata,k))
        #t = threading.Thread(target=submitWork,args=(result, errnum))
        threadingPool.append(t)
        t.start()
    for j in threadingPool:
        j.join()
    
#portal系统登录返回session
def login():
    global testdata
    url = "http://" + testdata['url1'] + "/portal/new/login"
    header = {}
    data = {}
    data['username'] = testdata['username']
    data['password'] = testdata['passwd']
    res = requests.post(url, headers=header, data=data)
   # print(res.text)
    tt = res.json()['data']['token']
    print(tt)
    #l1 = re.compile('token":"(.*?)"')
    #l2 = l1.findall(res.text)
    #return l2[0]
    return tt

#请求修改用户资料接口
def modifyUserInfo(cname=None,result=None,errnum=None,mytoken=None,testdata=None,k=None):
    global portest
    url = "http://" + testdata['url2'] + "/portal/user/sysUserUpdate"
    header = {}
    header['Cookie'] = "JSESSIONID=" + mytoken
    header["Content-Type"] = "application/json;charset=UTF-8"
    data = {}
    data["id"] = "10564"
    data["account"] = testdata['username']
    data["name"] = "型男" + str(random.randint(100,999))
    data["kjyPassport"] = ""
    data["email"] = ""
    data["userType"] = "0"
    data["phone"] = ""
    data["companyId"] = "1"
    data["roleId"] = "10186"
    data["firstLogin"] = "1"
    try:
        res = requests.post(url, headers=header, data=json.dumps(data), timeout=(61,121))
    except requests.exceptions.ConnectTimeout:
        print("requests.exceptions.ConnectTimeout")
        errnum.put([cname + "_"+ str(k),'506'])
        return None
    except requests.exceptions.Timeout:
        print("requests.exceptions.Timeout")
        errnum.put([cname + "_"+ str(k),'507'])
        return None
    except requests.exceptions.ConnectionError:
        print("requests.exceptions.ConnectionError")
        errnum.put([cname + "_"+ str(k),'508'])
        return None
    if str(res.status_code) == "200":
        sec = res.elapsed.total_seconds()
        portest.put(sec)
        return None
    else:
        errnum.put([ cname + "_" + str(k),res.status_code])
        print("gateway timeout %d"%res.status_code)
        #logging.debug(str(res.status_code) + res.text + str(res.elapsed.total_seconds()))
        return None

#提交工单会给客户发送邮件，确认后再用
def submitWork(c,porerr,hd=None):
    """提交工单"""
    url = "http://" + testdata['url1'] + "/portal/workSheet/submitWorkSheet"
    '''
    data = OrderedDict([("phone",("","13112341234")),
            ("problemDescribe",(None,"test")),
            ("email",(None,"335916781@qq.com")),
            ("priority",(None,22)),
            ("status",(None,1)),
            ("userId",(None,"10046")),
            ("problemDescribe",(None,11)),
            ("workSheetTypeId",(None,3))])
    '''
    data = {"JSESSIONID":(None,mytoken),"phone":(None,"13112341234"), "problemDescribe":(None,"test"), "email":(None,"335916781@qq.com"), "priority":(None, "22"),"status":(None,"1"), "userId":(None,"10564"),"problemDescribe":(None,11),"workSheetTypeId":(None,3),"workSheetProblemId":(None,"8")}
    try:
        res = requests.post(url, headers=hd, files=data, timeout=(61,121))
#        print(res.request.body)
#        print(res.request.headers)
    except requests.exceptions.ConnectTimeout:
        print("requests.exceptions.ConnectTimeout")
        porerr.put('506')
        return None
    except requests.exceptions.Timeout:
        print("requests.exceptions.Timeout")
        porerr.put('507')
        return None
    except requests.exceptions.ConnectionError:
        print("requests.exceptions.ConnectionError")
        porerr.put('508')
        return None
   # except ChunkedEncodingError:
   #     print("ChunkedEncodingError")
   #     porerr.put('509')
   #     return None
    if str(res.status_code) == "200":
        sec = res.elapsed.total_seconds()
        if random.randint(1,100) == 1:
            c.put(sec)
        print(res.content)
        return None
    else:
        print(res.status_code)
        porerr.put(res.status_code)
        return None




if __name__ == "__main__":
    portest = queue.Queue()
    #服务端地址
    #server_addr = '10.0.117.135'
    server_addr = '192.168.18.128'
    #进程池
    processpool = []
    #获取客户端主ip
    clientName = socket.getfqdn(socket.gethostname())
    #测试环境配置
    testdata = {"url1":"1.71.191.200","url2":"11.2.77.3","username":"testpro","passwd":"123456aA~"}
    #怀柔环境配置
    #testdata = {"url1":"159.226.90.74","url2":"159.226.90.74","username":"u3359167","passwd":"123456"}
    #日志配置
    LOG_FORMAT= "%(asctime)s %(levelname)s %(message)s" 
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S %a" 
    FNAME = time.strftime("%Y-%m-%d#%H-%M-%S",time.localtime())
    if not os.path.exists('log'):
        os.makedirs('log')
    logging.basicConfig(level=logging.DEBUG,format=LOG_FORMAT,datefmt=DATE_FORMAT,filename='./log/' + FNAME + '.log') 
    #获取用户登录session
    mytoken = login()
    # 创建类似的QueueManager:
    class QueueManager(BaseManager):
        pass
    # 由于这个QueueManager只从网络上获取Queue，所以注册时只提供名字:
    QueueManager.register('get_task_queue')
    QueueManager.register('get_result_queue')
    QueueManager.register('get_rept_queue')
    QueueManager.register('get_err_queue')
    # 连接到服务器，也就是运行task_master.py的机器:
    print('Connect to server %s...' % server_addr)
    # 端口和验证码注意保持与task_master.py设置的完全一致:
    m = QueueManager(address=(server_addr, 5000), authkey=b'abc')
    # 从网络连接:
    while True:
        try:
            m.connect()
            print("Connect success.")
            break
        except ConnectionRefusedError:
            continue
    # 获取Queue的对象:
    task = m.get_task_queue()
    result = m.get_result_queue()
    rept = m.get_rept_queue()
    errnum = m.get_err_queue()
    while True:
        try:
            taskResult = task.get()
            print(taskResult)
            break
        except:
            continue
    myll = []
    for k in range(taskResult['iterationTimes']):
        mydata = []
        #每次迭代等待时间
        print("############第%d此迭代开始##################"%(k+1))
        time.sleep(taskResult['waitingTime'])
        starttime = time.strftime("%Y/%m/%d %H:%M:%S",time.localtime())
        for i in range(taskResult['processNumber']):
            freeze_support()
            p = Process(target=prun,args=(clientName,result,errnum,taskResult['threadNumber'],mytoken,testdata,k))
            processpool.append(p)
            p.start()
        for j in processpool:
            j.join()
        endtime = time.strftime("%Y/%m/%d %H:%M:%S",time.localtime())
        mydata = {"start":starttime,"end":endtime,"cname":clientName,"iteration":k}
        print(mydata)
        rept.put(mydata)
        for i in range(portest.qsize()):
            myll.append(i)
        print({clientName:myll})

        print("############第%d此迭代结束##################"%(k+1))
    # 处理结束:
    print('worker exit.')
