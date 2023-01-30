#!/usr/bin/env python3

import requests
import json

'''
测试安全组被绑定在哪个云主机上
需要手动获取token值
'''

token = "7b5f2600-8048-4178-b5b4-ab01e85d9cdc"

def sechost(sid):
    global token
    url = "https://console.casjc.com/portal/cloud/securitygroup/getSecurityGroupByHostId?times=1614742004267&serverId=" + sid
    header = {}
    header['Token'] = token
    r = requests.get(url, headers=header)
    #print(r.json['data'])
    for i in r.json()['data']:
        if i['securityName'] == "xxxx":
            print(i['securityId'])
            print(i['securityName'])
            print("#" * 10)

def gethost():
    global token
    url = "https://console.casjc.com/portal/cloud/host/getHostList"
    header = {}
    header['Token'] = token
    header['Content-Type'] = "application/json"
    data =  {"areaId":1,"endTime":"","imageName":"","ip":"","name":"","pageNum":1,"pageSize":30,"serverId":"","hostAccounts":"","status":"ACTIVE"}
    r = requests.post(url, headers=header, data=json.dumps(data))
    for i in r.json()['data']['list']:
        #print(i['serverId'])
        sechost(i['serverId'])

#sechost()
gethost()
