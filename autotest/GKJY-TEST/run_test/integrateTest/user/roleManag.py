#!/usr/bin/env python3

import requests
import threading
import json
import sys, os
sys.path.append(os.getcwd() + '/../../lhlmysql')
sys.path.append(os.getcwd() + '/../../../')

from lhlsql import lhlSql, portalSql
import config
import userLogin

class roleManag():

    def __init__(self):
        self.sqldata = lhlSql()
        self.portalsql = portalSql()
        self.session = userLogin.userlogin()
        self.postheader = {}
        self.postheader['Content-Type'] = "application/json"
        self.postheader['Authorization'] = self.session.accountLogin()
        self.url = config.userurl
        pass

    def addrole(self):
        """使用合法角色名称添加新角色"""

        mokuai = "添加角色"
        roleName = ["中國石油化工集團公司中國石油化工集團公司中國石油化工集團公司"] #["系统管理员","企业管理员","销售经理","销售总监","财务经理","法务经理","总经理","商务经理","运营管理员","企业用户","个人用户"]
        param = {}
        for j in roleName:
            param['roleName'] = j
            url = self.url + "/role/add"
            res = requests.post(url, headers=self.postheader, params=param)
            print(res.text)
            if res.json()['code'] == 200:
               result = "Success"
            else:
               result = "Faile"
            self.sqldata.insertInterfaceRespond(mokuai, url, json.dumps(param), res.text, res.status_code, round(res.elapsed.total_seconds(),5), self.addrole.__doc__, result)
        return None

    def waddrole(self):
        """使用非法角色名称添加新角色"""

        mokuai = "添加角色"
        roleName = ["中國石油化工集團公司中國石油化工集團公司中國石油化工集團公司中",""," ",None] #["系统管理员","企业管理员","销售经理","销售总监","财务经理","法务经理","总经理","商务经理","运营管理员","企业用户","个人用户"]
        param = {}
        for j in roleName:
            param['roleName'] = j
            url = self.url + "/role/add"
            res = requests.post(url, headers=self.postheader, params=param)
            print(res.text)
            if res.json()['code'] != 200:
               result = "Success"
            else:
               result = "Faile"
            self.sqldata.insertInterfaceRespond(mokuai, url, json.dumps(param), res.text, res.status_code, round(res.elapsed.total_seconds(),5), self.waddrole.__doc__, result)
        return None

    def getallrole(self):
        """查看系统中所有角色"""

        mokuai = "获取全部启用角色"
        url = self.url + "/role/all"
        param = {}
        res = requests.get(url, headers=self.postheader)
        print(res.text)
        if res.json()['code'] == 200:
           result = "Success"
        else:
           result = "Faile"
        self.sqldata.insertInterfaceRespond(mokuai, url, json.dumps(param), res.text, res.status_code, round(res.elapsed.total_seconds(),5), self.getallrole.__doc__, result)
        return None

    def checkrole(self):
        """检查已成功添加的角色名称是否存在"""

        mokuai = "检查角色名称是否存在"
        roleName = ["系统管理员","企业管理员","销售经理","销售总监","财务经理","法务经理","总经理","商务经理","运营管理员","企业用户","个人用户"]
        param = {}
        for j in roleName:
            param['name'] = j
            url = self.url + "/role/exist"
            res = requests.post(url, headers=self.postheader, params=param)
            print(res.text)
            if res.json()['code'] == 200:
               result = "Success"
            else:
               result = "Faile"
            self.sqldata.insertInterfaceRespond(mokuai, url, json.dumps(param), res.text, res.status_code, round(res.elapsed.total_seconds(),5), self.checkrole.__doc__, result)
        return None

    def listrole(self):
        """分页获取角色"""

        mokuai = "分页获取角色"
        roleName = ["系统管理员"]
        param = {}
        param['pageNum'] = "0"
        param['roleName'] = ""
        url = self.url + "/role/list"
        res = requests.post(url, headers=self.postheader, params=param)
        print(res.text)
        if res.json()['code'] == 200:
           result = "Success"
        else:
           result = "Faile"
        self.sqldata.insertInterfaceRespond(mokuai, url, json.dumps(param), res.text, res.status_code, round(res.elapsed.total_seconds(),5), self.checkrole.__doc__, result)
        return None

    def updaterole(self):
        """修改角色名称"""

        mokuai = "修改角色"
        roleName = ["游戏GM01","神","0","中科曙光Casjc1中科曙光Casjc1中科曙光Casjc1","个\n人 用\t户","中國石油化工集團公司中國石油化工集團公司中國石油化工集團公司"]
        param = {}
        for j in roleName:
            param['name'] = j
            param['id'] = "14"
            url = self.url + "/role/update"
            res = requests.post(url, headers=self.postheader, params=param)
            print(res.text)
            if res.json()['code'] == 200:
               result = "Success"
            else:
               result = "Faile"
            self.sqldata.insertInterfaceRespond(mokuai, url, json.dumps(param), res.text, res.status_code, round(res.elapsed.total_seconds(),5), self.updaterole.__doc__, result)
        return None

    def wupdaterole(self):
        """修改非法角色名称"""

        mokuai = "修改角色"
        roleName = [""," ",None,"中科曙光Casjc1中科曙光Casjc1中科曙光Casjc10","\n\t"]
        param = {}
        for j in roleName:
            param['name'] = j
            param['id'] = "14"
            url = self.url + "/role/update"
            res = requests.post(url, headers=self.postheader, params=param)
            print(res.text)
            if res.json()['code'] != 200:
               result = "Success"
            else:
               result = "Faile"
            self.sqldata.insertInterfaceRespond(mokuai, url, json.dumps(param), res.text, res.status_code, round(res.elapsed.total_seconds(),5), self.wupdaterole.__doc__, result)
        return None


    def enablerole(self):
        """启用角色"""

        mokuai = "角色启用和禁用"
        myid = ["14"]
        param = {}
        for j in myid:
            param['id'] = j
            url = self.url + "/role/enable"
            res = requests.post(url, headers=self.postheader, params=param)
            print(res.text)
            if res.json()['code'] == 200:
               result = "Success"
            else:
               result = "Faile"
            self.sqldata.insertInterfaceRespond(mokuai, url, json.dumps(param), res.text, res.status_code, round(res.elapsed.total_seconds(),5), self.enablerole.__doc__, result)
        return None

    def permrole(self):
        """角色授权"""

        mokuai = "角色授予权限"
        myid = ["14"]
        param = {}
        for j in myid:
            param['id'] = j
            param['mids'] = "1"
            url = self.url + "/role/addrm"
            res = requests.post(url, headers=self.postheader, params=param)
            print(res.text)
            if res.json()['code'] == 200:
               result = "Success"
            else:
               result = "Faile"
            self.sqldata.insertInterfaceRespond(mokuai, url, json.dumps(param), res.text, res.status_code, round(res.elapsed.total_seconds(),5), self.permrole.__doc__, result)
        return None


    def permmanag(self):
        """获取全部启用权限"""

        mokuai = "权限管理"
        param = {}
        url = self.url + "/module/list"
        res = requests.get(url, headers=self.postheader)
        print(res.text)
        if res.json()['code'] == 200:
           result = "Success"
        else:
           result = "Faile"
        self.sqldata.insertInterfaceRespond(mokuai, url, json.dumps(param), res.text, res.status_code, round(res.elapsed.total_seconds(),5), self.permmanag.__doc__, result)
        return None

if __name__ == "__main__":
    runtest = roleManag()
#    runtest.addrole()
#    runtest.waddrole()
#    runtest.updaterole()
#    runtest.wupdaterole()
    runtest.getallrole()
#    runtest.checkrole()
#    runtest.listrole()
#    runtest.enablerole()
#    runtest.permrole()
#    runtest.permmanag()

    tmp = []
    for i in range(0):
        t = threading.Thread(target=runtest.addrole)
        tmp.append(t)
        t.start()
    for j in tmp:
        j.join()
