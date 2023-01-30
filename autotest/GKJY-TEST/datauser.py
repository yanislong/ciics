#!/usr/bin/env python3

import requests
import json, time, re, sys
from bs4 import BeautifulSoup

def test(name):
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
    eurl = "http://11.2.77.3/portal-test/user/reg/email/code"
    param = {}
    param['email'] = email
    param['account'] = account
    #请求发送邮箱获取验证码
    res = requests.post(eurl, params=param)
    try:
        res.text
        print(res.json()['code'])
    except KeyError:
        print('发送验证码失败')
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
                print(mid)
                cparam = {}
                cparam['data'] = tmp
                cparam['type'] = "mailinfo"
                cparam['arg'] = "f=" + str(mid)
                code = requests.post(url, headers=reheader, params=cparam) 
#                print(code.text)
#                print(code.json()['data'][0][1][0]['DATA'])
                cc = code.json()['data'][0][1][0]['DATA'][0]
                ehtml = BeautifulSoup(cc, features='lxml')
                #获取到的验证码
                ccd = ehtml.find_all('span')[1]
                ccd = ccd.get_text()
                print(ccd)
                regheader['User-Agent'] = ug
                regheader['Content-Type'] = "application/json"
                data = {}
                data['account'] = account
                data['email'] = email
                data['code'] = str(ccd)
                data['password'] = passwd
                #请求邮箱注册接口,进行用户注册
                result = requests.post(regurl, headers=regheader, data=json.dumps(data))
                print(result.text)
                break

if __name__ == "__main__":
    name = "Sugon00"
    for i in range(10,100):
        test(name + str(i))
