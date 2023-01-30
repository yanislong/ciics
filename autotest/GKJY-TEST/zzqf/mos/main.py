#!/usr/bin/env python3

import requests
import threading, json, time, datetime, random

import config, mosRsa
import mosRsa_split
import testPram
import mos_log


def hisApplyDeduction(packag=testPram.testdataB01):
    #实例RSA加密对象
    #调前置机
    #print(packag)
    enfun = mosRsa_split.RsaUtil(config.pub_key, config.his_pri_key)
    endata = enfun.public_long_encrypt(json.dumps(packag))
    #endata = enfun.public_long_encrypt(json.dumps({"test":"aa"}))
    config.mosReq["requestData"] = endata
    mydata =config.mosReq
    #print(mydata)
    #mos_log.logging.info(mydata)
    header = {}
    header["Content-Type"] = "application/json"
    r = requests.post(config.testUrl, headers=header, data=json.dumps(mydata), timeout=60)
    #print(r.content)
    #print(r.json())
    print(config.testUrl)
    print(r.status_code)
    rTime = str(r.elapsed.total_seconds())
    try:
        if r.json()['code'] == 0:
            resdata = enfun.private_long_decrypt(r.json()['data'])
            result = "响应时间:#" + rTime + "#" + str(r.status_code) + resdata
            #print(result)
            mos_log.logging.info(result)
            return True
        else:
            resdata = enfun.private_long_decrypt(r.json()['data'])
            result = "响应码:#" + str(r.status_code) + "#响应时间:#" + rTime + "#" + resdata
            print(result)
            mos_log.logging.info(result)
            return False
    except json.decoder.JSONDecodeError:
        result = "响应时间:#" + rTime + "#" +  r.text
        mos_log.logging.info(result)
        return False
    except KeyError:
        print("keyError")
        result = "响应时间:#" + rTime + "#"+  r.text
        mos_log.logging.info(result)
        return False

def mosApplyDeduction():
    #实例RSA加密对象
    #直接调mos
    enfun = mosRsa_split.RsaUtil(config.pub_key, config.pri_key)
    endata = enfun.public_long_encrypt(json.dumps(testPram.testdata))
    #endata = enfun.public_long_encrypt(json.dumps({"1":"1"}))
    mydata = endata
    #mydata = testPram.testdata
    print(mydata)
    header = {}
    header["Content-Type"] = "application/json"
    r = requests.post(config.testUrl, headers=header, data=mydata)
    #print(r.content)
    print(config.testUrl)
    print(r.json())
    print(r.status_code)
    try:
        if r.json()['code'] == 0:
            try:
                result = r.elapsed.total_seconds(), r.json()['msg'] , r.json()['sbTradeNum']
                print(result)
            except:
                result = r.elapsed.total_seconds(), r.json()['msg']
                print(result)
            return result
        else:
            return False
    except json.decoder.JSONDecodeError:
        return False
    except KeyError:
        print("keyError")
        return False


def deductionConfirm():
    data = {}
    data["settlementSerialNumber"] = ""
    data["sbTradeNum"] = ""
    data["paymentAmount"] = ""
    data["verifyCode"] = ""
    r = requests.post(config.testUrl, data=data)
    print(r.content)
    if r.json()['code'] == 0:
        result = r.elapsed.total_seconds(), json()['msg']
        return result
    else:
        return False

def refund():
    data = {}
    data["Type"] = ""
    data["oldSettlementSerialNumber"] = ""
    data["oldPaySerialNumber"] = ""
    data["newSettlementSerialNumber"] = ""
    data["medData"] = ""
    data["costData"] = ""
    data["payData"] = ""
    r = requests.post(config.testUrl, data=data)
    print(r.content)
    return True

def detail():
    data = {}
    data["diagNo"] = ""
    data["name"] = ""
    data["phone"] = ""
    data["identityCard"] = ""
    data["sendId"] = ""
    data["sendOperatorCode"] = ""
    data["sendOperatorName"] = ""
    data["settleNo"] = ""
    data["recDateType"] = ""
    r = requests.post(config.testUrl, data=data)
    print(r.content)
    return True

