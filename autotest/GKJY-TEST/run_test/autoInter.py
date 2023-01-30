#!/usr/bin/env python3

import requests
import sys, json, re
import os

sys.path.append(os.getcwd() + '/integrateTest')
sys.path.append(os.getcwd() + '/integrateTest/user')
sys.path.append(os.getcwd() + '/run_test/integrateTest/user')
sys.path.append(os.getcwd())

import userLogin
from lhlmysql.lhlsql import lhlSql
import config

class lhl:
    
    def __init__(self):
        if config.authorized == True:
            try:
                pass
                #self.session = userLogin.userlogin().accountLogin(config.useaccount,config.passwd)
            except requests.exceptions.ConnectionError:
                self.session = ""
                print('没有身份认证信息')
        else:
            self.session = ""
        self.timeout = 12
        self.testurl = config.testurl
        self.getheader = {}
        self.getheader['Authorization'] = self.session
        self.postheader_json = {}
        self.postheader_json['Authorization'] = self.session 
        self.postheader_json['Content-Type'] = "application/json"
        self.postheader_www = {}
        self.postheader_www['Authorization'] = self.session 
        self.postheader_www['Content-Type'] = "application/x-www-form-urlencoded"
        pass

    def respondGet(self, result_code, url, header="", param="", upwd=None):
        """
        请求时需要4个参数, 预期的响应code, 完整url, 请求header,请求参数, 测试账号密码
        函数返回一个字典{'body': , 'respondTime':, 'code':}
        """
        #判断是否提供了测试用的用户名和密码，如果没有提供则使用默认账号，如果提供有误则没有身份认证信息
        self.getheader['Authorization'] = self.session
        if upwd:
            try:
                upwd = json.loads(upwd)
                try:
                    testsession = userLogin.userlogin().accountLogin(upwd['username'],upwd['passwd'])
                    self.getheader['Authorization'] = testsession
                except requests.exceptions.ConnectionError:
                    self.getheader['Authorization'] = ""
                except KeyError:
                    self.getheader['Authorization'] = ""
            except json.decoder.JSONDecodeError:
                self.getheader['Authorization'] = ""
        s = requests.session()
        if not self.__analysisUrl(url):
            return None
        try:
            param = json.loads(param)
        except json.decoder.JSONDecodeError:
            param = {}
        if not isinstance(param, dict):
            print('get请求的参数格式有误')
            param = {}
        try:
            res = s.get(url, headers=self.getheader, params=param, timeout=self.timeout)
        except requests.exceptions.ConnectionError:
            print("请求URL无法连接")
            return None
#        print(res.status_code)
#        print(res.url)
#        print(res.text)
        #判断是否给了预期的code,如果没有结果为None
        if result_code:
            #如果code为200,判断响应json中的code是否和预期的值相等,如果解析json失败返回Error
            if res.status_code == 200:
                try:
                    if str(res.json()['code']) == str(result_code.strip()):
                        result = 'Success'
                    else:
                        result = 'Faile'
                except json.decoder.JSONDecodeError:
                    result = 'Faile'
                except KeyError:
                    result = 'Faile'
            #如果响应的code不是200
            else:
                 #判断预期的code与服务端的响应code是否相等,相等也认定为成功,不相等返回Error
                if str(res.status_code) == str(result_code.strip()):
                    result = 'Success'
                else:
                    result = 'Error'
        else:
            result = "None"
       # print(res.text.encode('utf-8').decode('utf-8'),res.elapsed.total_seconds(),res.status_code)
        rep = {'body': res.text, 'respondTime':res.elapsed.total_seconds(), 'code':res.status_code, 'result':result}
        return rep
   
    def respondPost(self, result_code, url, header="", data={}, upwd=None):
        """
        请求时需要4个参数，预期的响应code, 完整url，请求header,请求参数
        函数返回一个字典{'body': , 'respondTime':, 'code':}
        """
        #判断是否提供了测试用的用户名和密码，如果没有提供则使用默认账号，如果提供有误则没有身份认证信息
        self.postheader_json['Authorization'] = self.session
        self.postheader_www['Authorization'] = self.session
        if not upwd:
            try:
                upwd = json.loads(upwd)
                try:
                    testsession = userLogin.userlogin().accountLogin(upwd['username'],upwd['passwd'])
                    self.postheader_json['Authorization'] = testsession
                    self.postheader_www['Authorization'] = testsession
                except requests.exceptions.ConnectionError:
                    self.postheader_json['Authorization'] = ""
                    self.postheader_www['Authorization'] = ""
                except KeyError:
                    self.postheader_json['Authorization'] = ""
                    self.postheader_www['Authorization'] = ""
            except json.decoder.JSONDecodeError:
                self.postheader_json['Authorization'] = ""
                self.postheader_www['Authorization'] = ""
        try:
            data = json.loads(data)
        except json.decoder.JSONDecodeError:
            data = {}
        if not isinstance(data, dict):
            print('post请求的数据格式有误')
            param = {}
        s = requests.session()
        if header.strip() == "json":
            try:
                res = s.post(url, headers=self.postheader_json, data=json.dumps(data), timeout=self.timeout)
                print(url,self.postheader_json,data)
            except requests.exceptions.MissingSchema:
                print('请求的Url地址有误')
                return None
            except requests.exceptions.ConnectionError:
                print("请求URL无法连接")
                return None
