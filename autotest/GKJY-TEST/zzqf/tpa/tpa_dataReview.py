#!/usr/bin/env python3

import json
import requests
import tpa_login, ciics_log

def returnDispatch():
    global url
    header = {}
    header['Authorization'] = token
    header['Content-Type'] = "application/json"
    mydata = {}
    mydata["conclusion"] = "审核错误"
    mydata["comment"] = "审核人员看错了"
    mydata["caseNos"] = "GCO310000180P"
    mydata["isNeedAdjustment"] = False
    r = requests.post(url, headers=header, data=json.dumps(mydata))
    print(r.json())
    if r.json()['code'] != 0:
        ciics_log.logging.info("🐷" * 50)
        ciics_log.logging.info("请求失败")
        ciics_log.logging.info("请求参数:")
        ciics_log.logging.info(mydata)
        ciics_log.logging.info("请求响应:")
        ciics_log.logging.info(r.json())
        ciics_log.logging.info("🐷" * 50)
    else:
        ciics_log.logging.info("请求成功")
        ciics_log.logging.info("请求参数:")
        ciics_log.logging.info(mydata)
        ciics_log.logging.info("请求响应:")
        ciics_log.logging.info(r.json())
    ciics_log.logging.info("-" * 80)

if __name__ == "__main__":
    ciics_log.logging.info("########### 脚本开始执行 #############\n")
    url = "http://sittpapc.ciics.cn/tpaserver/tclaimcase/returnDispatch"
    ciics_log.logging.info("请求接口地址: " + url + "\n")
    token = tpa_login.login()
    returnDispatch()
    ciics_log.logging.info("########### 脚本执行结束 #############")
