#!/usr/bin/env python3

import json, time
import datetime
import requests
import tpa_login, tpa_log, tpa_config

class tpa_process():

    header = {}
    header['Content-Type'] = "application/json"

    def __init__(self):
        token = tpa_login.login()
        self.header['Authorization'] = token

    def takeOrder(self, insuranceCompany, company, policyNo, expenseType, dutyType, number):

        #根据入参获取报销类型和责任类型ID
        tt = {"dictCodeList":["gen:claim_type","gen:responsibility_type","gen:ordination_area"],"channel":"TPA"}
        ed = requests.post(tpa_config.url + "/tpabaseserver/sysdict/findListByCode", headers = self.header, data=json.dumps(tt))
        tpa_log.logger.info(json.dumps(ed.json(), ensure_ascii=False))
        for t in ed.json()['data']['gen:claim_type']:
            if expenseType.strip() == t['dictName']:
                expenseTypeId = t['dictCode']
        for y in ed.json()['data']['gen:responsibility_type']:
            if dutyType.strip() == y['dictName']:
                dutyTypeId = y['dictCode']

        #根据入参insuranceCompany获取保险公司ID
        i = requests.get(tpa_config.url + "/tpabaseserver/sysinsurancecompany/findCompany", headers=self.header)
        if i.status_code == 200:
            for j in i.json()['data']:
                if insuranceCompany.strip() == j['companyName']:
                    #获取保险公司ID
                    insuranceCompanyId = j['id']
                    #查询当前保险公司下关联的企业
                    icId = {"insuranceCompanyId" : insuranceCompanyId}
                    c = requests.post(tpa_config.url + "/tpabaseserver/sysinsuranceapplication/findApplication", headers = self.header, data=json.dumps(icId))
                    tpa_log.logger.info(json.dumps(c.json(), ensure_ascii=False))
                    for k in c.json()['data']:
                        if company.strip() == k['applicationName']:
                            #获取企业ID
                            companyId = k['id']
                            #查询当前保险公司和被保单位下关联的保单号
                            comId = {"insuranceApplicationId": companyId, "insuranceCompanyId" : insuranceCompanyId}
                            e = requests.post(tpa_config.url + "/tpabaseserver/tpolicymessage/findpolicy", headers = self.header, data=json.dumps(comId))
                            tpa_log.logger.info(json.dumps(e.json(), ensure_ascii=False))
                            #判断入参的保单号是否存在
                            mymark = 0
                            for y in e.json()['data']:
                                if policyNo == y['policyNo']:
                                    mymark = 1
        if mymark == 0:
            tpa_log.logger.info("没有找到保单号")
            return None
        #请求收单接口,生成单子
        today = time.strftime("%Y-%m-%d", time.localtime())
        data = {"batchNo":"","insuranceCompanyId": insuranceCompanyId,"insuranceApplicationId":companyId,"policyNo": policyNo,"claimType": expenseTypeId,"responsibilityType": dutyTypeId,"caseAmount": number,"receivePolicyTime": today,"ordinationArea":"","healthAgency":"","exigency":"0","caseSource":"PC","pageCount":0,"amountSummary":0,"expressageNo":"","fileName":"","startTime":"","endTime":"","videoFileStatus":"1","imageVoList":[]}
        r = requests.post(tpa_config.url + "/tpaserver/tclaimbatch/saveBatch", headers = self.header, data=json.dumps(data))
        tpa_log.logger.info(json.dumps(r.json(), ensure_ascii=False))
        batchId = r.json()['data']['id']
        tpa_log.logger.info(batchId)
        return batchId

    def submitMake(self):

        #查询收单列表中未提交的单子
        searchParam = {"page":{"current":1,"size":20},"endTime":"","startTime":"","status":"1"}
        s = requests.post(tpa_config.url + "/tpaserver/tclaimbatch/pageBatch", headers = self.header, data=json.dumps(searchParam))
        tpa_log.logger.info(json.dumps(s.json(), ensure_ascii=False))
        listdata = s.json()['data']['records']
        if listdata:
            data = {'id': listdata[0]['id']}
            tpa_log.logger.info(data)
            tpa_log.logger.info('提交的批次号:' + listdata[0]['batchNo'])
            #请求收单接口
            r = requests.post(tpa_config.url + "/tpaserver/tclaimbatch/submitBatch", headers = self.header, data=json.dumps(data))
            tpa_log.logger.info(json.dumps(r.json(), ensure_ascii=False))
            if r.json()['code'] != 0:
                tpa_log.logger.info('收单异常')
                return None
            return True
        else:
            tpa_log.logger.info('收单列表没有未提交的数据')
            return None

    def inputReceive(self):

        #查询录入列表数据
        today = time.strftime("%Y-%m-%d", time.localtime())
        datebf7 = (datetime.date.today() + datetime.timedelta(days = -7)).strftime("%Y-%m-%d")
        #print(datebf7)
        data = {"page":{"current":1,"size":20},"insuranceCompanyId":"","enterCurrentNodeStartTime": datebf7,"enterCurrentNodeEndTime": today,"insuranceApp":"","policyNo":""}
        r = requests.post(tpa_config.url + "/tpaserver/tclaimcase/ocr/unCollected/page/list", headers = self.header, data=json.dumps(data))
        tpa_log.logger.info(json.dumps(r.json(), ensure_ascii=False))
        listdata = r.json()['data']['records']
        if listdata:
            data = {'workSign': listdata[0]['caseNo']}
            tpa_log.logger.info(data)
            tpa_log.logger.info('领取的批次号:' + listdata[0]['batchNo'])
            #请求领取接口
            r = requests.post(tpa_config.url + "/tpaserver/fWorkFlowConf/receiveWorkflow", headers = self.header, data=json.dumps(data))
            tpa_log.logger.info(json.dumps(r.json(), ensure_ascii=False))
            if r.json()['code'] != 0:
                tpa_log.logger.info('领取异常')
                return None
            return True
        else:
            tpa_log.logger.info('录入列表没有可领取的数据')
            return None

    def myInput(self, idCard=""):

        #我的录入列表查询
        data = {"page":{"current":1,"size":20},"nodeType":["02"]}
        r = requests.post(tpa_config.url + "/tpaserver/tclaimcase/collected/page/list", headers = self.header, data=json.dumps(data))
        #tpa_log.logger.info(json.dumps(r.json(), ensure_ascii=False))
        if r.json()['data']['records']:
            tpa_log.logger.info(json.dumps(r.json()['data']['records'][0], ensure_ascii=False))
            myId = r.json()['data']['records'][0]['caseId']
            myBatchNo = r.json()['data']['records'][0]['batchNo']
            myCaseNo = r.json()['data']['records'][0]['caseNo']
        else:
            tpa_log.logger.info("我的录入列表没有数据")
            return None

        #查询指定批次号单子详情
        r1 = requests.get(tpa_config.url + "/tpaserver/tclaimbatch/selectBatch/" + myBatchNo, headers = self.header)
        #tpa_log.logger.info(json.dumps(r1.json(), ensure_ascii=False))
        if r1.status_code == 200:
            tpa_log.logger.info(json.dumps(r1.json()['data'], ensure_ascii=False))
            myPolicyNo = r1.json()['data']['policyNo']
            myCreateTime = r1.json()['data']['createTime']
            myStatus = r1.json()['data']['status']
            myChannel = r1.json()['data']['channel']
            myCaseSource = r1.json()['data']['caseSource']
            myResponsibilityType = r1.json()['data']['responsibilityType']
            myInsuranceCompanyId = r1.json()['data']['insuranceCompanyId']
            myInsuranceApplicationId = r1.json()['data']['insuranceApplicationId']
        else:
            tpa_log.logger.info("查看案件异常,批次号: " + str(myBatchNo))
            return None

        #根据身份证号查询被保人信息

        data = {"insured":{},"insuranceApplicationId": myInsuranceApplicationId,"insuredReceiver":{},"insuredAccidentInfo":{},"applyPerson":{},"claimCase":{},"policyNo": myPolicyNo, "insuranceCompanyId": myInsuranceCompanyId, "isItTrueBankAccount": None, "showAddress": ""}
        data["insured"] = {"id":"","customerNo":"","insuredName":"","idType":"0","idCard": idCard,"idCardAddress":"","mobile":"","insuredRelationship":"","age":0,"version":0,"isLongTerm":0,"occupationType":"","startTime":None,"endTime":None,"status":0,"createUser":"","createTime":"","updateUser":"","updateTime":"","delFlag":0,"province":"","city":"","area":"","address":"","accountBalance":"0.00","dutyPlanType":""}
        data["insuredReceiver"] = {"id":"","bankName":"","bankAccount":"","insuredRelationship":"00","professionType":"","version":0,"createUser":"","createTime":None,"updateUser":"","updateTime":"","delFlag":0,"bankType":1}
        data["insuredAccidentInfo"] = {"id":"","accidentDate":None,"accidentType":"200","healthStatus":"","province":"","city":"","area":"","address":"","accidentResult":"","accidentCourse":"","accidentReason":"","version":0,"createUser":"","createTime":None,"updateUser":"","updateTime":"","delFlag":0}
        data["applyPerson"] = {"insuredRelationship":""}
        data["claimCase"] = {"id": myId,"batchId": "1455431054927102000","batchNo": myBatchNo,"caseNo": myCaseNo,"applyNo":"","socialSecurityProcessNo":"","ticketNumber":0,"amountSummary":0,"expressageNo":"","startTime":"1970-01-01 00:00:00","endTime":"1970-01-01 00:00:00","videoFileStatus":1,"caseStatus": myStatus,"caseSecondStatus":"","backReason":"","specialSign":"","physicalSign":0,"version":0,"createUser":"lihailong","createTime": myCreateTime,"updateUser":"","updateTime":"1970-01-01 00:00:00","delFlag":0,"responsibilityType": myResponsibilityType,"qualityCheckType":"A","firstTrialConclusion":"","reviewConclusion":"","oneQualityCheckConclusion":"","twoQualityCheckConclusion":"","threeQualityCheckConclusion":"","videoFileNum":0,"caseEndDate":"1970-01-01 08:00:00","loanedDate":"1970-01-01 08:00:00","frozenSerial":"","giveName":"","giveNameCode":"","channel": myChannel,"reviewTime":"1970-01-01 00:00:00","qualityCheckBatchNo":"","synCaseStatus":"0","applicationAmount":0}
        r2 = requests.post(tpa_config.url + "/tpaserver/tclaimcaseinsured/userInfo", headers = self.header, data=json.dumps(data))
        print(r2.json())
        codedata = {}
        codedata["insured"] = {"id":"1499666575177842690","batchId":"1455436581635653633","caseId":"1455436581656625154","batchNo":"0203-00235","caseNo":"0203-00235-00002","customerNo":"4198648520","dutyPlanType":"","insuredName":"袁军","idType":"0","idCard":"152701197712100618","idCardAddress":"","mobile":"13255121110","birthDate":"1970-01-01","age":0,"version":1,"isLongTerm":1,"occupationType":"5","startTime":"2011-02-18","endTime":"2199-12-31","belongToGroup":"1","createUser":"lihailong","createTime":"2022-03-04 16:42:29","updateUser":"lihailong","updateTime":"2022-03-04 16:42:32","delFlag":0,"province":"110000","city":"110100","area":"110101","address":"test","repeatMsg":"","consNo":""}
        codedata["insuranceApplicationId"] = "3"
        codedata["insuredReceiver"] = {"id":"1499666575299477505","batchId":"1455436581635653633","caseId":"1455436581656625154","batchNo":"0203-00235","caseNo":"0203-00235-00002","bankType":1,"bankName":"中国建设银行","bankAccount":"622812345678951","bankCode":"8600020-中国建设银行","insuredRelationship":"00","version":0,"createUser":"lihailong","createTime":"2022-03-04 16:42:29","updateUser":"lihailong","updateTime":"2022-03-04 16:42:32","delFlag":0}
        codedata["insuredAccidentInfo"] = {"id":"1499666575354003457","caseId":"1455436581656625154","batchId":"1455436581635653633","batchNo":"0203-00235","caseNo":"0203-00235-00002","accidentDate":"2022-03-01 00:00:00","accidentType":"200","province":"110000","city":"110100","area":"110101","address":"test","accidentResult":"","accidentCourse":"test","accidentReason":"","version":0,"createUser":"lihailong","createTime":"2022-03-04 16:42:29","updateUser":"lihailong","updateTime":"2022-03-07 17:19:49","delFlag":0,"healthStatus":""}
        codedata["applyPerson"] = {"id":"1499666575249145857","caseId":"1455436581656625154","batchId":"1455436581635653633","batchNo":"0203-00235","caseNo":"0203-00235-00002","insuredRelationship":"GX01","createUser":"lihailong","createTime":"2022-03-04 16:42:29","updateUser":"lihailong","updateTime":"2022-03-04 16:42:32","delFlag":0}
        codedata["claimCase"] = {"id":"1455436581656625154","batchId":1455436581635653600,"batchNo":"0203-00235","caseNo":"0203-00235-00002","applyNo":"","socialSecurityProcessNo":"","ticketNumber":4,"amountSummary":0,"expressageNo":"","startTime":"1970-01-01 00:00:00","endTime":"1970-01-01 00:00:00","videoFileStatus":1,"caseStatus":"02","caseSecondStatus":"","backReason":"","specialSign":"","physicalSign":0,"version":0,"createUser":"lihailong","createTime":"2021-11-02 15:28:16","updateUser":"lihailong","updateTime":"2022-03-07 17:19:49","delFlag":0,"responsibilityType":"1","qualityCheckType":"A","firstTrialConclusion":"","reviewConclusion":"","oneQualityCheckConclusion":"","twoQualityCheckConclusion":"","threeQualityCheckConclusion":"","videoFileNum":4,"caseEndDate":"1970-01-01 08:00:00","loanedDate":"1970-01-01 08:00:00","frozenSerial":"","giveName":"","giveNameCode":"","channel":"XH","reviewTime":"1970-01-01 00:00:00","qualityCheckBatchNo":"","synCaseStatus":"0","applicationAmount":0}
        codedata["policyNo"] = "202012140933"
        codedata["isItTrueBankAccount"] = False
        codedata["insuranceCompanyId"]= "1"
        return True

def returnDispatch():
    mydata = {}
    mydata["conclusion"] = "审核错误"
    mydata["comment"] = "审核人员看错了"
    mydata["caseNos"] = "GCO310000180P"
    mydata["isNeedAdjustment"] = False
    r = requests.post(url, headers=header, data=json.dumps(mydata))
    print(r.json())

if __name__ == "__main__":
    n = 1
    tpa_log.logger.info("########### 脚本开始执行 #############\n")
    mytest = tpa_process()
    for i in range(n):
        #mytest.takeOrder("XXX保险基金管理公司","神华神东煤炭集团有限责任公司","202012140933","票据报销","门诊",1)
        #mytest.submitMake()
        mytest.inputReceive()
        #mytest.myInput("152701197712100618")
        pass
    tpa_log.logger.debug("########### 脚本执行结束 #############")
