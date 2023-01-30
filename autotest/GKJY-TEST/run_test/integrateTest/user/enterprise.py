#!/usr/bin/env python3

import requests
import json
import sys, os
sys.path.append(os.getcwd() + '/../../lhlmysql')
sys.path.append(os.getcwd() + '/../../../')

from lhlsql import lhlSql, portalSql
import config
import userLogin

class enterprise():

    def __init__(self):
        self.sqldata = lhlSql()
        self.portalsql = portalSql()
        self.postheader = {}
        self.postheader['Authorization'] = userLogin.userlogin().accountLogin()
        self.postheader['Content-Type'] = "application/json"
        self.url = config.userurl + "/account/enterprise"
        pass

    def adduser(self):
        """添加企业用户"""

        mokuai = "企业用户管理"
        data = {}
        data["account"] = "1"
        data["companyId"] = 0
        data["email"] = "1"
        data["id"] = 0
        data["mobilePhone"] = "1"
        data["name"] = "1"
        data["roleId"] = 0
        url = self.url + "/add"
        res = requests.post(url, headers=self.postheader)
        print(res.text)
        print(res.url)
        try:
            if res.json()['code'] == 200:
                result = "Success"
            else:
                result = "Faile"
        except KeyError:
            result = "Error"
        self.sqldata.insertInterfaceRespond(mokuai, url, json.dumps(data), res.text, res.status_code, round(res.elapsed.total_seconds(),5), self.adduser.__doc__, result)
        return None


if __name__ == "__main__":
    runtest = enterprise()
    runtest.adduser()
