#!/usr/bin/env python3

import requests
import json, os
import sys
sys.path.append(os.getcwd() + '/../../../')
sys.path.append(os.getcwd() + '/../../lhlmysql')
sys.path.append(os.getcwd() + '/run_test/lhlmysql')

from lhlsql import lhlSql, portalSql
import config

class userlogin():

    def __init__(self):
        self.sqldata = lhlSql()
        self.portalsql = portalSql()
        self.postheader = {}
        self.postheader['Content-Type'] = "application/json"
        self.account = config.useaccount
        self.mobile = config.mobile
        self.url = config.userurl
        pass

    def accountLogin(self, username=config.useaccount, passwd=config.passwd):
        """使用已注册账号进行登录"""

        mokuai = "用户登录"
        data = {}
        data['password'] = passwd
        data['account'] = username
        data['rememberMe'] = True
        data['origin'] = 1
        url = self.url + "/login/account"
        res = requests.post(url, headers=self.postheader, data=json.dumps(data))
        print(res.text)
        if res.json()['code'] == 200:
            result = "Success"
        else:
            result = "Faile"
        if __name__ == "__main__":
            self.sqldata.insertInterfaceRespond(mokuai, url, json.dumps(data), res.text, res.status_code, round(res.elapsed.total_seconds(),5), self.accountLogin.__doc__, result)
        return res.json()['data']

    def wpassLogin(self):
        """使用正确账号与错误密码进行登录"""

        mokuai = "用户登录"
        passwd = "11111111"
        data = {}
        data['password'] = passwd
        data['rememberMe'] = True
        url = self.url + "/login/account"
        print(url)
        for j in self.account.keys():
            data['account'] = j
            res = requests.post(url, headers=self.postheader, data=json.dumps(data))
            print(res.text)
            if res.json()['code'] != 200:
               result = "Success"
            else:
               result = "Faile"
            self.sqldata.insertInterfaceRespond(mokuai, url, json.dumps(data), res.text, res.status_code, round(res.elapsed.total_seconds(),5), self.wpassLogin.__doc__, result)
        return res.json()['data']

if __name__ == "__main__":
    runtest = userlogin()
    #runtest.accountLogin(config.useaccount,config.passwd)
    runtest.accountLogin("tmp007","YzAyMTgyMT")
    #runtest.wpassLogin()
