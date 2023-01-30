#!/usr/bin/env python3

import requests
import threading, json

import config, mosRsa
import mosRsa_split
import testPram
import mos_log


def hisApplyDeduction(packag=testPram.testdataB01):
    #实例RSA加密对象
    #调前置机
    enfun = mosRsa_split.RsaUtil(config.pub_key, config.pri_key)
    endata = enfun.public_long_encrypt(json.dumps(packag))
    #endata = enfun.public_long_encrypt(json.dumps({"test":"aa"}))
    config.mosReq["requestData"] = endata
    mydata =config.mosReq
    print(mydata)
    mos_log.logging.info(mydata)
    header = {}
    header["Content-Type"] = "application/json"
    r = requests.post(config.testUrl, headers=header, data=json.dumps(mydata))
    #print(r.content)
    print(config.testUrl)
    print(r.json())
    print(r.status_code)
    try:
        if r.json()['code'] == 0:
            try:
                #resdata = enfun.private_long_decrypt(r.json()['data'])
                result = "响应时间: " + str(r.elapsed.total_seconds()) +  r.json()['message']
                print(result)
                mos_log.logging.info(result)
            except:
                result = "响应时间: " + str(r.elapsed.total_seconds()) +  r.json()['message']
                print(result)
                mos_log.logging.info(result)
            return result
        else:
            result = str(r.elapsed.total_seconds())
            print(result, r.content)
            mos_log.logging.info("响应时间: " + result + str(r.content))
            return False
    except json.decoder.JSONDecodeError:
        mos_log.logging.info(r.content)
        return False
    except KeyError:
        print("keyError")
        mos_log.logging.info(r.content)
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
    threadTotal = 1
    threadingPool = []
    for i in range(threadTotal):
        #t = threading.Thread(target=hisApplyDeduction,args=(testPram.testdataB01,))
        #t = threading.Thread(target=hisApplyDeduction,args=(testPram.testdataB02,))
        #t = threading.Thread(target=hisApplyDeduction,args=(testPram.testdataB03,))
        #t = threading.Thread(target=hisApplyDeduction,args=(testPram.testdataB04,))
        t = threading.Thread(target=hisApplyDeduction,args=(testPram.testdataq,))
        #t = threading.Thread(target=mosApplyDeduction,args=())
        threadingPool.append(t)
        t.start()
    for j in threadingPool:
        j.join()

