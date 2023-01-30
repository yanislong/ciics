#!/usr/bin/env python3

import requests
import json
import sys, os
sys.path.append(os.getcwd() + '/../../lhlmysql')
sys.path.append(os.getcwd() + '/../../../')

from lhlsql import lhlSql, portalSql
import config
import userLogin

class personal():

    def __init__(self):
        self.sqldata = lhlSql()
        self.portalsql = portalSql()
        self.postheader = {}
        self.postheader['Authorization'] = userLogin.userlogin().accountLogin()
        self.postheader['Content-Type'] = "application/json"
        self.url = config.userurl
        pass

    def dataauthoriz(self):
        """获取登录人数据权限"""

        mokuai = "个人中心"
        data = {}
        url = self.url + "/person/data/rp"
        res = requests.post(url, headers=self.postheader)
        print(res.text)
        try:
            if res.json()['code'] == 200:
                result = "Success"
            else:
                result = "Faile"
        except KeyError:
            result = "Error"
        self.sqldata.insertInterfaceRespond(mokuai, url, json.dumps(data), res.text, res.status_code, round(res.elapsed.total_seconds(),5), self.dataauthoriz.__doc__, result)
        return None

    def personinfo(self):
        """获取当前登陆人信息"""

        mokuai = "个人中心"
        data = {}
        url = self.url + "/person/get"
        res = requests.get(url, headers=self.postheader)
        print(res.text)
        try:
            if res.json()['code'] == 200:
                result = "Success"
            else:
                result = "Faile"
        except KeyError:
            result = "Error"
        self.sqldata.insertInterfaceRespond(mokuai, url, json.dumps(data), res.text, res.status_code, round(res.elapsed.total_seconds(),5), self.personinfo.__doc__, result)
        return None

    def menuauthoriz(self):
        """获取登陆人功能权限"""

        mokuai = "个人中心"
        data = {}
        url = self.url + "/person/resource/rp"
        res = requests.post(url, headers=self.postheader)
        print(res.text)
        try:
            if res.json()['code'] == 200:
                result = "Success"
            else:
                result = "Faile"
        except KeyError:
            result = "Error"
        self.sqldata.insertInterfaceRespond(mokuai, url, json.dumps(data), res.text, res.status_code, round(res.elapsed.total_seconds(),5), self.menuauthoriz.__doc__, result)
        return None

    def updateemail(self):
        """修改邮箱"""

        mokuai = "个人中心"
        data = {}
        url = self.url + "/person/update/email"
        data['email'] = ""
        res = requests.post(url, headers=self.postheader, params=data)
        print(res.text)
        try:
            if res.json()['code'] == 200:
                result = "Success"
            else:
                result = "Faile"
        except KeyError:
            result = "Error"
        self.sqldata.insertInterfaceRespond(mokuai, url, json.dumps(data), res.text, res.status_code, round(res.elapsed.total_seconds(),5), self.updateemail.__doc__, result)
        return None

    def updateinterest(self):
        """修改研究方向"""

        mokuai = "个人中心"
        data = {}
        url = self.url + "/person/update/interest"
        data['interest'] = ""
        res = requests.post(url, headers=self.postheader, params=data)
        print(res.text)
        try:
            if res.json()['code'] == 200:
                result = "Success"
            else:
                result = "Faile"
        except KeyError:
            result = "Error"
        self.sqldata.insertInterfaceRespond(mokuai, url, json.dumps(data), res.text, res.status_code, round(res.elapsed.total_seconds(),5), self.updateinterest.__doc__, result)
        return None

    def updatemobile(self):
        """修改手机"""

        mokuai = "个人中心"
        data = {}
        url = self.url + "/person/update/mobile"
        data['mobilePhone'] = ""
        res = requests.post(url, headers=self.postheader, params=data)
        print(res.text)
        try:
            if res.json()['code'] == 200:
                result = "Success"
            else:
                result = "Faile"
        except KeyError:
            result = "Error"
        self.sqldata.insertInterfaceRespond(mokuai, url, json.dumps(data), res.text, res.status_code, round(res.elapsed.total_seconds(),5), self.updatemobile.__doc__, result)
        return None

    def updatephone(self):
        """修改联系电话"""

        mokuai = "个人中心"
        data = {}
        url = self.url + "/person/update/telephone"
        data['telephone'] = ""
        res = requests.post(url, headers=self.postheader, params=data)
        print(res.text)
        try:
            if res.json()['code'] == 200:
                result = "Success"
            else:
                result = "Faile"
        except KeyError:
            result = "Error"
        self.sqldata.insertInterfaceRespond(mokuai, url, json.dumps(data), res.text, res.status_code, round(res.elapsed.total_seconds(),5), self.updatephone.__doc__, result)
        return None

    def updateaddress(self):
        """修改联系地址"""

        mokuai = "个人中心"
        data = {}
        url = self.url + "/person/update/address"
        data['address'] = "a" * 300
        res = requests.post(url, headers=self.postheader, params=data)
        print(res.text)
        try:
            if res.json()['code'] == 200:
                result = "Success"
            else:
                result = "Faile"
        except KeyError:
            result = "Error"
        self.sqldata.insertInterfaceRespond(mokuai, url, json.dumps(data), res.text, res.status_code, round(res.elapsed.total_seconds(),5), self.updateaddress.__doc__, result)
        return None

    def updatepwd(self):
        """修改密码"""

        mokuai = "个人中心"
        data = {}
        url = self.url + "/person/update/pwd"
        data['confirmNewPassword'] = "12345678"
        data['newPassword'] = "12345678"
        data['password'] = "12345678"
        data['id'] = "10015"
        res = requests.post(url, headers=self.postheader, data=json.dumps(data))
        print(res.text)
        try:
            if res.json()['code'] == 200:
                result = "Success"
            else:
                result = "Faile"
        except KeyError:
            result = "Error"
        self.sqldata.insertInterfaceRespond(mokuai, url, json.dumps(data), res.text, res.status_code, round(res.elapsed.total_seconds(),5), self.updatepwd.__doc__, result)
        return None

if __name__ == "__main__":
    runtest = personal()
#    runtest.dataauthoriz()
    runtest.personinfo()
#    runtest.menuauthoriz()
#    runtest.updateemail()
#    runtest.updateinterest()
#    runtest.updatemobile()
#    runtest.updatephone()
#    runtest.updateaddress()
#    runtest.updatepwd()
