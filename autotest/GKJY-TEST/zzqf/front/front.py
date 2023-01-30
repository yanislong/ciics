#!/usr/bin/env python3

import time, json
import requests
import pymysql

import front_config
import front_mode
import front_mail
import ciics_log

def activityList():
    global token
    title = "活动类型列表接口"
    des = "test"
    url = front_config.global_url + "front/bulk/sd-bulk-service-type/getActivityList"
    header = {}
    header['Cookie'] = "TOKEN=" + token
    data = {}
    r = requests.get(url, headers=header)
    print(r.json())
    front_mode.checkResult(r.json())
    ciics_log.logging.info(r.json())
    front_mode.insertShellRespond(con,title,url,data,r.json(),r.status_code,r.elapsed.total_seconds(),des)
    return None

def serverTypeList():
    global token
    title = "服务包列表"
    des = "test"
    url = front_config.global_url + "front/front/bulk/sd-bulk-service-pack/getBulkTypeList"
    header = {}
    header['Cookie'] = "TOKEN=" + token
    data = {}
    data['serverType'] = 0
    r = requests.get(url, headers=header, params=data)
    print(r.json())
    front_mode.checkResult(r.json())
    ciics_log.logging.info(r.json())
    front_mode.insertShellRespond(con,title,url,data,r.json(),r.status_code,r.elapsed.total_seconds(),des)
    return None

def supplierList():
    global token
    title = "供应商列表"
    des = "test"
    url = front_config.global_url + "front/front/bulk/sd-medical-institution/getMedicalInstitutions"
    header = {}
    header['Cookie'] = "TOKEN=" + token
    data = {}
    data['serverType'] = 0
    data['packId'] = "849598448171745280"
    r = requests.get(url, headers=header, params=data)
    print(r.json())
    front_mode.checkResult(r.json())
    ciics_log.logging.info(r.json())
    front_mode.insertShellRespond(con,title,url,data,r.json(),r.status_code,r.elapsed.total_seconds(),des)
    return None

if __name__ == "__main__":
    ciics_log.logging.info("########### 脚本开始执行 #############")
    con = pymysql.connect(front_config.mysql_host,front_config.mysqluser,front_config.mysqlpasswd, 'portaltest', charset="utf8mb4")
    token = ""
    #activityList()
    #serverTypeList()
    supplierList()
    con.close()
    ciics_log.logging.info("########### 脚本执行结束 #############")
