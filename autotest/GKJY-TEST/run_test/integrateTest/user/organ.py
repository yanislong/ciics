#!/usr/bin/env python3

import requests
import json
import sys, os
sys.path.append(os.getcwd() + '/../../lhlmysql')
sys.path.append(os.getcwd() + '/../../../')

from lhlsql import lhlSql, portalSql
import config
import userLogin

class org():

    def __init__(self):
        self.sqldata = lhlSql()
        self.portalsql = portalSql()
        self.postheader = {}
        self.postheader['Authorization'] = userLogin.userlogin().accountLogin()
        self.postheader['Content-Type'] = "application/json"
        self.url = config.userurl + "/department"
        pass

    def addorg(self):
        """添加组织机构"""

        ii = {"id":4,"no":"ABCD","name":"国科晋云","level":1,"sort":1,"parentId":0,"leaf":0,"leaderId":10013,"userIds":None}
        mokuai = "组织机构"
        data = {}
       # data["id"] = 0
        data["leaderId"] = "10014"
        data["leaf"] = 0
        data["level"] = 1
        data["no"] = "20191209"
        data["name"] = "20191209组织机构"
        data["parentId"] = 0
        data["sort"] = 0
        data["userIds"] = None
        url = self.url + "/add"
        res = requests.post(url, headers=self.postheader, data=json.dumps(data))
        print(res.text)
        print(res.url)
        try:
            if res.json()['code'] == 200:
                result = "Success"
            else:
                result = "Faile"
        except KeyError:
            result = "Error"
        self.sqldata.insertInterfaceRespond(mokuai, url, json.dumps(data), res.text, res.status_code, round(res.elapsed.total_seconds(),5), self.addorg.__doc__, result)
        return None

    def orgupdate(self):
        """修改组织机构"""

        mokuai = "组织机构"
        data = {}
        data["leaderId"] = "1"
        data["leaf"] = 0
        data["level"] = "1"
        data["no"] = 1
        data["name"] = "1"
        data["parentId"] = "1"
        data["sort"] = 0
        data["id"] = 1
        data["userIds"] = 1
        url = self.url + "/update"
        res = requests.post(url, headers=self.postheader, data=json.dumps(data))
        print(res.text)
        print(res.url)
        try:
            if res.json()['code'] == 200:
                result = "Success"
            else:
                result = "Faile"
        except KeyError:
            result = "Error"
        self.sqldata.insertInterfaceRespond(mokuai, url, json.dumps(data), res.text, res.status_code, round(res.elapsed.total_seconds(),5), self.orgupdate.__doc__, result)
        return None

    def orgrd(self):
        """组织机构授权"""

        mokuai = "组织机构"
        data = {}
        data["rids"] = "1"
        data["id"] = 1
        url = self.url + "/addrd"
        res = requests.post(url, headers=self.postheader, params=data)
        print(res.text)
        print(res.url)
        try:
            if res.json()['code'] == 200:
                result = "Success"
            else:
                result = "Faile"
        except KeyError:
            result = "Error"
        self.sqldata.insertInterfaceRespond(mokuai, url, json.dumps(data), res.text, res.status_code, round(res.elapsed.total_seconds(),5), self.orgrd.__doc__, result)
        return None

    def delorg(self):
        """删除组织机构"""

        mokuai = "组织机构"
        data = {}
        data["id"] = 1
        url = self.url + "/del"
        res = requests.post(url, headers=self.postheader, params=data)
        print(res.text)
        print(res.url)
        try:
            if res.json()['code'] == 200:
                result = "Success"
            else:
                result = "Faile"
        except KeyError:
            result = "Error"
        self.sqldata.insertInterfaceRespond(mokuai, url, json.dumps(data), res.text, res.status_code, round(res.elapsed.total_seconds(),5), self.delorg.__doc__, result)
        return None

    def orgmode(self):
        """获取组织机构权限"""

        mokuai = "组织机构"
        data = {}
        data["id"] = 1
        url = self.url + "/hasmods"
        res = requests.post(url, headers=self.postheader, params=data)
        print(res.text)
        print(res.url)
        try:
            if res.json()['code'] == 200:
                result = "Success"
            else:
                result = "Faile"
        except KeyError:
            result = "Error"
        self.sqldata.insertInterfaceRespond(mokuai, url, json.dumps(data), res.text, res.status_code, round(res.elapsed.total_seconds(),5), self.orgmode.__doc__, result)
        return None

    def orglist(self):
        """分页获取组织机构"""

        mokuai = "组织机构"
        data = {}
        data["id"] = ""
        data["name"] = ""
        data["pageNum"] = 1
        url = self.url + "/list"
        res = requests.post(url, headers=self.postheader, data=json.dumps(data))
        print(res.text)
        print(res.url)
        try:
            if res.json()['code'] == 200:
                result = "Success"
            else:
                result = "Faile"
        except KeyError:
            result = "Error"
        self.sqldata.insertInterfaceRespond(mokuai, url, json.dumps(data), res.text, res.status_code, round(res.elapsed.total_seconds(),5), self.orglist.__doc__, result)
        return None

    def orgno(self):
        """检查组织机构编号是否存在"""

        mokuai = "组织机构"
        data = {}
        data["no"] = 1
        url = self.url + "/no"
        res = requests.post(url, headers=self.postheader, params=data)
        print(res.text)
        print(res.url)
        try:
            if res.json()['code'] == 200:
                result = "Success"
            else:
                result = "Faile"
        except KeyError:
            result = "Error"
        self.sqldata.insertInterfaceRespond(mokuai, url, json.dumps(data), res.text, res.status_code, round(res.elapsed.total_seconds(),5), self.orgno.__doc__, result)
        return None

    def orgparent(self):
        """获取所有上级组织机构"""

        mokuai = "组织机构"
        data = {}
        data["level"] = 1
        url = self.url + "/parent"
        res = requests.post(url, headers=self.postheader, params=data)
        print(res.text)
        print(res.url)
        try:
            if res.json()['code'] == 200:
                result = "Success"
            else:
                result = "Faile"
        except KeyError:
            result = "Error"
        self.sqldata.insertInterfaceRespond(mokuai, url, json.dumps(data), res.text, res.status_code, round(res.elapsed.total_seconds(),5), self.orgparent.__doc__, result)
        return None

    def orgperm(self):
        """获取全部数据权限"""

        mokuai = "组织机构"
        data = {}
        url = self.url + "/perms"
        res = requests.get(url, headers=self.postheader)
        print(res.text)
        print(res.url)
        try:
            if res.json()['code'] == 200:
                result = "Success"
            else:
                result = "Faile"
        except KeyError:
            result = "Error"
        self.sqldata.insertInterfaceRespond(mokuai, url, json.dumps(data), res.text, res.status_code, round(res.elapsed.total_seconds(),5), self.orgperm.__doc__, result)
        return None

    def orgtree(self):
        """获取全部组织机构树"""

        mokuai = "组织机构"
        data = {}
        url = self.url + "/tree"
        res = requests.get(url, headers=self.postheader)
        print(res.text)
        print(res.url)
        try:
            if res.json()['code'] == 200:
                result = "Success"
            else:
                result = "Faile"
        except KeyError:
            result = "Error"
        self.sqldata.insertInterfaceRespond(mokuai, url, json.dumps(data), res.text, res.status_code, round(res.elapsed.total_seconds(),5), self.orgtree.__doc__, result)
        return None

    def orgrename(self):
        """重命名组织机构"""

        mokuai = "组织机构"
        data = {}
        data["id"] = 1
        data["departmentName"] = 1
        url = self.url + "/rename"
        res = requests.post(url, headers=self.postheader, params=data)
        print(res.text)
        print(res.url)
        try:
            if res.json()['code'] == 200:
                result = "Success"
            else:
                result = "Faile"
        except KeyError:
            result = "Error"
        self.sqldata.insertInterfaceRespond(mokuai, url, json.dumps(data), res.text, res.status_code, round(res.elapsed.total_seconds(),5), self.orgrename.__doc__, result)
        return None


if __name__ == "__main__":
    runtest = org()
    runtest.addorg()
#    runtest.orgupdate()
#    runtest.orgrd()
#    runtest.delorg()
#    runtest.orgmode()
#    runtest.orglist()
#    runtest.orgno()
#    runtest.orgparent()
#    runtest.orgperm()
    runtest.orgtree()
#    runtest.orgrename()
