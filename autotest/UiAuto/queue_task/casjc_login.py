#!/usr/bin/env python3

import requests
import json

import casjc_config
import casjc_log_task

def login(username=casjc_config.ausername,passwd=casjc_config.apasswd, loginType=1):

    """太原先计算云平台用户登录, """

    url = casjc_config.global_url + "/portal-test/user/login/account"
    data = {}
    data['account'] = username
    data['password'] = passwd
    data['origin'] = loginType
    data['rememberMe'] = False
    header = {}
    header['Content-Type'] = "application/json"
    r = requests.post(url, headers=header, data=json.dumps(data))
    #print(r.json())
    url2 = casjc_config.global_url + "/portal-test/user/person/get"
    header2 = {}
    header2['Token'] = r.json()['data']
    r2 = requests.get(url2, headers=header2)
    #print(r2.json())
    if loginType == 0:
        ltype = "控制台登录"
    elif loginType == 1:
        ltype = "管理后台登录"
    casjc_log_task.logging.info(login.__doc__ + ltype + " 登录账号:" + username + " 登录结果: " + json.dumps(r.json()))
    #返回登录用户的token, 用户Id, 企业Id
    return r.json()['data'], r2.json()['data']['id'], r2.json()['data']['companyId']


if __name__ == "__main__":
    login()