def diction():
    data = {}
    data["operation_type"] = ""
    data["busseId"] = ""
    itemList = {}
    data["itemList"] = itemList
    r = requests.post(config.testUrl, data=data)
    print(r.content)
    return True

if __name__ == "__main__":
    #hisApplyDeduction(testPram.testdataq)
    testround = 5
    threadTotal = 0
    threadingPool = []
    threadingPool2 = []
    threadingPool3 = []
    threadingPool4 = []
    startTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    for r in range(testround):
        for i in range(threadTotal):
            b01xd = testPram.testdataB01
            b01xd["packag"]["body"]["settlementSerialNumber"] = "hc42607637c44a0d8781d4bcb7" + "".join(random.sample('zyxwvutsrqponmlkjihgfedcba',6))
            t = threading.Thread(target=hisApplyDeduction,args=(b01xd,))
            threadingPool.append(t)
            t.start()
        for j in testPram.getOrderInfo(0,0):
            b02xd = testPram.testdataB02
            b02xd["packag"]["body"]["settlementSerialNumber"] = j[1]
            b02xd["packag"]["body"]["sbTradeNum"] = j[0]
            b02xd["packag"]["body"]["paymentAmount"] = str(j[2])
            #print(b02xd)
            t2 = threading.Thread(target=hisApplyDeduction,args=(b02xd,))
            threadingPool2.append(t2)
            t2.start()
        for f in testPram.getOrderInfo(1,5):
            b03bf = testPram.testdataB03
            b03bf["packag"]["body"]["oldSettlementSerialNumber"] = f[1]
            #b03bf["packag"]["body"]["oldSettlementSerialNumber"] = 'zc42607637c44a0d8781d4bcb7ykgmqb'
            b03bf["packag"]["body"]["newSettlementSerialNumber"] = "zssss07637c44a0d8781d4bcb7" + "".join(random.sample('zyxwvutsrqponmlkjihgfedcba',6))
            #print(b03bf)
            print(b03bf["packag"]["body"]["oldSettlementSerialNumber"])
            t3 = threading.Thread(target=hisApplyDeduction,args=(b03bf,))
            threadingPool4.append(t3)
            t3.start()
        for k in testPram.getOrderInfo(1,0):
            b04qb = testPram.testdataB04
            b04qb["packag"]["body"]["oldSettlementSerialNumber"] = k[1]
            #b04qb["packag"]["body"]["oldSettlementSerialNumber"] = "hc42607637c44a0d8781d4bcb7xjwpuf"
            t4 = threading.Thread(target=hisApplyDeduction,args=(b04qb,))
            threadingPool4.append(t4)
            t4.start()
            #t = threading.Thread(target=hisApplyDeduction,args=(testPram.testdataq,))
        for j in threadingPool:
            j.join()
        for j2 in threadingPool2:
            j2.join()
        for j3 in threadingPool3:
            j3.join()
        for j4 in threadingPool4:
            j4.join()
    endTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    mos_log.logging.info('"开始执行时间：" {0},"结束时间：" {1}'.format(startTime,endTime))
    start = datetime.datetime.strptime(startTime, "%Y-%m-%d %H:%M:%S")
    end = datetime.datetime.strptime(endTime, "%Y-%m-%d %H:%M:%S")
    data = end-start  # 天数小时分钟
    #print(data)
    if data:
        days = (end-start).days  # 天数
        try:
            hours = str(data).split(',')[1].split(':')[0].replace(' ', '')  # 小时
        except IndexError:
            hours = 0
        try:
            minutes = str(data).split(':')[1]  # 分钟
        except IndexError:
            minutes = 0
        try:
            second = str(data).split(':')[2]  # 秒钟
        except IndexError:
            second = 0
        total_time = str(days*24+int(hours))+'小时'+str(minutes)+'分钟'+str(second)+'秒'  # ×小时×分钟
        #print(total_time)
    else:
        total_time = 0
    mos_log.logging.info('运行时常: {0}'.format(total_time))
