#!/usr/bin/env python3

import json
import requests
import tpa_login, ciics_log

def test(changeobjecttype,casechangetype, bcb):
    global body
    global url
    header = {}
    header['Authorization'] = token
    header['Content-Type'] = "application/json"
    mydata = {}
    mydata["caseChangeType"] = casechangetype
    mydata["changeObjectType"] = changeobjecttype
    mydata["changeObjectValue"] = bcb
    mydata[tuple(body[casechangetype].keys())[0]] = tuple(body[casechangetype].values())[0]
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
    url = "http://sittpapc.ciics.cn/tpaserver/case-change/save"
    ciics_log.logging.info("请求接口地址: " + url + "\n")
    token = tpa_login.login()
    #ChangeObjectType:  批次号->1 分案号->2 按票据号->3
    bcb = ["GCO2150055G","GCO2150103P","1231"]
    """    caseChangeType
    {"code":1,"beanName":"dutyChangeRule","desc":"给付责任","changeObjectScope":["BATCH","CASE","BILL"],"singleValue":false}
    {"code":2,"beanName":"costNameCodeChangeRule","desc":"费用项目代码","changeObjectScope":["BILL"],"singleValue":true}
    {"code":3,"beanName":"diseaseDiagnosisChangeRule","desc":"主要诊断","changeObjectScope":["BATCH","CASE","BILL"],"singleValue":false}
    {"code":4,"beanName":"receivePolicyTimeChangeRule","desc":"客户交单日","changeObjectScope":["BATCH","CASE"],"singleValue":false}
    {"code":5,"beanName":"mobileChangeRule","desc":"手机号","changeObjectScope":["CASE"],"singleValue":false}
    {"code":6,"beanName":"idCardTermValidityChangeRule","desc":"证件起止期","changeObjectScope":["CASE"],"singleValue":false}
    {"code":7,"beanName":"billDateChangeRule","desc":"票据日期","changeObjectScope":["BILL"],"singleValue":false}
    {"code":8,"beanName":"bankAccountChangeRule","desc":"领款银行账户","changeObjectScope":["CASE"],"singleValue":false}
    {"code":9,"beanName":"addressChangeRule","desc":"住址","changeObjectScope":["CASE"],"singleValue":false}
    {"code":10,"beanName":"billTypeChangeRule","desc":"票据类型","changeObjectScope":["BILL"],"singleValue":false}
    {"code":11,"beanName":"billNoChangeRule","desc":"票据号","changeObjectScope":["BILL"],"singleValue":true
    """
    testbody = {"GCO2150055G": [1,3,4,], "GCO2150103P": [1,3,4,5,6,8,9], "1231":[1,2,3,7,10,11]}
    body = {}
    body[1] = {"duty":{"billClaimType":"100","dutyCode":"520102","dutyName":"综合医疗保险金","getDutyCode":"520145","getDutyName":"门急诊医疗费用","insuranceApplicationId":"1336189224397844481","insuranceCompanyId":"4","policyNo":"66492006290001"}}
    body[2] = {"costNameCodet":{"costNameCode":"CC006","costType":"CC","detailIds":["1429730970923204610"]}}
    body[3] = {"diseaseDiagnosis":{"diseaseDiagnosis":"M8123/3","diseaseName":"基底细胞样癌 (C21.1)"}}
    body[4] = {"receivePolicyTime":{"receivePolicyTime":"2021-08-19"}}
    body[5] = {"mobile":{"mobile":"13112341238"}}
    body[6] = {"idCardTermValidity":{"endTime":"2029-12-31","longTerm":0,"startTime":"2021-08-01"}}
    body[7] = {"billDate":{"billDate":"2021-08-23"}}
    body[8] = {"bankAccount":{"bankAccount":"6225751106424455","bankCode":"8600020","bankName":"中国建设银行","bankType":"2"}}
    body[9] = {"address":{"address":"三元桥","area":"110101","city":"110100","province":"110000"}}
    body[10] = {"billType":{"billType":"7"}}
    body[11] = {"billNo":{"billNo":"1231988"}}
    myk = 1
    for x in testbody.keys():
        for y in testbody.values():
            for z in y:
                if z in testbody[x]:
                    test(myk,z,x)
        myk = myk + 1
    ciics_log.logging.info("########### 脚本执行结束 #############")
