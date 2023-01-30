#!/usr/bin/env python3

import requests
import threading
import json, sys, random, os
sys.path.append(os.getcwd() + '/../../lhlmysql')
sys.path.append(os.getcwd() + '/../../../')
sys.path.append(os.getcwd() + "/../user")

from lhlsql import lhlSql, portalSql
import config
import userLogin

class payCondition():

    def __init__(self):
        self.sqldata = lhlSql()
        self.portalsql = portalSql()
        self.session = userLogin.userlogin()
        self.postheader = {}
        self.postheader['Content-Type'] = "application/json"
        self.postheader['Authorization'] = self.session.accountLogin()
        self.url = config.contracturl
        pass

    def addcondition(self):
        """新增付款条件"""

        mokuai = "付款条件"
        roleName = ["中國石油化工集團公司中國石油化工集團公司中國石油化工集團公司"] 
        url = self.url + "/contractPayTerms/save"
        param = {}
        param["contractId"] = 0
        param["contractTemplateId"] = 0
        param["description"] = ""
        param["id"] = 0
        param["payPercentage"] = 0
        param["payTerms"] = ""
        param["payTermsTime"] = ""
        param["tag"] = ""
        param["termsPro"] = 0
        param["termsType"] = 0
        param["termsTypeName"] = ""
        for j in roleName:
            res = requests.post(url, headers=self.postheader, data=json.dumps(param))
            print(res.text)
            if res.json()['code'] == 200:
               result = "Success"
            else:
               result = "Faile"
            self.sqldata.insertInterfaceRespond(mokuai, url, json.dumps(param), res.text, res.status_code, round(res.elapsed.total_seconds(),5), self.addcondition.__doc__, result)
        return None

    def getorder(self):
        """我的申请单列表"""

        mokuai = "订单管理"
        roleName = ["中國石油化工集團公司中國石油化工集團公司中國石油化工集團公司"] 
        param = {}
        param['pageNum'] = "1"
        param['pageSize'] = "10"
        for j in roleName:
            url = self.url + "/order/myOrderList"
            res = requests.get(url, headers=self.postheader, params=param)
            print(res.url)
            print(res.text)
            if res.json()['code'] != 200:
               result = "Success"
            else:
               result = "Faile"
            self.sqldata.insertInterfaceRespond(mokuai, url, json.dumps(param), res.text, res.status_code, round(res.elapsed.total_seconds(),5), self.getorder.__doc__, result)
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
            url = self.url + "/account/update"
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
            url = self.url + "/account/update"
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
        url = self.url + "/account/get"
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

    def orderpaymanag(self):
        """根据订单号进行付款"""

        mokuai = "订单支付管理"
        url = self.url + "/pay/payOrder"
        param = {}
        param['orderId'] = ""
        param['payPrice'] = ""
        param['payTimes'] = ""
        res = requests.post(url, headers=self.postheader, data=json.dumps(param))
        print(res.text)
        try:
            if res.json()['code'] == 200:
               result = "Success"
            else:
               result = "Faile"
        except KeyError:
               result = "Error"
        self.sqldata.insertInterfaceRespond(mokuai, url, json.dumps(param), res.text, res.status_code, round(res.elapsed.total_seconds(),5), self.orderpaymanag.__doc__, result)
        return None

if __name__ == "__main__":
    runtest = payCondition()
    runtest.addcondition()
#    runtest.getorder()

    tmp = []
    for i in range(0):
        t = threading.Thread(target=runtest.addrole)
        tmp.append(t)
        t.start()
    for j in tmp:
        j.join()
