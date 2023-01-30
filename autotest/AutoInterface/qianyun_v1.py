#!/usr/bin/env python3

import requests
import re, json, time, queue, sys, random
from threading import Thread, Lock
import hashlib
import pandas as pd
import matplotlib.pyplot as plt
import pycurl
from io import BytesIO
import urllib
import numpy as np
from decimal import Decimal
import pymysql
from datetime import datetime

np.set_printoptions(suppress=True)

class qianyun():

    def __init__(self,rTime):
        self.resTime = rTime
        self.myurl = "http://192.168.15.25"
        self.username = "sysadmin"       
        mypw = hashlib.md5()
        mypw.update("Sugon123".encode('utf-8'))
        self.passwd = mypw.hexdigest()
        self.mycookie = self.login()
        self.header = {}
        self.header['Cookie'] = "JSESSIONID=" + self.mycookie
       # self.hostId = str(self.cloudHostList().json()['content'][0]['id'])
       # self.cardId = str(self.queryCardList().json()['content'][0]['id'])
        self.deployId = ""
        self.hostId = "8a6251a4-6ba0-4012-b79b-e50f2db3ed01"
        self.cardId = "00f7031f-999a-4cbc-b711-dc99da83a087"
        self.getRequest = ["url"]

        

    def login(self):
         s = requests.Session()
         url = self.myurl + "/login"
         param = {}
         param["username"] = self.username
         param['password'] = self.passwd
         param['encrypted'] = True
         param['loginType'] = "Normal"
         res = s.post(url,params=param)
         l1 = re.compile('JSESSIONID=(.*?);')
         l2 = l1.findall(res.headers['Set-Cookie'])
         #print(l2[0])
         return l2[0]    
    
    """业务功能"""


    #查询已有网络
    def queryExistNetwork(self):
        """查询已有网络"""
        url = self.myurl + "/cloudprovider?action=queryCloudResource"
        self.header['Content-Type'] = "application/json"
        data = {
 "businessGroupId":None,
 "cloudResourceType": "cloudchef.openstack.nodes.Server::network",
 "cloudEntryId": ""
 }
        res = requests.post(url, headers=self.header, data=json.dumps(data))
        print(res.text)
        print( "请求接口: <" + self.queryExistNetwork.__doc__  + "> 用时：%s \n" %(res.elapsed.total_seconds()))
        self.resTime.put(res.elapsed.total_seconds())
        return res

    #获取卡片列表
    def queryCardList(self):
        """获取卡片列表"""
        url = self.myurl + "/catalogs/published?page=1&size=1&sort=asc"
        res = requests.get(url, headers=self.header)
       # print(res.text)
        print( "请求接口: <" + self.queryCardList.__doc__  + "> 用时：%s \n" %(res.elapsed.total_seconds()))
        self.resTime.put(res.elapsed.total_seconds())
        return res

    #获取卡片详情
    def queryCardInfo(self):
        """获取卡片详情"""
        mid = self.cardId
        url = self.myurl + "/catalogs/" + mid
        res = requests.get(url, headers=self.header)
      #  print(res.text)
        print( "请求接口: <" + self.queryCardInfo.__doc__  + "> 用时：%s \n" %(res.elapsed.total_seconds()))
        self.resTime.put(res.elapsed.total_seconds())
        return res

    #获取卡片蓝图参数
    def queryCardParam(self):
        """获取卡片蓝图参数"""
        mid = self.cardId
        url = self.myurl + "/catalogs/" + mid + "/inputs"
        res = requests.get(url, headers=self.header)
       # print(res.text)
        print( "请求接口: <" + self.queryCardParam.__doc__  + "> 用时：%s \n" %(res.elapsed.total_seconds()))
        self.resTime.put(res.elapsed.total_seconds())
        return res

    #获取规格详情
    def querySpecsInfo(self):
        """获取规格详情"""
        url = self.myurl + "/cloudprovider?action=queryCloudResource"
        self.header['Content-Type'] = "application/json"
        data = {
 "cloudResourceType":"cloudchef.openstack.nodes.Server::flavor",
    "queryProperties":{"physicalTemplateId":"",
                       "logicTemplateId":"",
                       "resourceBundleId":""}
}
        res = requests.post(url, headers=self.header,data=json.dumps(data))
      #  print(res.text)
        print( "请求接口: <" + self.querySpecsInfo.__doc__  + "> 用时：%s \n" %(res.elapsed.total_seconds()))
        self.resTime.put(res.elapsed.total_seconds())
        return res

    #获取磁盘类型列表
    def queryDiskTypeList(self):
        """获取磁盘类型列表"""
        url = self.myurl + "/cloudprovider?action=queryCloudResource"
        self.header['Content-Type'] = "application/json"
        data = {"cloudResourceType":"yacmp:cloudentry:type:openstack::volume-type"}
        res = requests.post(url, headers=self.header,data=json.dumps(data))
       # print(res.text)
        print( "请求接口: <" + self.queryDiskTypeList.__doc__  + "> 用时：%s \n" %(res.elapsed.total_seconds()))
        self.resTime.put(res.elapsed.total_seconds())
        return res

    #申请虚机
    def applyVirtualMachine(self):
        """申请虚机"""
        mid = self.cardId
        vmname = "portal_" + time.strftime("%Y%m%d%H:%M:%S",time.localtime()) + str(random.randint(100,999))
        url = self.myurl + "/catalogs/provision/deployment/" + mid
        self.header['Content-Type'] = "application/json"
        tempdata = '[{"Network_resource_id":"66ef2332-e812-4287-8c2e-f6738bb70e04","Server_server_logic_template_id":"56668877-d775-4a7a-9f14-56203a218fc6","Server_server_physical_template_id":"eb0c4619-dceb-496d-9448-6d1479b18b3d","Server_server_volume_type":"DS900_1_SSD","modify_pass_lin_root_pass":"Sugon123","Network_subnet_id":"6410fbdd-0319-40d5-a782-c02ff1d1d76d","Server_server_volume_size":100,"Server_flavor":"12","Server_server_vm_display_name":"%s"}]'%vmname
        data = {
    "reason":"",
    "attachments":{

    },
    "kind":"PROVISION",
    "paramJson":tempdata,
    "count":1,
    "requestParameters":{
        "extensibleParameters":[
            {
            }
        ]
    },
    "ownerId":"sysadmin",
    "deploymentShutdownDuration":11052,
    "number":1,
    "nodes":[

    ],
    "businessGroupId":"0f975778-1d94-4b61-8d6c-f369356b2a39",
    "scheduleDate":None,
    "deploymentName":"",
    "deploymentTeardownDuration":7,
    "projectId":""
}
        res = requests.post(url, headers=self.header,data=json.dumps(data))
        try:
            self.deployId = res.json()[0]['deployment']['id']
        except:
            print(res.text)
       # print(res.text)
        print( "请求接口: <" + self.applyVirtualMachine.__doc__  + "> 用时：%s \n" %(res.elapsed.total_seconds()))
        self.resTime.put(res.elapsed.total_seconds())
        return res

    #重置密码
    def resetPasswd(self):
        """重置密码"""
        mid = self.hostId
        url = self.myurl + "/nodes/" + mid + "/execute-resource-action"
        self.header['Content-Type'] = "application/json"
        data = {"resourceActionId":"reset_password","executeParameters":{"username":"gege123","newPassword":"123456"}}
        res = requests.post(url, headers=self.header,data=json.dumps(data))
      #  print(res.text)
        print( "请求接口: <" + self.resetPasswd.__doc__  + "> 用时：%s \n" %(res.elapsed.total_seconds()))
        self.resTime.put(res.elapsed.total_seconds())
        return res

    #虚机关机
    def stopVirtualMachine(self):
        """虚机关机"""
        hostid = self.hostId
        url = self.myurl + "/nodes/execute-action"
        self.header['Content-Type'] = "application/json"
        data = {hostid:{"operationName":"stop","scheduledTime":None}}
        res = requests.post(url, headers=self.header,data=json.dumps(data))
      #  print(res.text)
        print( "请求接口: <" + self.stopVirtualMachine.__doc__  + "> 用时：%s \n" %(res.elapsed.total_seconds()))
        self.resTime.put(res.elapsed.total_seconds())
        return res

    #虚机开机
    def startVirtualMachine(self):
        """虚机关机"""
        hostid = self.hostId
        url = self.myurl + "/nodes/execute-action"
        self.header['Content-Type'] = "application/json"
        data = {hostid:{"operationName":"start","scheduledTime":None}}
        res = requests.post(url, headers=self.header,data=json.dumps(data))
       # print(res.text)
        print( "请求接口: <" + self.startVirtualMachine.__doc__  + "> 用时：%s \n" %(res.elapsed.total_seconds()))
        self.resTime.put(res.elapsed.total_seconds())
        return res

    #虚机重启
    def resetVirtualMachine(self):
        """虚机重启"""
        mid = self.hostId
        url = self.myurl + "/nodes/" + mid + "/execute-resource-action"
        self.header['Content-Type'] = "application/json"
        data = {"resourceActionId":"reboot","scheduledTime":None}
        res = requests.post(url, headers=self.header,data=json.dumps(data))
       # print(res.text)
        print( "请求接口: <" + self.resetVirtualMachine.__doc__  + "> 用时：%s \n" %(res.elapsed.total_seconds()))
        self.resTime.put(res.elapsed.total_seconds())
        return res

    #虚机卸载
    def uninstallVirtualMachine(self):
        """虚机卸载"""
        url = self.myurl + "/deployments/execute-action"
        self.header['Content-Type'] = "application/json"
        data = {"XXXXXX(deploymentd)":{"operationName":"Tear Down","scheduledTime":None,"operationParamJson":"{}"}}
        res = requests.post(url, headers=self.header,data=json.dumps(data))
      #  print(res.json())
        print( "请求接口: <" + self.uninstallVirtualMachine.__doc__  + "> 用时：%s \n" %(res.elapsed.total_seconds()))
        self.resTime.put(res.elapsed.total_seconds())
        return res

    #更新云主机名称
    def updateCloudName(self):
        """更新云主机名称"""
        mid = ""
        url = self.myurl + "/nodes/" + mid + "/execute-resource-action"
        self.header['Content-Type'] = "application/json"
        data = {"executeParameters":{"displayName":"XXXXXXX"},"resourceActionId":"update_display_name"}
        res = requests.post(url, headers=self.header,data=json.dumps(data))
      #  print(res.text)
        print( "请求接口: <" + self.updateCloudName.__doc__  + "> 用时：%s \n" %(res.elapsed.total_seconds()))
        self.resTime.put(res.elapsed.total_seconds())
        return res

    #远程登录
    def remoteLogin(self):
        """远程登录"""
        url = self.myurl + "/nodes/" + id + "/consoleurl"
        res = requests.get(url, headers=self.header)
        print(self.header)
       # print(res.text)
        print( "请求接口: <" + self.remoteLogin.__doc__  + "> 用时：%s \n" %(res.elapsed.total_seconds()))
        self.resTime.put(res.elapsed.total_seconds())
        return res

    #挂模板
    def upTemplate(self):
        """挂模板"""
        system_id = ""
        url = self.myurl + "/logic-templates/" + system_id + "/physical-templates"
        self.header['Content-Type'] = "application/json"
        data = {
    "flavorId":None,
    "sshPort":22,
    "validateType":"password",
    "authSecretKey":None,
    "authSshSecretKey":None,
    "authPassword":None,
    "customSpecName":None,
    "snapshotMode":"normal",
    "default":False,
    "alias":"Li001",
    "cloudEntryId":"118b14a0-76e7-4c0b-b161-85024dd9c3db",
    "templateId":"ef7ff919-34d0-496e-bee2-cb56e5cca902",
    "customSpecType":None,
    "monitorPort":9100,
    "bootType":"volumeboot",
    "deleteOnTermination":False,
    "sshEnable":True,
    "sshUserName":"root",
    "sshPassword":"123456",
    "monitorMode":"remote",
    "agentMode":"remote"
}
        res = requests.get(url, headers=self.header,data=json.dumps(data))
      #  print(res.text)
        print( "请求接口: <" + self.upTemplate.__doc__  + "> 用时：%s \n" %(res.elapsed.total_seconds()))
        self.resTime.put(res.elapsed.total_seconds())
        return res


        """定时任务"""
        
    #云主机列表
    def cloudHostList(self):
        """云主机列表"""
        s = requests.Session()
        url = self.myurl + "/nodes/search?page=1&size=10000&sort=createdDate,desc"
        param = {}
        res = s.get(url, headers=self.header)
        print( "请求接口: <" + self.cloudHostList.__doc__  + "> 用时：%s \n" %(res.elapsed.total_seconds()))
        self.resTime.put(res.elapsed.total_seconds())
      #  print(res.text)
        return res

    #云主机详情
    def cloudHostInfo(self):
        """云主机详情"""
        s = requests.Session()
        url = self.myurl + "/nodes/" + self.hostId
        res = s.get(url, headers=self.header)
      #  print(res.text)
        print( "请求接口: <" + self.cloudHostInfo.__doc__  + "> 用时：%s \n" %(res.elapsed.total_seconds()))
        self.resTime.put(res.elapsed.total_seconds())
        return res

    #查询操作系统
    def queryOperatingSystem(self):
        """查询操作系统"""
        s = requests.Session()
        url = self.myurl + "/logic-templates/search?expand"
        res = s.get(url, headers=self.header)
       # print(res.text)
        print( "请求接口: <" + self.queryOperatingSystem.__doc__  + "> 用时：%s \n" %(res.elapsed.total_seconds()))
        self.resTime.put(res.elapsed.total_seconds())
        return res

    #查询公共模板
    def queryPublicTemplate(self):
        """查询公共模板"""
        systemid = "56668877-d775-4a7a-9f14-56203a218fc6"
        s = requests.Session()
        url = self.myurl + "/logic-templates/" + systemid + "/physical-templates?expand=&businessGroupId&resourceBundleId"
        res = s.get(url, headers=self.header)
       # print(res.text)
        print( "请求接口: <" + self.queryPublicTemplate.__doc__  + "> 用时：%s \n" %(res.elapsed.total_seconds()))
        self.resTime.put(res.elapsed.total_seconds())
        return res

    #查询网络
    def queryNetwork(self):
        """查询网络"""
        s = requests.Session()
        url = self.myurl + "/cloudprovider?action=queryCloudResource"
        self.header['Content-Type'] = "application/json"
        data = {"cloudResourceType":"cloudchef.openstack.nodes.Server::network"}
        res = s.post(url, headers=self.header, data=json.dumps(data))
      #  print(res.text)
        print( "请求接口: <" + self.queryNetwork.__doc__  + "> 用时：%s \n" %(res.elapsed.total_seconds()))
        self.resTime.put(res.elapsed.total_seconds())
        return res

    #查询子网
    def querySubnet(self):
        """查询子网"""
        s = requests.Session()
        url = self.myurl + "/cloudprovider?action=queryCloudResource"
        self.header['Content-Type'] = "application/json"
        data = {"cloudResourceType":"yacmp:cloudentry:type:openstack::network-subnet","queryProperties":{"networkIds":"925e8b4e-60f3-4663-a2b1-e687953c0473"}}
        res = s.post(url, headers=self.header, data=json.dumps(data))
     #   print(res.json())
        print( "请求接口: <" + self.querySubnet.__doc__  + "> 用时：%s \n" %(res.elapsed.total_seconds()))
        self.resTime.put(res.elapsed.total_seconds())
        return res

    #查询部署操作历史
    def queryDeployOpertingHistory(self):
        """查询部署操作历史"""
        did = self.deployId
        s = requests.Session()
        url =  "http://159.226.90.23/deployments/" + str(did) + "/tasks?page=1&size=10&sort=createdDate,desc"
        res = s.get(url, headers=self.header)
      #  print(res.text)
        print( "请求接口: <" + self.queryDeployOpertingHistory.__doc__  + "> 用时：%s \n" %(res.elapsed.total_seconds()))
        self.resTime.put(res.elapsed.total_seconds())
        return res

    #查询部署详情
    def queryDeployInfo(self):
        """查询部署详情"""
        did = self.deployId
        s = requests.Session()
        url =  "http://159.226.90.23/deployments/" + did + "/details"
        res = s.get(url, headers=self.header)
      #  print(res.text)
        print( "请求接口: <" + self.queryDeployInfo.__doc__  + "> 用时：%s \n" %(res.elapsed.total_seconds()))
        self.resTime.put(res.elapsed.total_seconds())
        return res

    def getMyCurl(self,testurl,myqueue,execsql,interface,conn,lock):
        c = pycurl.Curl()
        c.setopt(pycurl.URL, testurl)
        buf = BytesIO()
        c.setopt(c.WRITEDATA,buf)
        #允许跟踪来源
        #c.setopt(pycurl.FOLLOWLOCATION, 1)
        c.setopt(pycurl.CONNECTTIMEOUT, 60) #链接超时
        c.setopt(pycurl.TIMEOUT, 300) #下载超时
        c.setopt(pycurl.MAXREDIRS, 5)
        c.setopt(pycurl.HTTPHEADER, ['Cookie: JSESSIONID=%s'%self.mycookie])
        content = c.perform()#execute
        code = c.getinfo(c.HTTP_CODE)
        dns_time = c.getinfo(pycurl.NAMELOOKUP_TIME) #DNS time 域名解析时间
        conn_time = c.getinfo(pycurl.CONNECT_TIME)   #TCP/IP 3-way handshaking time
        starttransfer_time = c.getinfo(pycurl.STARTTRANSFER_TIME)  #time-to-first-byte time远程服务器连接时间
        con_start_data = c.getinfo(pycurl.PRETRANSFER_TIME) #连接上后到开始传输时的时间
        total_time = c.getinfo(pycurl.TOTAL_TIME)  #last requst time 请求总的时间
        updata = c.getinfo(pycurl.SIZE_UPLOAD) # 上传的数据大小
        downdata = c.getinfo(pycurl.SIZE_DOWNLOAD)  #下载的数据大小
        data = {'dns_time':dns_time, 'conn_time':conn_time, 'con_start_data':con_start_data,'total_time':total_time,'updata':updata,'downdata':downdata}
        #data = {'DNS解析时间':round(Decimal(dns_time),8), '连接服务器时间':conn_time,'开始传输数据时间':con_start_data,'请求总时间':total_time,}
        c.close()
        sql = "insert into qianyun(dns_time,conn_time,startData_time,total_time,content,insertTime,updata,downdata,code) value({0},{1},{2},{3},'{4}','{5}',{6},{7},{8})".format(data['dns_time'],data['conn_time'],data['con_start_data'],data['total_time'],interface,datetime.now().strftime("%m-%d %H:%M:%S.%f"),round(data['updata']/1024.0,2),round(data['downdata']/1024.0),code)
        lock.acquire()
        mysql = con.cursor()
        mysql.execute(sql)        
        con.commit()
        lock.release()
        mysql.close()
        #print(data)
        #myqueue.put(data)
        # print(page)
        return None

        
    def postMyCurl(self,testurl,myqueue,execsql,interface,conn,lock,testdata):
        c = pycurl.Curl()
        c.setopt(pycurl.URL, testurl)
        buf = BytesIO()
        c.setopt(c.WRITEDATA,buf)
        #允许跟踪来源
        #c.setopt(pycurl.FOLLOWLOCATION, 1)
        c.setopt(pycurl.CONNECTTIMEOUT, 60) #链接超时
        c.setopt(pycurl.TIMEOUT, 300) #下载超时
        c.setopt(pycurl.MAXREDIRS, 5)
        c.setopt(pycurl.HTTPHEADER, ['Cookie: JSESSIONID=%s'%self.mycookie,'Content-Type: application/json'])
        c.setopt(pycurl.POSTFIELDS, json.dumps((testdata)))
        content = c.perform()
        code = c.getinfo(c.HTTP_CODE)#execute 
        dns_time = c.getinfo(pycurl.NAMELOOKUP_TIME) #DNS time 域名解析时间
        conn_time = c.getinfo(pycurl.CONNECT_TIME)   #TCP/IP 3-way handshaking time
        starttransfer_time = c.getinfo(pycurl.STARTTRANSFER_TIME)  #time-to-first-byte time远程服务器连接时间
        con_start_data = c.getinfo(pycurl.PRETRANSFER_TIME) #连接上后到开始传输时的时间
        total_time = c.getinfo(pycurl.TOTAL_TIME)  #last requst time 请求总的时间
        updata = c.getinfo(pycurl.SIZE_UPLOAD) # 上传的数据大小
        downdata = c.getinfo(pycurl.SIZE_DOWNLOAD)  #下载的数据大小
        data = {'dns_time':dns_time, 'conn_time':conn_time, 'con_start_data':con_start_data,'total_time':total_time,'updata':updata,'downdata':downdata}
        #data = {'DNS解析时间':round(Decimal(dns_time),8), '连接服务器时间':conn_time,'开始传输数据时间':con_start_data,'请求总时间':total_time,}
        c.close()
        sql = "insert into qianyun_post(dns_time,conn_time,startData_time,total_time,content,insertTime,updata,downdata,code) value({0},{1},{2},{3},'{4}','{5}',{6},{7},{8})".format(data['dns_time'],data['conn_time'],data['con_start_data'],data['total_time'],interface,datetime.now().strftime("%m-%d %H:%M:%S.%f"),round(data['updata']/1024.0,2),round(data['downdata']/1024.0),code)
        lock.acquire()
        mysql = con.cursor()
        mysql.execute(sql)        
        con.commit()
        lock.release()
        mysql.close()
        page = buf.getvalue()
        #print(data)
        #print(page)
        #myqueue.put(data)
        return None




