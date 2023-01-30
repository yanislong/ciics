#!/usr/bin/env python3

import requests
import hashlib
import json, time, random
import sys, os
import threading
sys.path.append(os.getcwd() + '/../../lhlmysql')
sys.path.append(os.getcwd() + '/../../../')
print(sys.path)

from lhlsql import lhlSql, portalSql
import config

class userregist():

    def __init__(self):
        self.sqldata = lhlSql()
        self.portalsql = portalSql()
        self.postheader = {}
        self.postheader['Content-Type'] = "application/json"
        self.account = config.account
        self.mobile = config.mobile
        self.noAccount = config.noAccount
        self.passwd = config.passwd
        self.url = config.userurl
        pass

    def phoneRegist(self):
        """使用合法账号名进行注册"""

        tmp = []
        mokuai = "用户注册"
        for ll in range(len(self.account)):
            tmp.append((self.account[ll],self.mobile[ll]))
        url = self.url + "/reg/mobile/add"
        data = {}
        data['password'] = self.passwd
        for i in [1]:
#            acc = requests.post(config.userurl + "/reg/exist/account?account=" + str(i[0]))
#            print(acc.text)
#            if acc.json()['data'] == True:
#                self.portalsql.delUser(str(i[0]))
#            pho = requests.post(config.userurl + "/reg/exist/mobile?mobile=" + str(i[1]))
#            print(pho.text)
#            if pho.json()['data'] == True:
#                self.portalsql.delUser(str(i[1]))
#            code = requests.post(config.userurl + "/reg/sms/code?mobile=" + str(i[1]))
#            print(code.text)
#            tmp = code.json()['data']
#            data['code'] = tmp
            data['account'] = str(random.choice("abcdefghi")) + "13141032576"#str(i[0])
            data['mobilePhone'] = "13141032576"#str(i[1])
            for i in range(1):
                data['code'] = 280339
#                print(data)
                reg = requests.post(url, headers=self.postheader, data=json.dumps(data))
                print(reg.text)
                if reg.json()['code'] == 200:
#                    print(i)
                    print(reg.text)
                    break
            if reg.json()['code'] == 200:
               result = "Success"
            else:
               result = "Faile"
            self.sqldata.insertInterfaceRespond(mokuai, url, json.dumps(data), reg.text, reg.status_code, round(reg.elapsed.total_seconds(),5), self.phoneRegist.__doc__, result)
        return None

    def illegalAccountRegist(self):
        """使用非法账户名进行注册"""

        mokuai = "用户注册"
        url = self.url + "/reg/mobile/add"
        data = {}
        data['password'] = self.passwd
        for i in self.noAccount:
            data['account'] = i
            mobile = "1381234" + str(random.randint(1000,9999))
            data['mobilePhone'] = mobile
            code = requests.post(url + "/reg/sms/code?mobile=" + mobile)
#            print(code.text)
            tmp = code.json()['data']
            data['code'] = tmp
#            print(data)
            reg = requests.post(url, headers=self.postheader, data=json.dumps(data))
            print(reg.text)
            if reg.json()['code'] != 200:
               result = "Success"
            else:
               result = "Faile"
            self.sqldata.insertInterfaceRespond(mokuai, url, json.dumps(data), reg.text, reg.status_code, round(reg.elapsed.total_seconds(),5), self.illegalAccountRegist.__doc__, result)
        return None

if __name__ == "__main__":
    runtest = userregist()
    #runtest.phoneRegist()
    #runtest.illegalAccountRegist()
    for i in range(1):
        t = threading.Thread(target=runtest.phoneRegist)
        t.start()
