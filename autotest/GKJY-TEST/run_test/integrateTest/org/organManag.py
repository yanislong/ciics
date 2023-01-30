#!/usr/bin/env python3

import requests
import threading
import json
import sys, os
sys.path.append(os.getcwd() + '/../user')
sys.path.append(os.getcwd() + '/../../lhlmysql')
sys.path.append(os.getcwd() + '/../../../')

from lhlsql import lhlSql, portalSql
import config
import userLogin

class organManag():

    def __init__(self):
        self.sqldata = lhlSql()
        self.portalsql = portalSql()
        self.session = userLogin.userlogin()
        self.postheader = {}
        self.getheader = {}
        self.postheader['Content-Type'] = "application/json"
        self.getheader['Content-Type'] = "application/x-www-form-urlencoded;charset=UTF-8"
        self.postheader['Requested-With'] = "XMLHttpRequest"
        self.postheader['Authorization'] = self.session.accountLogin()
        self.url = config.orgurl + "/org"
        pass

    def addaddress(self):
        """添加邮寄地址"""

        mokuai = "组织管理"
        param = {}
        param['address'] = ""
        param['detailedAddress'] = ""
        param['mobile'] = ""
        param['address'] = ""
        param['orgName'] = ""
        param['userName'] = ""
        url = self.url + "/insertAddress"
        res = requests.post(url, headers=self.postheader, data=param)
        print(res.url)
        print(res.text)
        try:
            if res.json()['code'] == 200:
                result = "Success"
            else:
                result = "Faile"
        except KeyError:
            result = "Error"
        except json.decoder.JSONDecodeError:
            result = "Error"
        self.sqldata.insertInterfaceRespond(mokuai, url, json.dumps(param), res.text, res.status_code, round(res.elapsed.total_seconds(),5), self.addaddress.__doc__, result)
        return None

    def getaddress(self):
        """查询邮寄地址"""

        mokuai = "组织管理"
        param = {}
        param['limit'] = ""
        param['start'] = ""
        url = self.url + "/getAddressList"
        res = requests.post(url, headers=self.postheader, data=param)
        print(res.url)
        print(param)
        print(res.text)
        try:
            if res.json()['code'] != 200:
                result = "Success"
            else:
                result = "Faile"
        except KeyError:
            result = "Error"
        except json.decoder.JSONDecodeError:
            result = "Error"
        self.sqldata.insertInterfaceRespond(mokuai, url, json.dumps(param), res.text, res.status_code, round(res.elapsed.total_seconds(),5), self.getaddress.__doc__, result)
        return None

    def deladdress(self):
        """删除邮寄地址"""

        mokuai = "组织管理"
        param = {}
        param['id'] = ""
        url = self.url + "/deleteAddress"
        res = requests.get(url, headers=self.postheader, params=param)
        print(res.url)
        print(res.text)
        try:
            if res.json()['code'] != 200:
                result = "Success"
            else:
                result = "Faile"
        except KeyError:
                result = "Error"
        except json.decoder.JSONDecodeError:
            result = "Error"
        self.sqldata.insertInterfaceRespond(mokuai, url, json.dumps(param), res.text, res.status_code, round(res.elapsed.total_seconds(),5), self.deladdress.__doc__, result)
        return None

    def updateaddress(self):
        """更新邮寄地址"""

        mokuai = "组织管理"
        param = {}
        param['id'] = "1"
        param['address'] = ""
        param['detailedAddress'] = ""
        param['mobile'] = ""
        param['address'] = ""
        param['orgName'] = ""
        param['userName'] = ""
        url = self.url + "/updateAddress"
        res = requests.post(url, headers=self.postheader, data=param)
        print(res.url)
        print(param)
        print(res.text)
        try:
            if res.json()['code'] == 200:
                result = "Success"
            else:
                result = "Faile"
        except KeyError:
            result = "Error"
        except json.decoder.JSONDecodeError:
            result = "Error"
        self.sqldata.insertInterfaceRespond(mokuai, url, json.dumps(param), res.text, res.status_code, round(res.elapsed.total_seconds(),5), self.updateaddress.__doc__, result)
        return None

    def addorg(self):
        """添加组织机构"""

        mokuai = "组织管理"
        param = {}
        #联系人
        param['contacts'] = "梁雪峰"
        #法人
        param['legalPerson'] = "梁凯"
        param['mobile'] = "18911226966"
        param['orgAddress'] = "龙域中心A座"
        param['orgAccount'] = ""
        param['orgName'] = "龙行天下创世纪集团"
        param['orgEmail'] = "250@qq.com"
        userinfo = {"account": "","email": "","id": 0,"mobilePhone": "","originPassword": "","password": "","salt": ""}
        param['userDTOList'] = [userinfo]
        param['userId'] = ""
        param['userNumber'] = ""
        url = self.url + "/insertOrg"
        res = requests.post(url, headers=self.postheader, data=json.dumps(param))
        print(res.url)
        print(res.text)
        try:
            if res.json()['code'] == 200:
                result = "Success"
            else:
                result = "Faile"
        except KeyError:
            result = "Error"
        except json.decoder.JSONDecodeError:
            result = "Error"
        self.sqldata.insertInterfaceRespond(mokuai, url, json.dumps(param), res.text, res.status_code, round(res.elapsed.total_seconds(),5), self.addorg.__doc__, result)
        return None


    def getorg(self):
        """查询组织机构"""

        mokuai = "组织管理"
        param = {}
        param['limit'] = ""
        param['orgAddress'] = ""
        param['orgAccount'] = ""
        param['orgName'] = ""
        param['start'] = ""
        url = self.url + "/getOrgList"
        res = requests.post(url, headers=self.postheader, data=param)
        print(res.url)
        print(res.text)
        try:
            if res.json()['code'] == 200:
                result = "Success"
            else:
                result = "Faile"
        except KeyError:
            result = "Error"
        except json.decoder.JSONDecodeError:
            result = "Error"
        self.sqldata.insertInterfaceRespond(mokuai, url, json.dumps(param), res.text, res.status_code, round(res.elapsed.total_seconds(),5), self.getorg.__doc__, result)
        return None

    def getorginfo(self):
        """查询组织机构详情"""

        mokuai = "组织管理"
        param = {}
        param['orgId'] = "1"
        url = self.url + "/getOrgById"
        res = requests.get(url, headers=self.postheader, params=param)
        print(res.url)
        print(res.text)
        try:
            if res.json()['code'] == 200:
                result = "Success"
            else:
                result = "Faile"
        except KeyError:
            result = "Error"
        except json.decoder.JSONDecodeError:
            result = "Error"
        self.sqldata.insertInterfaceRespond(mokuai, url, json.dumps(param), res.text, res.status_code, round(res.elapsed.total_seconds(),5), self.getorginfo.__doc__, result)
        return None

if __name__ == "__main__":
    runtest = organManag()
#    runtest.addaddress()
#    runtest.getaddress()
#    runtest.deladdress()
#    runtest.updateaddress()
    runtest.addorg()
#    runtest.getorg()
#    runtest.getorginfo()

    tmp = []
    for i in range(0):
        t = threading.Thread(target=runtest.addrole)
        tmp.append(t)
        t.start()
    for j in tmp:
        j.join()
