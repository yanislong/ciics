#!/usr/bin/env python3

import json, time, re, sys, os
import pymysql
import requests
from bs4 import BeautifulSoup
sys.path.append(os.getcwd() + '/run_test/integrateTest/user')
import userLogin

def test(name):
    global author
    account = name
    passwd = "123456aA"
    ug = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"
    url = "http://24mail.chacuo.net/zhtw"
    header = {}
    header['User-Agent'] = ug
    #请求临时邮箱,获取当前邮箱地址,和cookie
    r = requests.get(url, headers=header)
#    print(r.text)
#    print(r.headers['Set-Cookie'])
    l1 = re.compile(r'sid=(.*)$')
    l2 = l1.findall(r.headers['Set-Cookie'])
    token = l2[0]
#    print(token)
    html = BeautifulSoup(r.content, features='lxml')
#    print(html)
    tmp = str(html.input['value'])
    email = tmp + "@chacuo.net"
    print(email)
    eurl = "http://11.2.77.3/portal-test/user/account/system/add"
    addheader = {}
    addheader['Content-Type'] = "application/json"
    addheader['Authorization'] = author
    param = {
	"account": account,
	"departmentId": 17,
	"email": email,
	"name": "绝世美女Carry全场" + str(account),
	"roleId": 10
   }
    #添加系统用户成功后,重置密码
    res = requests.post(eurl, headers=addheader, data=json.dumps(param))
    try:
        print(res.json())
#        print(res.json()['code'])
#        con = pymysql.connect("192.168.15.21","root","Test~107443","j_portal")
#        cursor = con.cursor()
#        sql = "select id from user where account='{0}'".format(account)
#        cursor.execute(sql)
#        tmpid = cursor.fetchone()
#        print(tmpid[0])
        uu = "http://11.2.77.3/portal-test/user/account/system/reset"
        pp = {}
#        pp['id'] = tmpid[0]
#        uu2 = requests.post(uu, headers=addheader, params=pp)
#        print('重置密码')
#        print(uu2.text)
    except KeyError:
        print('失败')
        sys.exit()
    #如果邮箱验证码发送成功,获取临时邮箱中的验证码
    if res.json()['code'] == 200:
        time.sleep(5)
        reheader = {}
        reheader['User-Agent'] = ug
        reheader['X-Requested-With'] = "XMLHttpRequest"
        reheader['Cookie'] = "sid=" + token
        regurl = "http://11.2.77.3/portal-test/user/reg/email/add"
        eparam = {}
        eparam['data'] = tmp
        eparam['type'] = "refresh"
        eparam['arg'] = ""
        regheader = {}
        #循环10次,每次间隔10秒,如果仍没有获取就退出
        for i in range(10):
            time.sleep(10)
            eres = requests.post(url, headers=reheader, params=eparam)
#            print(eres.text)
            if  eres.json()['data'][0]['list']:
                mid = eres.json()['data'][0]['list'][0]['MID']
#                print(mid)
                cparam = {}
                cparam['data'] = tmp
                cparam['type'] = "mailinfo"
                cparam['arg'] = "f=" + str(mid)
                code = requests.post(url, headers=reheader, params=cparam) 
#                print(code.text)
                print(code.json()['data'][0][1][0]['DATA'])
                cc = code.json()['data'][0][1][0]['DATA'][0]
                ehtml = BeautifulSoup(cc, features='lxml')
                #获取到的密码
                ccd = ehtml.find_all('span')[1]
                ccd = ccd.get_text()
                print(ccd)
                print(account)
                mtoken = userLogin.userlogin().accountLogin(account,ccd)
                print(mtoken)
                lasturl = "http://11.2.77.3/portal-test/user/person/update/pwd"
                lastheader = {}
                lastheader['Content-Type'] = "application/json"
                lastheader['Authorization'] = mtoken
                lastdata = {}
                lastdata["password"] = ccd
                lastdata["newPassword"] = passwd
                lastdata["confirmNewPassword"] = passwd
                lastres = requests.post(lasturl, headers=lastheader, data=json.dumps(lastdata))
                print(lastres.text)
                print('success')
                break

if __name__ == "__main__":
    name = "yanqi0"
    author = "49db7f4c-4c69-48d9-9b82-f200bc53e2ec"
    for i in range(10,25):
        test(name + str(i))
