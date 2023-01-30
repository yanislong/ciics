#!/usr/bin/env python3

import json, time
import pymysql

import ciics_log
import front_mail
import front_config

def checkResult(jres=""):
    try:
        jres2 = json.dumps(jres)
        if not isinstance(jres,dict):
            ciics_log.logging.info('数据格式有误，不是json类型')
            return False
    except:
        ciics_log.logging.info('数据格式有误，不是json类型')
    if 'result' in jres.keys():
        if jres['result'] == "OK":
            ciics_log.logging.info('请求响应成功')
        else:
            ciics_log.logging.info('请求响应失败:\t')
            ciics_log.logging.info(jres)
    else:
        ciics_log.logging.info('响应的json不含有result,无法判断响应结果')

def insertShellRespond(con, iname, iaddr, irequestparam, irespondbody, icode, irespondtime, descp):
    """向interfaceRespond表中插入数据"""
    if icode == 200:
        result = "Success"
    else:
        result = "Error"
        for i in front_config.maillist:
            front_mail.sendMail(i,"http://10.9.19.179:8888/shelllog")
    checkResult(irespondbody)
    rbody = json.dumps(irespondbody,ensure_ascii=False)
    rdata = json.dumps(irequestparam,ensure_ascii=False)
    cursor = con.cursor()
    tt = time.strftime("%Y/%m/%d %H:%M:%S")
    sql = "insert into shellRespond(intername,interaddr,requestparam,respondbody,code,respondtime,inputtime,descp, result) value('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}')".format(iname,pymysql.escape_string(iaddr),pymysql.escape_string(rdata),pymysql.escape_string(rbody),icode,irespondtime,tt,descp,result)
    cursor.execute(sql)
    con.commit()
    cursor.close()
    return None

if __name__ == "__main__":
    checkResult()