#            print(res.url)
#            print(data)
            print(res.text,res.elapsed.total_seconds(),res.status_code)
        else:
            try:
                print('nojson')
                res = s.post(url, headers=self.postheader_www, data=data, timeout=self.timeout)
            except requests.exceptions.MissingSchema:
                print('请求的Url地址有误')
                return None
            except requests.exceptions.ConnectionError:
                print("请求URL无法连接")
                return None
#            print(res.url)
#            print(data)
#            print(res.text,res.elapsed.total_seconds(),res.status_code)
        #判断是否给了预期的code,如果没有结果为None
        if result_code:
            #如果code为200,判断响应json中的code是否和预期的值相等,如果解析json失败返回Error
            if res.status_code == 200:
                try:
                    if str(res.json()['code']) == str(result_code.strip()):
                        result = 'Success'
                    else:
                        result = 'Faile'
                except json.decoder.JSONDecodeError:
                    result = 'Error'
                except KeyError:
                    result = 'Error'
            #如果响应的code不是200
            else:
                 #判断预期的code与服务端的响应code是否相等,相等也认定为成功,不相等返回Error
                if str(res.status_code) == str(result_code.strip()):
                    result = 'Success'
                else:
                    result = 'Error'
        else:
            result = "None"
        rep = {'body': res.text, 'respondTime':res.elapsed.total_seconds(), 'code':res.status_code, 'result':result}
        return rep

    def respondPut(self, url, header="", data={}, upwd=None):
        """
        请求时需要3个参数，预期的响应code, 完整url，请求header,请求参数
        函数返回一个字典{'body': , 'respondTime':, 'code':}
        """
        #判断是否提供了测试用的用户名和密码，如果没有提供则使用默认账号，如果提供有误则没有身份认证信息
        self.postheader_json['Authorization'] = self.session
        self.postheader_www['Authorization'] = self.session
        if upwd:
            try:
                upwd = json.loads(upwd)
                try:
                    testsession = userLogin.userlogin().accountLogin(upwd['username'],upwd['passwd'])
                    self.postheader_json['Authorization'] = testsession
                    self.postheader_www['Authorization'] = testsession
                except requests.exceptions.ConnectionError:
                    self.postheader_www['Authorization'] = ""
                    self.postheader_json['Authorization'] = ""
                except KeyError:
                    self.postheader_json['Authorization'] = ""
                    self.postheader_www['Authorization'] = ""
            except json.decoder.JSONDecodeError:
                self.postheader_www['Authorization'] = ""
                self.postheader_json['Authorization'] = ""
        s = requests.session()
        self.pheader['Cookie'] = header
        try:
            res = s.get(url, headers=self.pheader, data=data, timeout=self.timeout)
        except requests.exceptions.MissingSchema:
            print('请求的Url地址有误')
            return None
        except requests.exceptions.ConnectionError:
            print("请求URL无法连接")
            return None
       # print(res.text.encode('utf-8').decode('utf-8'),res.elapsed.total_seconds(),res.status_code)
       #判断是否给了预期的code,如果没有结果为None
        if result_code:
            #如果code为200,判断响应json中的code是否和预期的值相等,如果解析json失败返回Error
            if res.status_code == 200:
                try:
                    if str(res.json()['code']) == str(result_code.strip()):
                        result = 'Success'
                    else:
                        result = 'Faile'
                except json.decoder.JSONDecodeError:
                    result = 'Error'
                except KeyError:
                    result = 'Error'
            #如果响应的code不是200
            else:
                 #判断预期的code与服务端的响应code是否相等,相等也认定为成功,不相等返回Error
                if str(res.status_code) == str(result_code.strip()):
                    result = 'Success'
                else:
                    result = 'Error'
        else:
            result = "None"

    def __analysisUrl(self,myurl):
        """url规则: 只有字母和数字[0-9a-zA-Z]、一些特殊符号"$-_.+!*'(),"[不包括双引号]、
        以及某些保留字，才可以不经过编码直接用于URL。"""
        l1 = re.compile('^https?:/{2}[0-9a-zA-Z$-_.+!*$&?]+$')
        l2 = l1.findall(myurl)
        l3 = re.match('^https?:/{2}[0-9a-zA-Z$-_.+!*$:/]+', myurl)
        if l3:
            return True
        else: 
            print("url格式有误")
            return None

    def runTest(self):
        sqldata = lhlSql()
        mydata = sqldata.getAllInterface()
        for i in mydata:
            l1 = re.compile('http://(.*?)/')
            l2 = l1.findall(i[2])
            if l2 == None or l2 =="" or l2==[]:
                l3 = i[2]
                print('url没有替换')
            else:
                l3 = i[2].replace(l2[0], self.testurl)
    #        print(l3)
    #        print(i)
            if i[5].lower() == "get":
                resGet = self.respondGet(i[8],l3.strip(),i[3],i[4],i[9])
                if resGet:
                    sqldata.insertInterfaceRespond(i[1],l3,i[4],resGet['body'],resGet['code'],round(resGet['respondTime'],5),i[7],resGet['result'])
                else:
                    sqldata.insertInterfaceRespond(i[1],l3,i[4],resGet['body'],resGet['code'],round(0),i[7],'Error')
            elif i[5].lower() == "post":
                resPost = self.respondPost(i[8],l3.strip(),i[3],i[4],i[9])
                if resPost:
                    sqldata.insertInterfaceRespond(i[1],l3,i[4],resPost['body'],resPost['code'],round(resPost['respondTime'],5),i[7],resPost['result'])
                else:
                    sqldata.insertInterfaceRespond(i[1],l3,i[4],resGet['body'],resGet['code'],round(0),i[7],'Error')
            elif i[5].lower() == "put":
                resPut = self.respondPut(l3.strip(),i[3],i[4],i[9])
                if resPut:
                    sqldata.insertInterfaceRespond(i[1],l3,i[4],resPost['body'],resPost['code'],round(resPost['respondTime'],5),i[7])
                else:
                    sqldata.insertInterfaceRespond(i[1],l3,i[4],resGet['body'],resGet['code'],round(0),i[7],'Error')
            else:
                print("请求方式或参数有误不存在")
        return None

    def oneTest(self,rid):
        sqldata = lhlSql()
        #rid = "7634"
        onedata = sqldata.getIdInterface(rid)
        for i in onedata:
            print(i)
            l1 = re.compile('http://(.*?)/')
            l2 = l1.findall(i[2])
            if l2 == None or l2=="" or l2==[]:
                l3 = i[2]
                print("url没有替换")
            else:    
                l3 = i[2].replace(l2[0], self.testurl)
            print(l3)
            if i[5].lower() == "get":
                resGet = self.respondGet(i[8],l3.strip(),i[3],i[4],i[9])
                if resGet:
                    sqldata.insertInterfaceRespond(i[1],l3,i[4],resGet['body'],resGet['code'],round(resGet['respondTime'],5),i[7],resGet['result'])
                else:
                    sqldata.insertInterfaceRespond(i[1],l3,i[4],'None','0',round(0),i[7],'Error')
            elif i[5].lower() == "post":
                print(i[5])
                resPost = self.respondPost(i[8],l3.strip(),i[3],i[4],i[9])
                if resPost:
                    sqldata.insertInterfaceRespond(i[1],l3,i[4],resPost['body'],resPost['code'],round(resPost['respondTime'],5),i[7],resPost['result'])
                else:
                    sqldata.insertInterfaceRespond(i[1],l3,i[4],'None','0',round(0),i[7],'Error')
            elif i[5].lower() == "put":
                resPut = self.respondPut(l3.strip(),i[3],i[4],i[9])
                if resPut:
                    sqldata.insertInterfaceRespond(i[1],l3,i[4],resPost['body'],resPost['code'],round(resPost['respondTime'],5),i[7])
                else:
                    sqldata.insertInterfaceRespond(i[1],l3,i[4],'None','0',round(0),i[7],'Error')
            else:
                print("请求方式或参数有误不存在")
        return None

if __name__ == "__main__":
    a = lhl()
    #a._lhl__analysisUrl("http://www.baidu.com:9090/123/abc")
    #a.runTest()
    a.oneTest("")
    pass
