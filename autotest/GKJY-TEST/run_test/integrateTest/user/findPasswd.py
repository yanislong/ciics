#!/usr/bin/env python3

import requests
import hashlib
import json, time, random
import sys, os
sys.path.append(os.getcwd() + '/../../lhlmysql')
sys.path.append(os.getcwd() + '/../../../')

from lhlsql import lhlSql, portalSql
import config

class userFind():

    def __init__(self):
        self.sqldata = lhlSql()
        self.portalsql = portalSql()
        self.postheader = {}
        self.postheader['Content-Type'] = "application/json"
        self.url = config.userurl
        pass

    def phoneFind(self):
        """通过手机号修改密码"""

        mokuai = "找回密码"
        mobile = ["173444322202"]
        account = ["lizongwu"]
        url = self.url + "/forget/info"
        data = {}
        for i in account:
#            acc = requests.post(config.userurl + "/forget/info?account=" + i)
#            print(acc.text)
#            uid = acc.json()['data']['id']
#            htoken = acc.json()['data']['token']
#            self.postheader['Authorization'] = htoken
#            pho = requests.post(config.userurl + "/forget/code?id=" + str(uid), headers=self.postheader)
#            print(pho.text)
            isexists = requests.post(config.userurl + "/forget/code/isvalid?code=814495&id=" + str("10051"), headers=self.postheader)
            print(isexists.text)
#            code = requests.post(config.testurl + "/reg/sms/code?mobile=" + str(i[1]))
#            print(code.text)
#            data['mobilePhone'] = str(i[1])
  #          print(data)
#            reg = requests.post(url, headers=self.postheader, data=json.dumps(data))
#            print(reg.text)
#            if reg.json()['code'] == 200:
#               result = "Success"
#            else:
#               result = "Faile"
            self.sqldata.insertInterfaceRespond(mokuai, url, json.dumps(data), reg.text, reg.status_code, round(reg.elapsed.total_seconds(),5), self.phoneFind.__doc__, result)
        return None

if __name__ == "__main__":
    runtest = userFind()
    runtest.phoneFind()
