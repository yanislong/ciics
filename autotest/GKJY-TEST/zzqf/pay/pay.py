#!/usr/bin/env python3

import time, json
import requests
import pymysql

import pay_login
import pay_config
import ciics_log
import pay_mode
import pay_mail

def getOrder():
    global token
    title = "查询所有订单"
    url = pay_config.global_url + "/o2ocheck/console/getAllOrder"
    header = {}
    header['Cookie'] = "TOKEN=" + token
    data = {}
    data['orderSn'] = ""
    data['phone'] = ""
    data['orderState'] = ""
    data['pageNum'] = "1"
    data['pageSize'] = "20"
    data['startTime'] = time.strftime("%Y-%m-%d 00:00:00",time.localtime())
    data['endTime'] = ""
    r = requests.post(url, headers=header, data=data)
    if r.status_code == 200:
        result = "Success"
    else:
        result = "Error"
        for i in pay_config.maillist:
            pay_mail.sendMail(i,"http://10.9.19.179:8888/shelllog")
    pay_mode.checkResult(r.json())
    ciics_log.logging.info(r.json())
    des = "test"
    rbody = json.dumps(r.json())
    rdata = json.dumps(data)
    pay_mode.insertShellRespond(con,title,url,rdata,rbody,r.status_code,r.elapsed.total_seconds(),des,result)
    #print(r.json())
    return None

def getShop():
    global token
    title = "查询所有商品"
    url = pay_config.global_url + "/o2ocheck/goods/goodsAll"
    header = {}
    header['Cookie'] = "TOKEN=" + token
    data = {}
    data['barCode'] = ""
    data['goodsNameCommon'] = ""
    data['goodsManufacturer'] = ""
    data['checkStatus'] = ""
    data['goodsApproval'] = ""
    data['goodsCode'] = ""
    data['medicineStatus'] = ""
    data['goodsShow'] = ""
    data['easyCode'] = ""
    data['pageNum'] = "1"
    data['pageSize'] = "20"
    r = requests.post(url, headers=header, data=data)
    pay_mode.checkResult(r.json())
    ciics_log.logging.info(r.json())
    #print(r.json())
    if r.status_code == 200:
        result = "Success"
    else:
        result = "Error"
        for i in pay_config.maillist:
            pay_mail.sendMail(i,"http://10.9.19.179:8888/shelllog")
    pay_mode.checkResult(r.json())
    ciics_log.logging.info(r.json())
    des = "test"
    rbody = json.dumps(r.json())
    rdata = json.dumps(data)
    pay_mode.insertShellRespond(con,title,url,rdata,rbody,r.status_code,r.elapsed.total_seconds(),des,result)
    return None

def getSales():
    global token
    title = "查询所有销售数据"
    url = pay_config.global_url + "/o2ocheck/financeManager/showtotal"
    header = {}
    header['Cookie'] = "TOKEN=" + token
    data = {}
    data['orderSn'] = ""
    data['phone'] = ""
    data['orderState'] = ""
    #data['createStart'] = "2021-08-26 00:00:00"
    data['createStart'] = time.strftime("%Y-%m-%d 00:00:00",time.localtime())
    data['createEnd'] = ""
    r = requests.post(url, headers=header, data=data)
    pay_mode.checkResult(r.json())
    ciics_log.logging.info(r.json())
    #print(r.json())
    if r.status_code == 200:
        result = "Success"
    else:
        result = "Error"
        for i in pay_config.maillist:
            pay_mail.sendMail(i,"http://10.9.19.179:8888/shelllog")
    pay_mode.checkResult(r.json())
    ciics_log.logging.info(r.json())
    des = "test"
    rbody = json.dumps(r.json())
    rdata = json.dumps(data)
    pay_mode.insertShellRespond(con,title,url,rdata,rbody,r.status_code,r.elapsed.total_seconds(),des,result)
    return None

def getCardList():
    global token
    title = "查询值付卡"
    url = pay_config.global_url + "/o2ocheck/console/getPayCardList"
    header = {}
    header['Cookie'] = "TOKEN=" + token
    data = {}
    data['payLogo'] = "8000001000075823"
    r = requests.post(url, headers=header, data=data)
    pay_mode.checkResult(r.json())
    ciics_log.logging.info(r.json())
    #print(r.json())
    cardNumber = r.json()['data'][0]['cardNumber']
    #print(cardNumber)
    if r.status_code == 200:
        result = "Success"
    else:
        result = "Error"
        for i in pay_config.maillist:
            pay_mail.sendMail(i,"http://10.9.19.179:8888/shelllog")
    pay_mode.checkResult(r.json())
    ciics_log.logging.info(r.json())
    des = "test"
    rbody = json.dumps(r.json())
    rdata = json.dumps(data)
    pay_mode.insertShellRespond(con,title,url,rdata,rbody,r.status_code,r.elapsed.total_seconds(),des,result)
    return cardNumber

def getUserCard(paycode="8000001000075823"):
    global token
    title = "查询值付卡所属用户信息"
    url = pay_config.global_url + "/o2ocheck/console/queryUserByPayCard"
    header = {}
    header['Cookie'] = "TOKEN=" + token
    data = {}
    data['payCardCode'] = paycode
    r = requests.post(url, headers=header, data=data)
    pay_mode.checkResult(r.json())
    ciics_log.logging.info(r.json())
    #print(r.json())
    memberId = r.json()['data']['memberId']
    payCode = r.json()['data']['accountNum']
    entId = r.json()['data']['enterpriseId']
    phone = r.json()['data']['memberMobile']
    payCardNumber = r.json()['data']['accountNum']
    #print(memberId, payCode, entId)
    #返回所属卡的用户id，卡id，手机号，企业id, payCardNumber
    if r.status_code == 200:
        result = "Success"
    else:
        result = "Error"
        for i in pay_config.maillist:
            pay_mail.sendMail(i,"http://10.9.19.179:8888/shelllog")
    pay_mode.checkResult(r.json())
    ciics_log.logging.info(r.json())
    des = "test"
    rbody = json.dumps(r.json())
    rdata = json.dumps(data)
    pay_mode.insertShellRespond(con,title,url,rdata,rbody,r.status_code,r.elapsed.total_seconds(),des,result)
    return memberId, payCode, phone, entId, payCardNumber

