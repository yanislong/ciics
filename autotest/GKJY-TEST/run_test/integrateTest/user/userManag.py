#!/usr/bin/env python3

import requests
import threading
import json, sys, random, os
sys.path.append(os.getcwd() + '/../../lhlmysql')
sys.path.append(os.getcwd() + '/../../../')

from lhlsql import lhlSql, portalSql
import config
import userLogin

class userManag():

    def __init__(self):
        self.sqldata = lhlSql()
        self.portalsql = portalSql()
        self.session = userLogin.userlogin()
        self.postheader = {}
        self.postheader['Content-Type'] = "application/json"
        self.postheader['Authorization'] = self.session.accountLogin()
        self.url = config.userurl + "/account/system"
        pass

    def adduser(self):
        """使用合法数据添加新用户"""

        mokuai = "用户管理"
        roleName = ["中國石油化工集團公司中國石油化工集團公司中國石油化工集團公司"] 
        param = {}
        param['account'] = "abcdef"
        param['companyId'] = ""
        param['email'] = str(random.randint(1,100)) + "@qq.com"
        param['mobilePhone'] = "13112341235"
        param['name'] = "abc123"
        param['roleId'] = "16"
        for j in roleName:
            url = self.url + "/add"
            res = requests.post(url, headers=self.postheader, data=json.dumps(param))
            print(res.text)
            if res.json()['code'] == 200:
               result = "Success"
            else:
               result = "Faile"
            self.sqldata.insertInterfaceRespond(mokuai, url, json.dumps(param), res.text, res.status_code, round(res.elapsed.total_seconds(),5), self.adduser.__doc__, result)
        return None

    def wadduser(self):
        """使用非法数据添加新用户"""

        mokuai = "用户管理"
        roleName = ["中國石油化工集團公司中國石油化工集團公司中國石油化工集團公司"] 
        param = {}
        param['account'] = "0abcdef"
        param['companyId'] = "1"
        param['email'] = ""
        param['mobilePhone'] = ""
        param['name'] = "abc123"
        param['roleId'] = "16"
        for j in roleName:
            url = self.url + "/add"
            res = requests.post(url, headers=self.postheader, data=json.dumps(param))
            print(res.text)
            if res.json()['code'] != 200:
               result = "Success"
            else:
               result = "Faile"
            self.sqldata.insertInterfaceRespond(mokuai, url, json.dumps(param), res.text, res.status_code, round(res.elapsed.total_seconds(),5), self.wadduser.__doc__, result)
        return None

    def updateuser(self):
        """使用合法数据修改用户"""

        mokuai = "用户管理"
        roleName = ["中國石油化工集團公司中國石油化工集團公司中國石油化工集團公司"] 
        param = {}
        param['account'] = "LIZONGWU"
        param['companyId'] = "1"
        param['email'] = ""
        param['mobilePhone'] = ""
        param['name'] = "abc123"
        param['roleId'] = "16"
        param['id'] = "10012"
        for j in roleName:
            url = self.url + "/update"
            res = requests.post(url, headers=self.postheader, data=json.dumps(param))
            print(res.text)
            if res.json()['code'] == 200:
               result = "Success"
            else:
               result = "Faile"
            self.sqldata.insertInterfaceRespond(mokuai, url, json.dumps(param), res.text, res.status_code, round(res.elapsed.total_seconds(),5), self.updateuser.__doc__, result)
        return None

    def wupdateuser(self):
        """使用非法数据修改用户"""

        mokuai = "用户管理"
        roleName = ["中國石油化工集團公司中國石油化工集團公司中國石油化工集團公司"] 
        param = {}
        param['account'] = "0LIZONGWU"
        param['companyId'] = "1"
        param['email'] = "li@qq.com"
        param['mobilePhone'] = "13112341235"
        param['name'] = "杨广"
        param['roleId'] = "14"
        param['id'] = "10012"
        for j in roleName:
            url = self.url + "/update"
            res = requests.post(url, headers=self.postheader, data=json.dumps(param))
            print(res.text)
            if res.json()['code'] != 200:
               result = "Success"
            else:
               result = "Faile"
            self.sqldata.insertInterfaceRespond(mokuai, url, json.dumps(param), res.text, res.status_code, round(res.elapsed.total_seconds(),5), self.updateuser.__doc__, result)
        return None

    def getuser(self):
        """通过用户Id获取用户信息"""

        mokuai = "用户管理"
        url = self.url + "/get"
        mid = ["10012"] 
        param = {}
        for j in mid:
            param['id'] = j
            res = requests.post(url, headers=self.postheader, params=param)
            print(res.text)
            if res.json()['code'] == 200:
               result = "Success"
            else:
               result = "Faile"
            self.sqldata.insertInterfaceRespond(mokuai, url, json.dumps(param), res.text, res.status_code, round(res.elapsed.total_seconds(),5), self.getuser.__doc__, result)
        return None

    def getpageuser(self):
        """分页获取用户信息"""

        mokuai = "用户管理"
        url = self.url + "/list"
        mid = ["10012"] 
        param = {}
        param['account'] = "abc"
        param['companyName'] = ""
        param['name'] = ""
        param['pageNum'] = "0"
        param['roleName'] = ""
        param['status'] = ""
        for j in mid:
            res = requests.post(url, headers=self.postheader, data=json.dumps(param))
            print(res.text)
            if res.json()['code'] == 200:
               result = "Success"
            else:
               result = "Faile"
            self.sqldata.insertInterfaceRespond(mokuai, url, json.dumps(param), res.text, res.status_code, round(res.elapsed.total_seconds(),5), self.getpageuser.__doc__, result)
        return None

if __name__ == "__main__":
    runtest = userManag()
    runtest.adduser()
#    runtest.wadduser()
#    runtest.updateuser()
#    runtest.wupdateuser()
#    runtest.getuser()
#    runtest.getpageuser()

    tmp = []
    for i in range(0):
        t = threading.Thread(target=runtest.addrole)
        tmp.append(t)
        t.start()
    for j in tmp:
        j.join()