def curlPerfthread(myfun,mydata,responTime,num=1):
    global iteration
    if num <1:
        return
    myll = []
    print("并发请求 %d 次"%num)
    threadpool = []
    sTime = time.strftime("%H:%M:%S",time.localtime())
    for j in range(iteration):
        for i in range(num):
            t1 = Thread(target=fun)
            threadpool.append(t1)
            t1.start()
        for j in threadpool:
            j.join()
    print(">" * 33)
    for i in range(responTime.qsize()):
        myll.append(responTime.get(i))
    eTime = time.strftime("%H:%M:%S",time.localtime())
    print(myll)
    dnst = []
    connt = []
    starttransfert = []
    con_start_data = []
    totalt = []
    updata = []
    for i in myll:
        print(i)
        dnst.append(i['dns_time'])
        connt.append(i['updata'])
        starttransfert.append(i['starttransfer_time'])
        con_start_data.append(i['con_start_data'])
        totalt.append(i['total_time'])
    print(dnst,connt,totalt)

    pdplt = pd.DataFrame({"域名解析时间":updata})#"服务器连接时间":connt,"开始传输数据时间":starttransfert,"接收到第一个字节时间":con_start_data,"请求总时间":totalt})
    pdplt.plot()
    plt.tick_params(labelsize=8)
    plt.rcParams['font.sans-serif']=['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.xlabel("number")
    plt.ylabel('reponse time(sec)')
    plt.title("骞云接口%s -- %s"%(sTime,eTime))
    plt.show()
   # plt.savefig('qianyunImg/' + fun.__doc__ + time.strftime("%Y%m%d%H%M%S",time.localtime()))
    time.sleep(1)
    return None


def myCurl(ck):
    c = pycurl.Curl()
    c.setopt(pycurl.URL, "http://192.168.15.25/catalogs/published?page=1&size=1&sort=asc")
    buf = BytesIO()
    c.setopt(c.WRITEDATA,buf)
    #把cookie保存在该文件中
    #c.setopt(pycurl.COOKIEFILE, "cookie_file_name")
    #c.setopt(pycurl.COOKIEJAR, "cookie_file_name")
    #允许跟踪来源
    #c.setopt(pycurl.FOLLOWLOCATION, 1)
    c.setopt(pycurl.CONNECTTIMEOUT, 60) #链接超时
    c.setopt(pycurl.TIMEOUT, 300) #下载超时
    c.setopt(pycurl.MAXREDIRS, 5)
    #设置代理 如果有需要请去掉注释，并设置合适的参数
    #c.setopt(pycurl.PROXY, ‘http://11.11.11.11:8080′)
    #c.setopt(pycurl.PROXYUSERPWD, ‘aaa:aaa’)
    c.setopt(pycurl.HTTPHEADER, ['Cookie: JSESSIONID=A319AD24BA40FD93D99C130C4990E331'])
    #c.setopt(pycurl.POSTFIELDS,  data)
    content = c.perform()                        #execute 
    dns_time = c.getinfo(pycurl.NAMELOOKUP_TIME) #DNS time 域名解析时间
    conn_time = c.getinfo(pycurl.CONNECT_TIME)   #TCP/IP 3-way handshaking time
    starttransfer_time = c.getinfo(pycurl.STARTTRANSFER_TIME)  #time-to-first-byte time远程服务器连接时间
    con_start_data = c.getinfo(pycurl.PRETRANSFER_TIME) #连接上后到开始传输时的时间
    total_time = c.getinfo(pycurl.TOTAL_TIME)  #last requst time 请求总的时间
    updata = c.getinfo(pycurl.SIZE_UPLOAD) # 上传的数据大小
    downdata = c.getinfo(pycurl.SIZE_DOWNLOAD)  #下载的数据大小
    data = json.dumps({'dns_time':dns_time,         
                       'conn_time':conn_time,        
                       'starttransfer_time':starttransfer_time,    
                       'con_start_data':con_start_data,
                       'total_time':total_time,
                       'updata':updata,
                       'downdata':round(downdata/1024,2)})
    page = buf.getvalue()
    c.close()
   # print(data)
   # print(page)
    return data


    
if __name__=="__main__":
    con = pymysql.connect(host="10.0.117.65",user="root",passwd="root",db="portaltest",charset="utf8")
    cursor = con.cursor()
    responTime = queue.Queue()
    curlTime = queue.Queue()
    test = qianyun(responTime)
    hostId = "8a6251a4-6ba0-4012-b79b-e50f2db3ed01"
    cardId = "00f7031f-999a-4cbc-b711-dc99da83a087"
    system_id = "56668877-d775-4a7a-9f14-56203a218fc6"
    mid = "1"
    myurl = "http://192.168.15.25"
    getRequest = [{"url":myurl + "/catalogs/published?page=1&size=1&sort=asc","interface":"获取卡片列表"},
                  {"url":myurl + "/catalogs/" + cardId,"interface":"获取卡片详情"},
                  {"url":myurl + "/catalogs/" + cardId + "/inputs","interface":"获取卡片蓝图参数"},
                  {"url":myurl + "/nodes/8a6251a4-6ba0-4012-b79b-e50f2db3ed01/consoleurl","interface":"远程登录"},
                  {"url":myurl + "/logic-templates/" + system_id + "/physical-templates","interface":"挂模板"},
                  {"url":myurl + "/nodes/search?page=1&size=10000&sort=createdDate,desc","interface":"云主机列表"},
                  {"url":myurl + "/nodes/" + hostId,"interface":"云主机详情"},
                  {"url":myurl + "/logic-templates/search?expand","interface":"查询操作系统"},
                  {"url":myurl + "/logic-templates/" + system_id + "/physical-templates?expand=&businessGroupId&resourceBundleId","interface":"查询公共模板"}]
    '''
                  {"url":"http://159.226.90.23/deployments/" + did + "/tasks?page=1&size=10&sort=createdDate,desc"},
                  {"url":"http://159.226.90.23/deployments/" + did + "/details"}]
    '''
    vmname = "portal_" + time.strftime("%Y%m%d%H:%M:%S",time.localtime()) + str(random.randint(100,999))
    tempdata = '[{"Network_resource_id":"66ef2332-e812-4287-8c2e-f6738bb70e04","Server_server_logic_template_id":"56668877-d775-4a7a-9f14-56203a218fc6","Server_server_physical_template_id":"eb0c4619-dceb-496d-9448-6d1479b18b3d","Server_server_volume_type":"DS900_1_SSD","modify_pass_lin_root_pass":"Sugon123","Network_subnet_id":"6410fbdd-0319-40d5-a782-c02ff1d1d76d","Server_server_volume_size":100,"Server_flavor":"12","Server_server_vm_display_name":"%s"}]'%vmname
    applyhost = {
    "reason":"",
    "attachments":{

    },
    "kind":"PROVISION",
    "paramJson":tempdata,
    "count":1,
    "requestParameters":{
        "extensibleParameters":[
            {
            }
        ]
    },
    "ownerId":"sysadmin",
    "deploymentShutdownDuration":11052,
    "number":1,
    "nodes":[

    ],
    "businessGroupId":"0f975778-1d94-4b61-8d6c-f369356b2a39",
    "scheduleDate":None,
    "deploymentName":"",
    "deploymentTeardownDuration":7,
    "projectId":""
}
    postRequest = [{"url":myurl + "/cloudprovider?action=queryCloudResource","interface":"查询已有网络","data":{"businessGroupId":None,"cloudResourceType": "cloudchef.openstack.nodes.Server::network", "cloudEntryId": ""}},
                  {"url":myurl + "/cloudprovider?action=queryCloudResource","interface":"获取规格详情","data":{"cloudResourceType":"cloudchef.openstack.nodes.Server::flavor","queryProperties":{"physicalTemplateId":"","logicTemplateId":"","resourceBundleId":""}}},
                  {"url":myurl + "/cloudprovider?action=queryCloudResource","interface":"获取磁盘类型列表","data":{"cloudResourceType":"yacmp:cloudentry:type:openstack::volume-type"}},
                  {"url":myurl + "/catalogs/provision/deployment/" + cardId,"interface":"申请虚机","data":applyhost},
                  {"url":myurl + "/nodes/" + hostId + "/execute-resource-action","interface":"重置密码","data":{"resourceActionId":"reset_password","executeParameters":{"username":"gege123","newPassword":"123456"}}},
                  {"url":myurl + "/nodes/execute-action","interface":"虚机关机","data":{hostId:{"operationName":"stop","scheduledTime":None}}},
                  {"url":myurl + "/nodes/execute-action","interface":"虚机开机","data":{hostId:{"operationName":"start","scheduledTime":None}}},
                  {"url":myurl + "/nodes/" + hostId + "/execute-resource-action","interface":"虚机重启","data":{"resourceActionId":"reboot","scheduledTime":None}},
                  {"url":myurl + "/deployments/execute-action","interface":"虚机卸载","data":{"XXXXXX(deploymentd)":{"operationName":"Tear Down","scheduledTime":None,"operationParamJson":"{}"}}},
                  {"url":myurl + "/nodes/" + mid + "/execute-resource-action","interface":"更新云主机名称","data":{"executeParameters":{"displayName":"XXXXXXX"},"resourceActionId":"update_display_name"}},
                  {"url":myurl + "/cloudprovider?action=queryCloudResource","interface":"查询网络","data":{"cloudResourceType":"cloudchef.openstack.nodes.Server::network"}},
                  {"url":myurl + "/cloudprovider?action=queryCloudResource","interface":"查询子网","data":{"cloudResourceType":"yacmp:cloudentry:type:openstack::network-subnet","queryProperties":{"networkIds":"925e8b4e-60f3-4663-a2b1-e687953c0473"}}}]

    threadPool = []
    lock = Lock()
    threadTotal = 1  
    iterative = 1
    #get
    for k in range(0):
        for i in getRequest:
            for j in range(threadTotal):
                print(j,i,k)
                t = Thread(target=test.getMyCurl,args=(i['url'],curlTime,cursor,i['interface'],con,lock))
                threadPool.append(t)
                t.start()
            for k in threadPool:
                k.join()
        time.sleep(60)

    #post
    for k in range(iterative):
        for i in postRequest:
            for j in range(threadTotal):
                print(j,i,k)
                t = Thread(target=test.postMyCurl,args=(i['url'],curlTime,cursor,i['interface'],con,lock,i['data']))
                threadPool.append(t)
                t.start()
            for k in threadPool:
                k.join()
        time.sleep(60)
    con.close()       

   # myCurl(test.queryCardList._url)
    data = {"businessGroupId":None, "cloudResourceType": "cloudchef.openstack.nodes.Server::network", "cloudEntryId": ""}
    url = "http://192.168.15.25/cloudprovider?action=queryCloudResource"