def buyShop():
    global token
    title = "生成订单"
    memberId, payCode, phone, entId, payCardNumber = getUserCard()
    cardNumber = getCardList()
    header = {}
    header['Cookie'] = "TOKEN=" + token
    header['Content-Type'] = "application/x-www-form-urlencoded"
    #生成购物订单
    url = pay_config.global_url + "/o2ocheck/console/submitOrderNew"
    data = 'memberId=' + memberId + '&memberPhone=' + phone + '&goodsList=[{"goodsId":"11f70c1cfd8b476d899b133a31e4e0f9","actualPrice":1,"goodsNum":1}]&source=1&enterpriseId=' + entId + '&ydOrderSource=null&payCardCode=' + payCode
    r = requests.post(url, headers=header, data=data)
    if r.status_code == 200:
        result = "Success"
    else:
        result = "Error"
        for i in pay_config.maillist:
            pay_mail.sendMail(i,"http://10.9.19.179:8888/shelllog")
    pay_mode.checkResult(r.json())
    ciics_log.logging.info(r.json())
    des = "test"
    rbody = json.dumps(r.json())
    rdata = json.dumps(data)
    pay_mode.insertShellRespond(con,title,url,rdata,rbody,r.status_code,r.elapsed.total_seconds(),des,result)
    pay_mode.checkResult(r.json())
    ciics_log.logging.info(r.json())
    #print(r.json())
    orderSn = r.json()['data']['orderSn']
    #验证支付密码
    url = pay_config.global_url + "/o2ocheck/console/checkPayPassword"
    data = {}
    data['memberId'] = memberId
    data['password'] = "WP/HlfsCTK4syRR8Y+wyk7w9mYKJZ2O3RL3d8oklEenB4kOzlpwrbPhpm7Dg9GA2nf1p9tWy+Plho3ZISaEjEvUozao64l98WckWgH7FgGH/BLDpanww+QsVYKACtSIIN9lHXdRTJ730/cZdDGETLMVRf5BkpmX4WluU7IQ99ms"
    data['ydOrderSource'] = None
    title = "验证支付密码"
    r = requests.post(url, headers=header, data=data)
    if r.status_code == 200:
        result = "Success"
    else:
        result = "Error"
        for i in pay_config.maillist:
            pay_mail.sendMail(i,"http://10.9.19.179:8888/shelllog")
    pay_mode.checkResult(r.json())
    ciics_log.logging.info(r.json())
    des = "test"
    rbody = json.dumps(r.json())
    rdata = json.dumps(data)
    pay_mode.insertShellRespond(con,title,url,rdata,rbody,r.status_code,r.elapsed.total_seconds(),des,result)
    pay_mode.checkResult(r.json())
    ciics_log.logging.info(r.json())
    #print(r.json())
    #订单完成支付
    url = pay_config.global_url + "/o2ocheck/console/doOrderPay"
    data = {}
    data['orderSn'] = orderSn
    data['payCardNumber'] = payCardNumber
    data['reqId'] = str(int(time.time() * 1000))
    data['payAmount'] = 0.01
    data['cashAmount'] = 0.99
    data['totalFee'] = 1.00
    data['goodsNum'] = 1
    data['changeReason'] = "无需调价"
    data['payCode'] = cardNumber
    title = "完成订单支付"
    r = requests.post(url, headers=header, data=data)
    pay_mode.checkResult(r.json())
    ciics_log.logging.info(r.json())
    #print(r.json())
    if r.status_code == 200:
        result = "Success"
    else:
        result = "Error"
        for i in pay_config.maillist:
            pay_mail.sendMail(i,"http://10.9.19.179:8888/shelllog")
    pay_mode.checkResult(r.json())
    ciics_log.logging.info(r.json())
    des = "test"
    rbody = json.dumps(r.json())
    rdata = json.dumps(data)
    pay_mode.insertShellRespond(con,title,url,rdata,rbody,r.status_code,r.elapsed.total_seconds(),des,result)
    return None


if __name__ == "__main__":
    ciics_log.logging.info("########### 脚本开始执行 #############")
    con = pymysql.connect(pay_config.mysql_host,pay_config.mysqluser,pay_config.mysqlpasswd, 'portaltest', charset="utf8mb4")
    name = "xx0101"
    passwd = "fMRQjArXddOlX1f1RuSypxSv7Q6t+BeC8kUZRZo7LDJusLrB6uMcbonf2L6CX7B9tjx3KLfVuwArrpoRDGrX2XQypGOVNDIIpOAJDdtYzUsOAac2pxlCYNaJpGJQ5u7SpV3rkjAeFaYFn8mDuSsoPiMFWHTde7DG+owULTH5eT0="
    token = pay_login.login(name,passwd)
    getOrder()
    getShop()
    getSales()
    getCardList()
    getUserCard()
    buyShop()
    con.close()
    ciics_log.logging.info("########### 脚本执行结束 #############")
