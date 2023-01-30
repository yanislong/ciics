#!/usr/bin/env python3

import requests
import time
import re
import json
import logging
import queue

import config

LOG_FORMAT= "%(asctime)s %(levelname)s %(message)s" 
DATE_FORMAT = "%Y-%m-%d %H:%M:%S %a" 
FNAME = time.strftime("%Y-%m-%d#%H-%M-%S",time.localtime()) 
logging.basicConfig(level=logging.DEBUG,format=LOG_FORMAT,datefmt=DATE_FORMAT,filename='./log/' + FNAME + '.log') 

def login():
    global u
    url = "http://" + config.testdata['u'] + "/portal/new/login"
    header = {}
    data = {}
    data['username'] = config.testdata['username']
    data['password'] = config.testdata['passwd']
    res = requests.post(url, headers=header, data=data)
    l1 = re.compile('token":"(.*?)"')
    l2 = l1.findall(res.text)
    return l2[0]

def modifyUserInfo(tempnum=None,cname=None):
    url = "http://" + config.testdata['u1'] + "/portal/user/sysUserUpdate"
    header = {}
    header['Cookie'] = "JSESSIONID="
    header["Content-Type"] = "application/json;charset=UTF-8"
    data = {}
    data["id"] = "10111"
    data["account"] = "gege123"
    data["name"] = ""
    data["kjyPassport"] = ""
    data["email"] = ""
    data["userType"] = "0"
    data["phone"] = ""
    data["companyId"] = "1"
    data["roleId"] = "2"
    data["firstLogin"] = "1"
    res = requests.get(url, headers=header, data=json.dumps(data))
#    print(res.content)
    sec = res.elapsed.total_seconds()
    tempnum.put([sec,cname])
    tempnum.task_done()
    logging.debug(str(res.status_code) + res.text + str(res.elapsed.total_seconds()))
    return sec

if __name__ == "__main__":
    modifyUserInfo()
