#!/usr/bin/env python3

from multiprocessing.managers import BaseManager
from multiprocessing import Process, freeze_support
import time, sys, queue, os, re, json, logging, random
import threading, queue
import socket
import requests


# 从task队列取任务,并把结果写入result队列:
def prun(result):
    for i in range(tnum):
        #t = threading.Thread(target=modifyUserInfo,args=())
        t = threading.Thread(target=getMessage,args=())
        #t = threading.Thread(target=test)
       # t = threading.Thread(target=login,args=(result,))
        #t.setDaemon(True)
        threadingPool.append(t)
        t.start()
    for j in threadingPool:
        j.join()
    
def test():
    url = "http://159.226.90.74/static/img/press_old.602dd9e.png"
    r = requests.get(url)
    print(r.status_code)
    return None
#portal系统登录返回session
def login(result=None):
    global testdata
    global errnum
    url = "http://" + testdata['url1'] + "/portal/new/login"
    header = {}
    data = {}
    data['username'] = testdata['username']
    data['password'] = testdata['passwd']
    try:
        res = requests.post(url, headers=header, data=data)
    except requests.exceptions.ConnectionError:
        print("无法链接请求地址%s" %testdata['url1'])
        result.put(1)
        return None
    if res.status_code == 200:
        print("服务端响应: " + res.text)
        try:
            tt = res.json()['data']['token']
        except:
            print("获取认证失败")
            return None
        if random.randint(1,3) == 4:
            num += 1
            if num < 5:
                sec = res.elapsed.total_seconds()
                print("响应时间: %s" % sec)
        #print(tt)
        return tt
    else:
       # if random.randint(1,20) == 5:
        result.put(1)
    return None

def blogin():
    url = "http://" + testdata['url2']+ "/portal/user/exists?accountOrEmail=823196834@qq.com"
    try:
        res = requests.get(url)
    except requests.exceptions.ConnectionError:
        print("无法链接请求地址%s" %testdata['url1'])
        return None
    try:
        tt = res.json()['msg']
    #    print(tt)
        return tt
    except:
        print('登录失败')
        sys.exit()

#获取消息数量
def getMessage():
    url = "http://" + testdata['url1'] + "/portal/notice/noticeCount"
    header = {}
    header['Cookie'] = "JSESSIONID=" + mytoken
    try:
        res = requests.get(url, headers=header)
    except requests.exceptions.ConnectionError:
        print("无法链接请求地址%s" %testdata['url1'])
        return None
    try:
        mm = res.json()
        print(mm)
    except:
        print('获取消息失败')
    finally:
        return None

#获取消息数量
def getMessage2():
    url = "http://" + testdata['url1'] + "/portal/cloundHost/flavorLists?pageNum=1&pageSize=1&flavorName="
    header = {}
    header['Cookie'] = "JSESSIONID=" + mytoken
    try:
        res = requests.get(url, headers=header)
    except requests.exceptions.ConnectionError:
        print("无法链接请求地址%s" %testdata['url1'])
        return None
    try:
        mm = res.json()
        print(mm)
    except:
        print('获取消息失败')
    finally:
        return None

#请求修改用户资料接口
def modifyUserInfo():
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
        return None
    if str(res.status_code) == "200":
        sec = res.elapsed.total_seconds()
        print("响应时间: %s" % sec)
    #    print(res.content)
        return None
    else:
        print("gateway timeout %d"%res.status_code)
        return None


if __name__ == "__main__":
    host = "0.0.0.0"
    result = queue.Queue()
    class QueueManager(BaseManager):
        pass
    QueueManager.register('get_num',callable=lambda: result)
    manager = QueueManager(address=(host, 5566), authkey=b'abc')
    manager.start()
    result = manager.get_num()
    num = 0
    #进程队列
    processpool = []
    #线程队列
    threadingPool = []
    #进程数量
    pnum = 1
    #线程数量
    tnum = 5
    rnum = 1
    errnum = 0
    #测试环境配置
    #testdata = {"url1":"1.71.191.200","url2":"11.2.77.3","username":"testpro","passwd":"123456aA~"}
    #怀柔环境配置
    testdata = {"url1":"159.226.90.74","url2":"159.226.90.74","username":"hebing","passwd":"123456aA~"}
    #日志配置
    LOG_FORMAT= "%(asctime)s %(levelname)s %(message)s" 
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S %a" 
    FNAME = time.strftime("%Y-%m-%d#%H-%M-%S",time.localtime())
    if not os.path.exists('log'):
        os.makedirs('log')
    logging.basicConfig(level=logging.DEBUG,format=LOG_FORMAT,datefmt=DATE_FORMAT,filename='./log/' + FNAME + '.log') 
    #获取用户登录session
    mytoken = login()
    #mytoken = blogin()
    for k in range(rnum):
        time.sleep(1)
        mydata = []
        #每次迭代等待时间
        print("############第%d此迭代开始##################"%(k+1))
        starttime = time.strftime("%Y/%m/%d %H:%M:%S",time.localtime())
        for i in range(pnum):
            p = Process(target=prun,args=(result,))
            processpool.append(p)
            p.start()
        for j in processpool:
            j.join()
        endtime = time.strftime("%Y/%m/%d %H:%M:%S",time.localtime())
        print("############第%d此迭代结束##################"%(k+1))
    # 处理结束:
    total = pnum * tnum * rnum
    #result.put(1)
    #for i in range(10):
    #     result.put(1)
    errnum = result.qsize()
    print("(包含初始数据准备时间) 程序运行 开始时间:{0}，结束时间:{1}".format(starttime,endtime))
    print("执行请求总次数: {0}".format(total))
    print("执行请求成功次数: {0}".format((total) - errnum))
    print("执行请求总率: %.4f%%" %(((int(total) - errnum)/ int(total)) * 100))
    print('worker exit.')
