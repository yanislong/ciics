#!/usr/bin/env python
#-*-coding=utf-8 -*-

from multiprocessing.managers import BaseManager
from multiprocessing import Process, freeze_support, Queue
import time, sys, os, re, json, logging, random
import threading
import requests
import socket
from progress.bar import Bar
from collections import OrderedDict, Iterable


# 从task队列取任务,并把结果写入result队列:
def prun(c,porerr,mytoken,threadTotal):
    threadingPool = []
    for i in range(threadTotal):
        t = threading.Thread(target=submitWork,args=(c,porerr,mytoken))
       # t = threading.Thread(target=getLog,args=(c,porerr,mytoken))
       # t = threading.Thread(target=roleList,args=(c,porerr,mytoken))
       # t = threading.Thread(target=modifyUserInfo,args=(c,porerr,mytoken))
        threadingPool.append(t)
        t.start()
    for j in threadingPool:
        j.join()
    
#portal系统登录返回session
def login():
    url = testdata['url1'] + "/portal/new/login"
    header = {}
    data = {}
    data['username'] = testdata['username']
    data['password'] = testdata['passwd']
    res = requests.post(url, headers=header, data=data)
    l1 = re.compile('token":"(.*?)"')
    l2 = l1.findall(res.text)
    header = {}
    header['Cookie'] = "JSESSIONID=" + l2[0]
    #header["Content-Type"] = "application/json;charset=UTF-8"
    return header

def roleList(c,porerr,hd=None):
    """获取角色列表"""
    url = testdata['url1'] + "/portal/role/allRoleList"
    try:
        res = requests.get(url, timeout=(61,121))
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
    except requests.ChunkedEncodingError:
        print("ChunkedEncodingError")
        porerr.put('509')
        return None
    if str(res.status_code) == "200":
        sec = res.elapsed.total_seconds()
        c.put(sec)
#        print(res.content)
        return None
    else:
        print(res.status_code)
        porerr.put(res.status_code)
        return None

def getLog(c,porerr,hd=None):
    """查询用户操作日志"""
    url = testdata['url1'] + "/portal/user/sysUserDetail?userId=335916781@qq.com"
    try:
        res = requests.get(url, headers=hd, timeout=(61,121))
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
    except requests.ChunkedEncodingError:
        print("ChunkedEncodingError")
        porerr.put('509')
        return None
    if str(res.status_code) == "200":
        sec = res.elapsed.total_seconds()
        c.put(sec)
#        print(res.content)
        return None
    else:
        print(res.status_code)
        porerr.put(res.status_code)
        return None

def MyTest(c,ee,tt=None):
    """测试百度"""
    url = "http://www.baidu.com"
    try:
        res = requests.get(url, timeout=(61,121))
    except requests.exceptions.ConnectTimeout:
        print("requests.exceptions.ConnectTimeout")
        return None
    except requests.exceptions.Timeout:
        print("requests.exceptions.Timeout")
        return None
    except requests.exceptions.ConnectionError:
        print("requests.exceptions.ConnectionError")
        return None
    except requests.ChunkedEncodingError:
        print("ChunkedEncodingError")
        return None
    if str(res.status_code) == "200":
        sec = res.elapsed.total_seconds()
        c.put(sec)
        return None
    else:
        print(res.status_code)
        ee.put(res.status_code)
        return None

def modifyUserInfo(c,porerr,hd):
    """修改用户资料"""
    url = testdata['url2'] + "/portal/user/sysUserUpdate"
    data = {}
    data["id"] = "10111"
    data["account"] = testdata['username']
    data["name"] = ""
    data["kjyPassport"] = ""
    data["email"] = ""
    data["userType"] = "0"
    data["phone"] = ""
    data["companyId"] = "1"
    data["roleId"] = "2"
    data["firstLogin"] = "1"
    try:
        res = requests.post(url, headers=hd, data=json.dumps(data), timeout=(61,121))
    except requests.exceptions.ConnectTimeout:
#        print("requests.exceptions.ConnectTimeout")
        porerr.put('506')
        return None
    except requests.exceptions.Timeout:
#        print("requests.exceptions.Timeout")
        porerr.put('507')
        return None
    except requests.exceptions.ConnectionError:
#        print("requests.exceptions.ConnectionError")
        porerr.put('508')
        return None
    except requests.ChunkedEncodingError:
#        print("ChunkedEncodingError")
        porerr.put('509')
        return None
    if str(res.status_code) == "200":
        sec = res.elapsed.total_seconds()
        c.put(sec)
        return None
    else:
#        print("gateway timeout %d"%res.status_code)
        porerr.put(res.status_code)
        return None

def submitWork(c,porerr,hd=None):
    """提交工单"""
    url = testdata['url1'] + "/portal/workSheet/submitWorkSheet"
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
    data = {"phone":(None,"13112341234"), "problemDescribe":(None,"test"), "email":(None,"335916781@qq.com"), "priority":(None, "22"),"status":(None,"1"), "userId":(None,"10046"),"problemDescribe":(None,11),"workSheetTypeId":(None,3),"workSheetProblemId":(None,"8")}
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
        if random.randint(1,100) = 1:
            c.put(sec)
#        print(res.content)
        return None
    else:
        print(res.status_code)
        porerr.put(res.status_code)
        return None

if __name__ == "__main__":
    portest = Queue()
    porerr = Queue()
    #服务端地址
    server_addr = '10.0.168.183'
    #获取客户端主ip
    clientName = socket.getfqdn(socket.gethostname())
    #测试环境配置
    #testdata = {"url1":"1http://.71.191.200","url2":"http://192.168.15.21","username":"gege123","passwd":"123456"}
    #怀柔环境配置
    testdata = {"url1":"http://159.226.90.74","url2":"http://159.226.90.74","username":"u3359167","passwd":"123456aA~"}
    #获取用户登录session
    try:
        mytoken = login()
    except:
        print("登录失败，请检查网络或请求参数")
        sys.exit()
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
    '''
    while True:
        try:
            m.connect()
            print("Connect success.")
            # 获取Queue的对象:
            task = m.get_task_queue()
            result = m.get_result_queue()
            rept = m.get_rept_queue()
            errnum = m.get_err_queue()
            while True:
                try:
                     taskResult = task.get()
                     print(taskResult)
                except:
                    continue
        except ConnectionRefusedError:
            break
        except TimeoutError:
            break
    '''
    #进程池
    processPool = []
    myll = {}
    myerr = []
    threadTotal = 80
    processTotal = 80
    m = 1
    bar = Bar("process start", max=m, fill="@", suffix="%(percent)d%%")
    for k in range(m):
       # print("   ############第%d此迭代开始############"%(k+1))
        starttime = time.strftime("%Y/%m/%d %H:%M:%S",time.localtime())
        for i in range(processTotal):
            #freeze_support()  #window 
            p = Process(target=prun,args=(portest,porerr,mytoken,threadTotal))
            processPool.append(p)
            p.start()
        for j in processPool:
            j.join()
        endtime = time.strftime("%Y/%m/%d %H:%M:%S",time.localtime())
        bar.next()
    bar.finish()
    print(portest.qsize())
   # for i in range(portest.qsize()):
   #     tmp = portest.get(i)
   #     myll[i] = tmp
    print(porerr.qsize())
   # for j in range(porerr.qsize()):
   #     tmp2 = porerr.get(j)
   #     myerr.append(tmp2)
    print(myll)
    print(myerr)
    print('worker exit.')
