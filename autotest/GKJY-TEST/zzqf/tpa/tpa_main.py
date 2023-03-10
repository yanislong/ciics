#!/usr/bin/env python3

import json, time, random, string
import datetime
import requests
from pprint import pprint
import tpa_login, tpa_log, tpa_config

class tpa_process():

    header = {}
    token = None
    header['Content-Type'] = "application/json"

    def __init__(self):
        token = tpa_login.login()
        self.header['Authorization'] = token
        self.token = token
        self.today = time.strftime("%Y-%m-%d", time.localtime())
        self.today_1 = (datetime.date.today() + datetime.timedelta(days = -31)).strftime("%Y-%m-%d")
        self.applyStartTime = "2022-12-31"
        self.applyEndTime = "2199-12-31"

        #查询保险公司ID
        data = {"page":{"current":1,"size":20},"nodeType":["02"]}
        r = requests.get(tpa_config.url + "/tpabaseserver/sysinsurancecompany/findCompany", headers=self.header, data=json.dumps(data))
        for i in r.json()['data']:
            if tpa_config.takeOrderParam[0].strip() == i['companyName']:
                print(i['companyName'])
                companyId = i['id']
                self.companyId = companyId

        #查询投保单位ID
        data = {"insuranceCompanyId": companyId}
        r = requests.post(tpa_config.url + "/tpabaseserver/sysinsuranceapplication/findApplication", headers=self.header, data=json.dumps(data))
        for i in r.json()['data']:
            if tpa_config.takeOrderParam[1].strip() == i['applicationName']:
                print(i['applicationName'])
                applicationId = i['id']
                self.applicationId = applicationId

        #查询保单号
        data = {"insuranceApplicationId": applicationId,"insuranceCompanyId": companyId}
        r = requests.post(tpa_config.url + "/tpabaseserver/tpolicymessage/findpolicy", headers=self.header, data=json.dumps(data))
        for i in r.json()['data']:
            if tpa_config.takeOrderParam[2].strip() == i['policyNo']:
                print(i['policyNo'])
                #print(i['id'])

        #根据入参获取报销类型和责任类型ID
        tt = {"dictCodeList":["gen:claim_type","gen:responsibility_type","gen:ordination_area"],"channel":"TPA"}
        ed = requests.post(tpa_config.url + "/tpabaseserver/sysdict/findListByCode", headers = self.header, data=json.dumps(tt))
        #tpa_log.logger.info(json.dumps(ed.json(), ensure_ascii=False))
        for t in ed.json()['data']['gen:claim_type']:
            if tpa_config.takeOrderParam[3].strip() == t['dictName']:
                self.expenseTypeId = t['dictCode']
        for y in ed.json()['data']['gen:responsibility_type']:
            if tpa_config.takeOrderParam[4].strip() == y['dictName']:
                self.dutyTypeId = y['dictCode']
            else:
                self.dutyTypeId = ""

    def takeOrder(self, *top):

        insuranceCompany = top[0][0]
        company = top[0][1]
        policyNo = top[0][2]
        expenseType = top[0][3]
        dutyType = top[0][4]
        number = top[0][5]

        #请求收单接口,生成单子
        data = {"batchNo":"","insuranceCompanyId": self.companyId,"insuranceApplicationId":self.applicationId,"policyNo": tpa_config.takeOrderParam[2],"claimType": self.expenseTypeId,"responsibilityType": self.dutyTypeId,"caseAmount": tpa_config.takeOrderParam[5],"receivePolicyTime": self.today,"ordinationArea":"","healthAgency":"","exigency":"0","caseSource":"PC","pageCount":0,"amountSummary":0,"expressageNo":"","fileName":"","startTime":"","endTime":"","videoFileStatus":"1","imageVoList":[]}
        r = requests.post(tpa_config.url + "/tpaserver/tclaimbatch/saveBatch", headers = self.header, data=json.dumps(data))
        #tpa_log.logger.info(json.dumps(r.json(), ensure_ascii=False))
        batchId = r.json()['data']['id']
        tpa_log.logger.info(batchId)
        return batchId

    def submitMake(self):

        #查询收单列表中未提交的单子
        searchParam = {"page":{"current":1,"size":20},"endTime": self.today + " 00:00:00","startTime": self.today + " 00:00:00","sortField": None,"sort": None,"insuranceCompanyId": self.companyId,"insuranceApplicationId": self.applicationId,"policyNo": tpa_config.takeOrderParam[2],"claimType": self.expenseTypeId,"status":"1"}
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
        data = {"page":{"current":1,"size":20},"sortField": None,"sort": None,"insuranceCompanyId": self.companyId,"insuranceApp": self.applicationId,"policyNo": tpa_config.takeOrderParam[2],"insuranceApplicationIds":[self.applicationId],"claimType": self.expenseTypeId,"enterCurrentNodeStartTime": self.today,"enterCurrentNodeEndTime": self.today,"claimTypes":[self.expenseTypeId]}
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
        data = {"page":{"current":1,"size":20},"nodeType":["02"],"insuranceApp": self.applicationId,"policyNo": tpa_config.takeOrderParam[2],"insuranceCompanyId": self.companyId,"insuranceApplicationIds":[self.applicationId],"sortField": None,"sort": None,"claimType": self.expenseTypeId,"claimTypes": [self.expenseTypeId]}
        r = requests.post(tpa_config.url + "/tpaserver/tclaimcase/collected/page/list", headers=self.header, data=json.dumps(data))
        #tpa_log.logger.info(json.dumps(r.json(), ensure_ascii=False))
        if r.json()['data']['records']:
            tpa_log.logger.info(json.dumps(r.json()['data']['records'][0], ensure_ascii=False))
            myId = r.json()['data']['records'][0]['caseId']
            myBatchId = r.json()['data']['records'][0]['batchId']
            myBatchNo = r.json()['data']['records'][0]['batchNo']
            myCaseNo = r.json()['data']['records'][0]['caseNo']
            mybirthdate = tpa_config.idCode[6:10] + "-" + tpa_config.idCode[10:12] + "-" + tpa_config.idCode[12:14]
            print(myBatchNo)
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
            myStatus = str(r1.json()['data']['status'])
            myChannel = r1.json()['data']['channel']
            myCaseSource = r1.json()['data']['caseSource']
            myResponsibilityType = r1.json()['data']['responsibilityType']
        else:
            tpa_log.logger.info("查看案件异常,批次号: " + str(myBatchNo))
            return None

        #根据入参获取职业,国籍,关系等数据字典
        tt = {"dictCodeList":["gen:id_type","gen:relationship_type","gen:accident_type","gen:jobs_type","gen:payee_insurd_relationship","gen:health_status","gen:nation","gen:relationship","gen:pay_method","gen:public_method","gen:bank_code_to_online","gen:bank_code","gen:bank_code_to_private","gen:sex","gen:money_source","gen:payee_beneficiary_relationship"],"channel": myChannel}
        ed = requests.post(tpa_config.url + "/tpabaseserver/sysdict/findListByCode", headers = self.header, data=json.dumps(tt))
        myjob = ed.json()['data']['gen:jobs_type'][0]['dictCode']
        myaccident_type = ed.json()['data']['gen:accident_type'][0]['dictCode']
        #根据渠道判断匹配的证件类型字典
        if myChannel == "RB":
            for i in ed.json()['data']['gen:id_type']:
                if i['dictName'] == "居民身份证":
                    myid_type = i['dictCode']
                    break
        elif myChannel == "XH":
            for i in ed.json()['data']['gen:id_type']:
                if i['dictName'] == "身份证":
                    myid_type = i['dictCode']
                    break
        else:
            myid_type = "00"
        #与主被保人关系
        for i in ed.json()['data']['gen:relationship_type']:
            if i['dictName'] == "本人":
                myrelation = i['dictCode']
                break
            else:
                myrelation = "0"
        #领款人与受益人关系
        if myChannel == "RB":
            for i in ed.json()['data']['gen:payee_beneficiary_relationship']:
                if i['dictName'] == "本人":
                    mybenefrelation = i['dictCode']
                    break
                else:
                    mybenefrelation = "0"
        else:
            mybenefrelation = "00"
        if myChannel == "RB":
            myState = "156"
        else:
            for i in ed.json()['data']['gen:nation']:
                if i['dictName'] == "中国":
                    myState = i['dictCode']
                    break
                else:
                    myState = "CHN"
        for i in ed.json()['data']['gen:accident_type']:
            if i['dictName'] == "疾病":
                myaccident = i['dictCode']
                break
            else:
                myaccident = "200"
        #获取支付方式字典数据
        mypaymethodList = ed.json()['data']['gen:pay_method']
        mypaymethod = random.choice(mypaymethodList)
        mypaymethodName = mypaymethod["dictName"]
        mypaymethodCode = mypaymethod["dictCode"]
        #获取开户银行字典数据
        mybankList = ed.json()['data']['gen:bank_code']
        mybank = random.choice(mybankList)
        mybankName = mybank["dictName"]
        mybankCode = mybank["dictCode"]

        #获取医院字典数据
        data = {}
        data["channel"] = myChannel
        data["hospitalNameOrCode"] = ""
        r = requests.post(tpa_config.url + "/tpabaseserver/syshospital/list", headers=self.header, data=json.dumps(data))
        hospitalList = r.json()['data']
        hospital = random.choice(hospitalList)
        hospitalName = hospital['hospitalName']
        hospitalCode = hospital['hospitalCode']
        hospitalGrade = hospital['hospitalGrade']

        #获取疾病字典数据
        r = requests.get(tpa_config.url + "/icdcode/icddatathird/getIcdByIcdNameAndStdCode?icdName=0&stdCode=" + myChannel, headers=self.header)
        diseaseList = r.json()['data']
        disease = random.choice(diseaseList)
        diseaseName = disease['diseaseCnName']
        diseaseCode = disease['diseaseCode']

        #获取费用类型字典数据
        data = {}
        data["channel"] = myChannel
        if myChannel == "RB":
            data["dictCodeList"] = ["gen:cost_type"]
            r = requests.post(tpa_config.url + "/tpabaseserver/sysdict/findListByCode", headers=self.header, data=json.dumps(data))
            costList = r.json()['data']['gen:cost_type']
        elif myChannel == "XH":
            data["dictCodeList"] = ["gen:bill_type_A"]
            r = requests.post(tpa_config.url + "/tpabaseserver/sysdict/findListByCode", headers=self.header, data=json.dumps(data))
            costList = r.json()['data']['gen:bill_type_A']
        #print(r.json())
        cost = random.choice(costList)
        costName = cost['dictName']
        costCode = cost['dictCode']

        #根据身份证号查询被保人信息
        data = {}
        data["insuranceApplicationId"] = self.applicationId
        data["policyNo"] = tpa_config.takeOrderParam[2]
        data["insuranceCompanyId"] = self.companyId
        data["insured"] = {"id":"","customerNo":"","insuredName":"","idType": myid_type,"idCard": tpa_config.idCode,"idCardAddress":"","mobile":"","insuredRelationship":"","age":0,"version":0,"isLongTerm":0,"occupationType":"","startTime":None,"endTime":None,"status":0,"createUser":"","createTime":"","updateUser":"","updateTime":"","delFlag":0,"province":"","city":"","area":"","address":"","accountBalance":"0.00","dutyPlanType":"","insuredState": myState,"birthDate": mybirthdate,"sex":0}
        data["insuredReceiver"] = {"id":"","bankName":"","bankAccount":"","insuredRelationship":"00","professionType":"","version":0,"createUser":"","createTime":None,"updateUser":"","updateTime":"","delFlag":0,"bankType":1}
        data["trustee"] ={"trusteeFlag":0,"trusteeType":"","trusteeRelation":"","insuredRelationship":"","trusteeName":"","idType":"","idCard":"","mobile":"","startTime":"","endTime":"","emailAddress":"","province":"","city":"","area":"","email":"","address":"","idCardAddress":"","applyState": "CHN","birthDate":"","trusteeState":"","sex": None}
        data["applyPerson"] = {"insuredRelationship":"","applyName":"","idType":"","idCard":"","mobile":"","applyStartTime":"","applyEndTime":"","emailAddress":"","province":"","city":"","area":"","email":"","address":"","idCardAddress":"","applyState": myState,"birthdate":"","sex": None}
        data["claimCase"] = {"id": myId,"batchId": myBatchId,"batchNo": myBatchNo,"caseNo": myCaseNo,"applyNo":"","socialSecurityProcessNo":"","ticketNumber":0,"amountSummary":0,"expressageNo":"","startTime":"1970-01-01 00:00:00","endTime":"1970-01-01 00:00:00","videoFileStatus":1,"caseStatus": "02","caseSecondStatus":"","backReason":"","specialSign":"","physicalSign":0,"version":0,"createUser":"lihailong","createTime": myCreateTime,"updateUser":"","updateTime":"1970-01-01 00:00:00","delFlag":0,"responsibilityType": self.expenseTypeId,"qualityCheckType":"A","firstTrialConclusion":"","reviewConclusion":"","oneQualityCheckConclusion":"","twoQualityCheckConclusion":"","threeQualityCheckConclusion":"","videoFileNum":0,"caseEndDate":"1970-01-01 08:00:00","loanedDate":"1970-01-01 08:00:00","frozenSerial":"","giveName":"","giveNameCode":"","channel": myChannel,"reviewTime":"1970-01-01 00:00:00","qualityCheckBatchNo":"","synCaseStatus":"0","applicationAmount":0}
        data["principalInsured"] = {"area":"","batchId":"","batchNo":"","belongToGroup":"","birthDate":"","caseId":"","caseNo":"","city":"","createTime":"","createUser":"","customerNo":"","delFlag":0,"dutyPlanType":"","empOnDuty":"","empOnDutyName":"","endTime":"","id":"","idCard":"","idCardAddress":"","idType":"","insuredId":"","insuredName":"","isLongTerm":0,"isSameAddress":0,"mobile":"","occupationType":"","province":"","repeatMsg":"","showAddress":"","socialAddress":"","startTime":"","updateTime":"","updateUser":"","version":0,"principalInsuredState": myState,"sex": None}
        #data["insuredAccidentInfo"] = {"id":"","accidentDate":None,"accidentType": myaccident_type,"healthStatus":"","province":"","city":"","area":"","address":"","accidentResult":"","accidentCourse":"","accidentReason":"","version":0,"createUser":"","createTime":None,"updateUser":"","updateTime":"","delFlag":0}
        #pprint(data)
        r2 = requests.post(tpa_config.url + "/tpaserver/tclaimcaseinsured/userInfo", headers = self.header, data=json.dumps(data))
        #pprint(r2.json())
        if r2.json()['code'] == 0:
            name = r2.json()['data']['insured']['insuredName']
            if r2.json()['data']['insured']['idCardAddress']:
                myaddress = r2.json()['data']['insured']['idCardAddress']
            else:
                myaddress = "北京"
            if r2.json()['data']['insured']['mobile']:
                mobile = r2.json()['data']['insured']['mobile']
            else:
                mobile = "13141031234"
            if r2.json()['data']['insured']['birthDate']:
                mybirthdate = r2.json()['data']['insured']['birthDate']
            if r2.json()['data']['insured']['startTime']:
                startTime = self.applyStartTime
            else:
                startTime = r2.json()['data']['insured']['startTime']
            if r2.json()['data']['insured']['endTime']:
                endTime = self.applyEndTime
            else:
                endTime = r2.json()['data']['insured']['endTime']
            myprincipalInsuredRelation = r2.json()['data']['insured']['principalInsuredRelation']
            mybelongToGroup = r2.json()['data']['insured']['belongToGroup']
            sex = r2.json()['data']['insured']['sex']
            gender = r2.json()['data']['insured']['sex']
            insuredId = r2.json()['data']['insured']['id']
            customer = r2.json()['data']['insured']['customerNo']
            applyPersonId = r2.json()['data']['applyPerson']['id']
            trusteeId = r2.json()['data']['trustee']['id']
            principalInsuredId = r2.json()['data']['principalInsured']['id']
            amountSum = r2.json()['data']['claimCase']['amountSummary']
            videoFileStatus = r2.json()['data']['claimCase']['videoFileStatus']
            ticketNumber = r2.json()['data']['claimCase']['ticketNumber']
            qualityCheckType = r2.json()['data']['claimCase']['qualityCheckType']
            videoFileNum = r2.json()['data']['claimCase']['videoFileNum']
            mybankaccount = "6234234234234"
            #occupationType = r2.json()['data']['insured']['occupationType']
        else:
            print(tpa_config.idCode + " 获取承保数据失败!")
            return None

        #保存受益人信息
        data = {}
        data = {"batchId": myBatchId,"batchNo": myBatchNo,"benefitEndTime": None,"benefitIdCard": tpa_config.idCode,"benefitIdType": tpa_config.codeType,"benefitIdTypeName":"","benefitName": name,"benefitRatio":"1","benefitStartTime": startTime,"caseId": myId,"caseNo": myCaseNo,"createTime":"","createUser":"","delFlag":0,"email":"","mobile": mobile,"id":0,"idCardAddress": myaddress,"isSameAddress":1,"permanentFlag":0,"relationAddress": myaddress,"relationArea":"110101","relationAreaName":"东城区","relationCity":"110100","relationCityName":"北京市","relationProvince":"110000","relationProvinceName":"北京市","relationToInsured": myrelation,"relationToInsuredName":"","updateTime":"","updateUser":"","benefitState": myState,"relationOccupationType":  myjob,"relationToAppntNo": myrelation,"birthday": mybirthdate,"sex": gender}
        #print(data)
        r = requests.post(tpa_config.url + "/tpaserver/tclaimcasebeneficiary/save", headers = self.header, data=json.dumps(data))
        print(r.json())

        #保存领款人信息,先查询受益人Id
        data = {}
        data["caseId"] = myId
        r = requests.post(tpa_config.url + "/tpaserver/tclaimcasebeneficiary/find", headers=self.header, data=json.dumps(data))
        beneficiaryId = r.json()['data'][0]['id']
        data = {}
        data = {"bankAccount": mybankaccount,"bankBranch":"","bankCity":"","bankCityName":"","bankCode": mybankCode + "-" + mybankName,"bankName": mybankName,"bankProvince":"","bankProvinceName":"","bankType":2,"batchId": myBatchId,"wochongqi":"","batchNo": myBatchNo,"beneficiaryId": beneficiaryId,"beneficiaryName": name,"bankAccountName": name,"caseId": myId,"caseNo": myCaseNo,"createTime":"","createUser":"","delFlag":0,"email":"","id":0,"idCardAddress": myaddress,"insuredRelationship": myrelation,"bankProvince":"01","bankProvinceName":"安徽","bankCity":"01001","bankCityName":"东至","isSameAddress":1,"mobile": mobile,"payeeEndTime":"2199-12-31","payeeIdCard": tpa_config.idCode,"payeeIdType":"0","payeeIdTypeName":"","payeeName": name,"payeeStartTime": startTime,"permanentFlag":1,"relationAddress": myaddress,"relationArea":"110101","relationAreaName":"东城区","relationCity":"110100","relationCityName":"北京市","relationPhone":"","relationProvince":"110000","relationProvinceName":"北京市","updateTime":"","updateUser":"","version":0,"receiverState": myState,"relationToBeneficiary": mybenefrelation,"payMode": mypaymethodCode,"payforpubFlag":"0","birthday": mybirthdate,"sex": gender,"relationOccupationType": myjob}
        r = requests.post(tpa_config.url + "/tpaserver/receiver/save", headers = self.header, data=json.dumps(data))
        print(r.json())

        #保存基本信息
        data = {}
        data["insured"] = {"id": insuredId,"batchId": myBatchId,"caseId": myId,"batchNo": myBatchNo,"caseNo":myCaseNo,"customerNo": customer,"dutyPlanType":"","insuredName": name,"idType": tpa_config.codeType,"idCard": tpa_config.idCode,"idCardAddress": myaddress,"mobile": mobile,"birthDate": mybirthdate,"age":0,"version":1,"isLongTerm":1,"occupationType": myjob,"startTime": self.applyStartTime,"endTime":"2199-12-31","belongToGroup": mybelongToGroup,"createUser":"lihailong","createTime": myCreateTime,"updateUser":"lihailong","updateTime": myCreateTime,"delFlag":0,"province":"110000","city":"110100","area":"110102","address": myaddress,"repeatMsg":"","socialAddress":"","insuredTag":0,"principalInsuredRelation": myprincipalInsuredRelation,"isSameAddress":0,"insuredState": myState,"sex": gender,"consNo":""}
        data["insuredReceiver"] = {"id":"","bankName":"","bankAccount":"","insuredRelationship": myrelation,"professionType":"","version":0,"createUser":"","createTime": None,"updateUser":"","updateTime":"","delFlag":0,"bankType":1}
        data["applyPerson"] = {"id": applyPersonId,"caseId": myId,"batchId": myBatchId,"batchNo": myBatchNo,"caseNo": myCaseNo,"insuredRelationship": myprincipalInsuredRelation,"applyName": name,"idType":tpa_config.codeType,"idCard": tpa_config.idCode,"applyStartTime": self.applyStartTime,"applyEndTime":"2199-12-31","permanentFlag":0,"mobile": mobile,"email":"","province":"110000","city":"110100","area":"110102","address": myaddress,"idCardAddress": myaddress,"isSameAddress":0,"applyState": myState,"createUser":"lihailong","createTime": None,"updateUser":"","updateTime":"1970-01-01 00:00:00","delFlag":0,"birthdate": mybirthdate,"sex": gender}
        data["trustee"] = {"id": trusteeId,"batchId": myBatchId,"caseId": myId,"batchNo": myBatchNo,"caseNo": myCaseNo,"trusteeFlag":0,"trusteeType":"","trusteeRelation":"","trusteeName":"","idType":"","idCard":"","sex": None,"birthDate": None,"mobile":"","startTime": None,"endTime": None,"isLongTerm":0,"occupationType":"","trusteeState":"","province":"","city":"","area":"","address":"","idCardAddress":"","createUser":"lihailong","createTime": None,"updateUser":"lihailong","updateTime": None,"delFlag":0,"email":"","postcode":""}
        data["claimCase"] = {"id": myId,"batchId": myBatchId,"batchNo": myBatchNo,"caseNo": myCaseNo,"applyNo":"","socialSecurityProcessNo":"","ticketNumber": ticketNumber,"amountSummary": amountSum,"expressageNo":"","startTime":"1970-01-01 00:00:00","endTime":"1970-01-01 00:00:00","videoFileStatus": videoFileStatus,"caseStatus": "02","caseSecondStatus":"","backReason":"","specialSign":"","physicalSign":0,"version":0,"createUser":"lihailong","createTime": myCreateTime,"updateUser":"lihailong","updateTime": myCreateTime,"delFlag":0,"responsibilityType":"","qualityCheckType": qualityCheckType,"firstTrialConclusion":"","reviewConclusion":"","oneQualityCheckConclusion":"","twoQualityCheckConclusion":"","threeQualityCheckConclusion":"","videoFileNum": videoFileNum,"caseEndDate":"1970-01-01 08:00:00","loanedDate":"1970-01-01 08:00:00","frozenSerial":"","giveName":"","giveNameCode":"","channel": myChannel,"reviewTime":"1970-01-01 00:00:00","qualityCheckBatchNo":"","synCaseStatus":"0","applicationAmount":0,"importCaseRecordId":"0","importCasePassFlag":0,"importCaseBackFlag":0,"fundsProvided":""}
        data["principalInsured"] = {"id": principalInsuredId,"batchId": myBatchId,"caseId": myId,"batchNo": myBatchNo,"dutyPlanType":"","caseNo": myCaseNo,"customerNo": customer,"occupationType": myjob,"insuredName": name,"idType": tpa_config.codeType,"idCard": tpa_config.idCode,"belongToGroup": mybelongToGroup,"startTime":"2011-02-18","endTime":"2199-12-31","isLongTerm":0,"province":"110000","city":"110100","area":"110102","address": myaddress,"idCardAddress": myaddress,"principalInsuredState": myState,"mobile": mobile,"birthDate": mybirthdate,"age":0,"version":0,"createUser":"","createTime": myCreateTime,"updateUser":"lihailong","updateTime": myCreateTime,"delFlag":0,"repeatMsg":"","isSameAddress":0,"socialAddress":"","insuredId": insuredId,"sex": gender}
        data["insuranceApplicationId"] = self.applicationId
        data["policyNo"] = tpa_config.takeOrderParam[2]
        data["insuranceCompanyId"] = self.companyId
        data["isItTrueBankAccount"] = False
        data["isItTrueBankAccount"] = None
        data["showAddress"] = ""
        #pprint(data)
        r = requests.post(tpa_config.url + "/tpaserver/tclaimcaseinsured/saveOrUpdate", headers = self.header, data=json.dumps(data))
        if r.json()['code'] == 0:
            print("保存基本信息成功!")
        else:
            pprint(r.json())
            return None

        #保存明细,先查询费用明细的药品/项目字典
        r = requests.get(tpa_config.url + "/tpabaseserver/sysdictmedical/page?size=20&current=1&name=1&channel=" + myChannel, headers=self.header)
        medicalList = r.json()['data']['records']
        medical = random.choice(medicalList)
        medicalName = medical['name']
        medicalId = medical['id']
        medicalCode = medical['standardCode']

        #上传影像件
        billList = []
        fileheader = {}
        fileheader['Authorization'] = self.token
        dataimage = {}
        dataimage['objectAcl'] = (None,"private")
        dataimage['isCompression'] = (None,True)
        dataimage['channelKey'] = (None,"tpa")
        dataimage['bucketName'] = (None,"sit-ciics")
        dataimage['icdCode'] = (None,"O03,O04,O05,O06,O07,O60,O61,O62,O63,O64,O65,O66,O67,O68,O69,O70,O71,O72,O73,O74,O75,O80,O81,O82,O83,O84,Z30,Z31,Z32,Z33,Z34,Z35,Z36,Z37,Z38,Z39")
        dataimage['accidentNature'] = (None,"EH4913:132:00:04,EH4913:131:00:05,EH1051:130:01:04,EH4913:10101:10101:05,EH4913:133:00:04")
        if myChannel == "RB":
            dataimage['file'] = ("tpd.jpg",open('tpd.jpg','rb'))
            r = requests.post(tpa_config.url + "/tpaossserver/oss/compression/upload/public/acl", headers=fileheader, files=dataimage)
            ossid = r.json()['data']['fileInfoId']
            filename = r.json()['data']['fileName']
            filePath = r.json()['data']['filePath']
            thumbnail = r.json()['data']['thumbnail']
            datatpd = {}
            datatpd["imagetypeId"] = "1283234106666246146"
            datatpd["imageSubtypeId"] = "1283279337436557311"
            datatpd["imagetypeCode"] = 1 #公共卷
            datatpd["imageSubtypeCode"] = 1 #团批单
            datatpd["fileName"] = filename
            datatpd["imageUrl"] = filePath
            datatpd["thumbnail"] = thumbnail
            datatpd["ossid"] = ossid
            datatpd["caseId"] = myId
            r = requests.post(tpa_config.url + "/tpaserver/tclaimimage/upload/image/handle/data", headers=self.header, data=json.dumps(datatpd))
            if r.json()["code"] == 0:
                print("团批单上传成功")
            else:
                print(r.json())

        for i in range(tpa_config.imageNum):
            ##案件与影像件关联
            dataimage['file'] = ("2023.jpg",open('2023.jpg','rb'))
            r = requests.post(tpa_config.url + "/tpaossserver/oss/compression/upload/public/acl", headers=fileheader, files=dataimage)
            #pprint(r.json())
            ossid = r.json()['data']['fileInfoId']
            filename = r.json()['data']['fileName']
            filePath = r.json()['data']['filePath']
            thumbnail = r.json()['data']['thumbnail']
            data = {}
            data["imagetypeId"] = "1283234619369578497"
            data["imagetypeCode"] = 4 #票据类型
            imagetype = random.choice([14,30])
            if imagetype == 30:
                data["imageSubtypeId"] = "1361561999279947779"
                data["imageSubtypeCode"] = imagetype  #医疗电子票据
            elif imagetype == 14:
                data["imageSubtypeId"] = "1283279337436557413"
                data["imageSubtypeCode"] = imagetype #增值税发票
            data["fileName"] = filename
            data["imageUrl"] = filePath
            data["thumbnail"] = thumbnail
            data["ossid"] = ossid
            data["caseId"] = myId
            r = requests.post(tpa_config.url + "/tpaserver/tclaimimage/upload/image/handle/data", headers=self.header, data=json.dumps(data))
            #pprint(r.json())

            #保存增值税发票,先查询影像件列表
            data = {}
            data ={"caseId": myId}
            r = requests.post(tpa_config.url + "/tpaserver/tclaimsettlementcasebill/list", headers=self.header, data=json.dumps(data))
            imageId = r.json()['data'][-1]['id']
            imageSeq = r.json()['data'][-1]['imageSeqNo']
            data = {}
            data = {"billTypeName":None,"dischargeTime":"","hospitalizedTime":"","reckoningTime":None,"hospitalCode": hospitalCode,"hospitalName": hospitalName,"hospitalGrade": hospitalGrade,"hospitalGradeName":None,"diseaseDiagnosis": diseaseCode,"countAmount":"10","medicalInsuranceAmount":"10.00","unitSupplementaryPayAmount":0,"fundPayAmount":0,"medicalAidInsurancePay":0,"retireSupplementaryMedicalPay":0,"disabledSoldierAllowanceMedicalPay":0,"medicalInsuranceFundPay":0,"personalAccountRemainingAmount":0,"selfPay1":"0","startPayAmount":0,"exceedingLimitAmount":0,"selfPay2":0,"selfPayAmount":"10.00","personalAccountPayAmount":0,"ownExpensePayAmount":"10","personalCashPayAmount":0,"yearFundTotalPayAmount":0,"cumulativeMedicalInsuranceRangeAmount":0,"retireSupplyMedicalInsurancePay":0,"unitSupplyMedicalInsurancePay":0,"yearLargeTotalPayAmount":0,"insuranceCompanyPaymentAmount":0,"otherThirdPayAmount":0,"thirdPartyPayAmount":0,"subjoinPayAmount":0,"claimDetailType":"1","insuredType":"1","socialSecurityPaymentAmount":0,"medicalFundPayAmount":0,"hospitalDays":0,"hospitalFlag":2,"repeatStatus":None,"repeatMsg":None,"billCode":"20312030","billName":"","billDate": self.today_1,"caseStatus":None,"countDeductAmount":None,"diseaseNameBefore":"","diseaseName": diseaseName,"checkCode":"123456","checkAuthenticityStatus":"not_verified","checkAuthenticityStatusDesc":"未验真","imageTypeName":"增值税发票","imageType":"4","imageSubtype":"14","imageSubTypeName":"增值税发票","refusePaymentStatus":None,"remark":"","deductionAccount":None,"fixedPoint":0,"fixedPointName":"非定点","imageSeqNo": imageSeq,"settlementStatus":1,"settlementStatusName":"是","eventId":"0","eventNo":"","accidentType": myaccident,"accidentReason":"","accidentReasonName":"","healthStatus":"03","cureDesc":"01","deathDate":None,"deformityDate":None,"accidentProvince":"650000","accidentCity":"652700","accidentArea":"652723","accidentAddress":"四姑娘山","hospitalAddress":"","repeatReasons":"","repeatDescribe":"","accResult2":"O47","accResult2Name":"假临产","accResult1":"OO4","accResult1Name":"与胎儿和羊膜腔及可能的分娩问题有关的孕产妇医疗(O30-O48）","hospitalNo":"","visitName":"","checkStatus":None,"fundSelfPay":0,"largeSelfPay":0,"exceedingMedicalFund":0,"billDutyType":"","isTrueFlag":None,"billOtherPays":[{"billId":"","selfPay1":"","selfPay2":"","ownExpensePayAmount":"","claimPayAmount":"","claimPayDate":"","claimPayUnit":"","claimPayUnitName":""}]}
            data["batchId"] = myBatchId
            data["caseId"] = myId
            data["batchNo"] = myBatchNo
            data["caseNo"] = myCaseNo
            data["ossid"] = ossid
            data["id"] = imageId
            data["billNo"] = time.strftime("%Y%m%d%H%M%S",time.localtime())
            myBillNo = data["billNo"]
            data["billType"] = "3"
            data["visitTime"] = self.today_1
            data["billCode"] = ''.join(random.sample(string.digits,8))
            myBillCode = data['billCode']
            data["billDate"] = self.today_1
            data["checkCode"] = "123456"
            data["imageType"] = "4"
            data["imageSubtype"] = "14"
            data["imageSeqNo"] = imageSeq
            #pprint(data)
            r = requests.post(tpa_config.url + "/tpaserver/tclaimsettlementcasebill/saveOrUpdate", headers=self.header, data=json.dumps(data))
            #pprint(r.json())

            data = []
            datainfo = {"costTypeName": costName,"costType": costCode,"costName":"","costNameCode":"","surgicalDiagnosisType":"","quantity":"1","drugName": medicalName,"druglist": medicalList,"selfPay1":"10","selfRatio":0,"selfPay2":0,"ownExpensePayAmount":0,"insuranceCompanyPaymentAmount":0,"otherThirdPaymentAmount":0,"unitPrice":"10.0","deductAmount":0,"deductCause":"","amount":"10","billId": imageId,"billNo": myBillNo,"batchId": myBatchId,"caseId": myId,"batchNo": myBatchNo,"caseNo": myCaseNo,"deductionCostReason":"99","deductionCostReasonName":"其他","goodsId": medicalId,"goodsCode": medicalCode,"principalInsuredIdType":"0","principalInsuredIdCode": tpa_config.idCode,"saveFlag":1,"index":0,"specification":"个"}
            data.append(datainfo)
            r = requests.post(tpa_config.url + "/tpaserver/tclaimcasebilldeductiondetail/saveOrUpdate", headers=self.header, data=json.dumps(data))
            print(r.json())

        #提交录入,1.获取inusredId;2.获取eventId,eventNo;3.获取detailId;4.获取票据ossid
        r = requests.get(tpa_config.url + "/tpaserver/tclaimcaseprincipalinsured/findByCaseId/" + myId, headers=self.header)
        #print(r.json())
        insuredId = r.json()['data']['insuredId']
        data = {}
        data["caseId"] = myId
        r = requests.post(tpa_config.url + "/tpaserver/claimCaseEvent/list", headers=self.header, data=json.dumps(data))
        eventId = r.json()['data'][0]['id']
        eventNo = r.json()['data'][0]['eventNo']
        data = {}
        data["billId"] = imageId
        r = requests.post(tpa_config.url + "/tpaserver/tclaimcasebilldeductiondetail/list", headers=self.header, data=json.dumps(data))
        detailId = r.json()['data'][0]['id']
        r = requests.get(tpa_config.url + "/tpaserver/tclaimcaseinsured/findInsured?caseId=" + myId, headers=self.header)
        applyPersonId = r.json()['data']['applyPerson']['id']
        data = {}
        data["caseId"] = myId
        r = requests.post(tpa_config.url + "/tpaserver/tclaimsettlementcasebill/list", headers=self.header, data=json.dumps(data))
        for i in r.json()['data']:
            billList.append(i['ossid'])
        data = {}
        data["caseId"] = myId
        data["billNoList"] = billList
        data["claimCaseBillSaveReq"] = {"ossid": ossid,"id": imageId,"batchId": myBatchId,"caseId": myId,"batchNo": myBatchNo,"caseNo": myCaseNo,"billNo": myBillNo,"billType":"3","billTypeName":None,"visitTime": self.today_1,"dischargeTime":None,"hospitalizedTime":None,"reckoningTime":None,"hospitalCode": hospitalCode,"hospitalName": hospitalName,"hospitalGrade": hospitalGrade,"hospitalGradeName":None,"diseaseDiagnosis": diseaseCode,"countAmount":10,"medicalInsuranceAmount":10,"unitSupplementaryPayAmount":0,"fundPayAmount":0,"medicalAidInsurancePay":0,"retireSupplementaryMedicalPay":0,"disabledSoldierAllowanceMedicalPay":0,"medicalInsuranceFundPay":0,"personalAccountRemainingAmount":0,"selfPay1":0,"startPayAmount":0,"exceedingLimitAmount":0,"selfPay2":0,"selfPayAmount":10,"personalAccountPayAmount":0,"ownExpensePayAmount":10,"personalCashPayAmount":0,"yearFundTotalPayAmount":0,"cumulativeMedicalInsuranceRangeAmount":0,"retireSupplyMedicalInsurancePay":0,"unitSupplyMedicalInsurancePay":0,"yearLargeTotalPayAmount":0,"insuranceCompanyPaymentAmount":0,"otherThirdPayAmount":0,"thirdPartyPayAmount":0,"subjoinPayAmount":0,"claimDetailType":"1","insuredType":"1","socialSecurityPaymentAmount":0,"medicalFundPayAmount":0,"hospitalDays":0,"hospitalFlag":2,"repeatStatus":0,"repeatMsg":None,"billCode": myBillCode,"billName":"","billDate": self.today_1,"caseStatus":None,"countDeductAmount":None,"diseaseNameBefore":"","diseaseName": diseaseName,"checkCode":"123456","checkAuthenticityStatus":"not_verified","checkAuthenticityStatusDesc":"未验真","imageTypeName":"增值税发票","imageType":"4","imageSubtype":"14","imageSubTypeName":"增值税发票","refusePaymentStatus":None,"remark":"","deductionAccount":None,"fixedPoint":0,"fixedPointName":"非定点","imageSeqNo": imageSeq,"settlementStatus":1,"settlementStatusName":"是","eventId": eventId,"eventNo": eventNo,"accidentType":"200","accidentReason":"","accidentReasonName":"","healthStatus":"03","cureDesc":"01","deathDate":None,"deformityDate":None,"accidentProvince":"650000","accidentCity":"652700","accidentArea":"652723","accidentAddress":"四姑娘山","hospitalAddress":"","repeatReasons":"","repeatDescribe":"","accResult2":"O47","accResult2Name":"假临产","accResult1":"OO4","accResult1Name":"与胎儿和羊膜腔及可能的分娩问题有关的孕产妇医疗(O30-O48）","hospitalNo":"","visitName":"","checkStatus":None,"fundSelfPay":0,"largeSelfPay":0,"exceedingMedicalFund":0,"claimCaseAccidentInfoId":""}
        data["caseBillDeductionDetails"] = [{"id": detailId,"batchId": myBatchId,"caseId": myId,"batchNo": myBatchNo,"caseNo": myCaseNo,"costType": costCode,"quantity":1,"unitPrice":10,"deductAmount":0,"billId": imageId,"amount":10,"deductCause":"","createUser":None,"createTime":None,"updateUser":None,"updateTime":None,"delFlag":0,"costNameCode":"","surgicaNo":"","surgicalDiagnosisType":"","deductionCostReason":"99","selfPay1":10,"selfPay2":0,"ownExpensePayAmount":0,"insuranceCompanyPaymentAmount":0,"otherThirdPaymentAmount":0,"drugName": medicalName,"selfRatio":0,"specification":"个","model":"","classAFee":None,"goodsCode": medicalCode,"goodsId": medicalId,"checkLabelCodes":None,"checkLabelNames":None,"principalInsuredIdType":tpa_config.codeType,"principalInsuredIdCode": tpa_config.idCode,"saveFlag":1,"costTypeName": costName,"costName":None,"deductionCostReasonName":"其他","channel": myChannel,"index":0}]
        data["insuredInfoVo"] = {"insured":{"id": insuredId,"batchId": myBatchId,"caseId": myId,"batchNo": myBatchNo,"caseNo": myCaseNo,"customerNo": customer,"dutyPlanType":"","insuredName": name,"idType": tpa_config.codeType,"idCard": tpa_config.idCode,"idCardAddress": myaddress,"mobile": mobile,"birthDate": mybirthdate,"age":0,"version":1,"isLongTerm":1,"occupationType": myjob,"startTime":"2011-02-18","endTime":"2199-12-31","belongToGroup": mybelongToGroup,"createUser":"lihailong","createTime": myCreateTime,"updateUser":"lihailong","updateTime": myCreateTime,"delFlag":0,"province":"110000","city":"110100","area":"110102","address": myaddress,"repeatMsg":"","socialAddress":"","insuredTag":0,"principalInsuredRelation": myprincipalInsuredRelation,"isSameAddress":0,"insuredState": myState,"sex": gender},"insuredReceiver":{"id":"","bankName":"","bankAccount":"","insuredRelationship": myprincipalInsuredRelation,"professionType":"","version":0,"createUser":"","createTime":None,"updateUser":"","updateTime":"","delFlag":0,"bankType":1},"applyPerson":{"id": applyPersonId,"caseId": myId,"batchId": myBatchId,"batchNo": myBatchNo,"caseNo": myCaseNo,"insuredRelationship": myprincipalInsuredRelation,"applyName": name,"idType": tpa_config.codeType,"idCard": tpa_config.idCode,"applyStartTime": self.applyStartTime,"applyEndTime":"2199-12-31","permanentFlag":0,"mobile": mobile,"email":"","province":"110000","city":"110100","area":"110102","address": myaddress,"idCardAddress": myaddress,"isSameAddress":0,"applyState": myState,"createUser":"lihailong","createTime": myCreateTime,"updateUser":"lihailong","updateTime": myCreateTime,"delFlag":0,"birthdate":"1977-12-10","sex": gender},"policyNo": tpa_config.takeOrderParam[2],"insuranceApplicationId": self.applicationId,"insuranceCompanyId": self.companyId}
        data["comment"] = "我独不解中国人何以于旧状况那么心平气和,于较新的机运就这么疾首蹙额;于已成之局那么委曲求全;于初兴之事就这么求全责备？"
        #pprint(data)
        r = requests.post(tpa_config.url + "/tpaserver/tclaimcase/ocr/submit", headers=self.header, data=json.dumps(data))
        print(r.json())
        return True

    def dataReview(self):

        #数据审核领取,先查询待领取列表，然后领取
        data = {}
        data["page"] = {"current": 1,"size": 20}
        data["nodeType"] = ["03"]
        data["insuranceApp"] = self.applicationId
        data["policyNo"] = tpa_config.takeOrderParam[2]
        data["sortField"] = None
        data["sort"] = None
        data["insuranceCompanyId"] = self.companyId
        data["insuranceApplicationIds"] = [self.applicationId]
        r = requests.post(tpa_config.url + "/tpaserver/tclaimcase/unCollected/page/list", headers=self.header, data=json.dumps(data))
        #pprint(r.json())
        caseNo = r.json()['data']['records'][0]['caseNo']
        data = {}
        data = {"workSign": caseNo}
        r = requests.post(tpa_config.url + "/tpaserver/fWorkFlowConf/receiveWorkflow", headers=self.header, data=json.dumps(data))
        #print(r.json())

        #数据审核提交,先查询已领取列表，然后审核
        data = {}
        data["page"] = {"current": 1,"size": 20}
        data["nodeType"] = ["03"]
        data["insuranceApp"] = self.applicationId
        data["policyNo"] = tpa_config.takeOrderParam[2]
        data["sortField"] = None
        data["sort"] = None
        data["insuranceCompanyId"] = self.companyId
        data["insuranceApplicationIds"] = [self.applicationId]
        r = requests.post(tpa_config.url + "/tpaserver/tclaimcase/collected/page/list", headers=self.header, data=json.dumps(data))
        pprint(r.json())
        caseNo = r.json()['data']['records'][0]['caseNo']
        caseId = r.json()['data']['records'][0]['caseId']
        #data = {}
        #data = {"workSign": caseNo}
        #获取ossid
        data = {}
        data = {"caseId": caseId}
        r = requests.post(tpa_config.url + "/tpaserver/tclaimsettlementcasebill/list", headers=self.header, data=json.dumps(data))
        ossidList = []
        myId = r.json()['data'][0]['id']
        myBatchId = r.json()['data'][0]['batchId']
        myBatchNo = r.json()['data'][0]['batchNo']
        myNo = r.json()['data'][0]['batchNo']
        myId = r.json()['data'][0]['id']
        myId = r.json()['data'][0]['id']
        for i in r.json()['data']:
            ossidList.append(i['ossid'])
        data = {}
        data["caseId"] = caseId
        data["billNoList"] = ossidList
        data["claimCaseBillSaveReq"] = {"ossid": ossidList[0],"id": myId,"batchId": myBatchId,"caseId": caseId,"batchNo": myBatchNo,"caseNo": caseNo,"billNo":"20230222140034","billType":"3","billTypeName":None,"visitTime":"2023-02-20","dischargeTime":None,"hospitalizedTime":None,"reckoningTime":None,"hospitalCode":"0000001","hospitalName":"上海中治职工医院","hospitalGrade":23,"hospitalGradeName":None,"diseaseDiagnosis": diseaseCode,"countAmount":10,"medicalInsuranceAmount":10,"unitSupplementaryPayAmount":0,"fundPayAmount":0,"medicalAidInsurancePay":0,"retireSupplementaryMedicalPay":0,"disabledSoldierAllowanceMedicalPay":0,"medicalInsuranceFundPay":0,"personalAccountRemainingAmount":0,"selfPay1":0,"startPayAmount":0,"exceedingLimitAmount":0,"selfPay2":0,"selfPayAmount":10,"personalAccountPayAmount":0,"ownExpensePayAmount":10,"personalCashPayAmount":0,"yearFundTotalPayAmount":0,"cumulativeMedicalInsuranceRangeAmount":0,"retireSupplyMedicalInsurancePay":0,"unitSupplyMedicalInsurancePay":0,"yearLargeTotalPayAmount":0,"insuranceCompanyPaymentAmount":0,"otherThirdPayAmount":0,"thirdPartyPayAmount":0,"subjoinPayAmount":0,"claimDetailType":"1","insuredType":"1","socialSecurityPaymentAmount":0,"medicalFundPayAmount":0,"hospitalDays":0,"hospitalFlag":2,"repeatStatus":0,"repeatMsg":None,"billCode":"39675408","billName":"","billDate":"2023-02-20","caseStatus":None,"countDeductAmount":None,"diseaseNameBefore":"","diseaseName": diseaseName,"checkCode":"123456","checkAuthenticityStatus":"not_verified","checkAuthenticityStatusDesc":"未验真","imageTypeName":"增值税发票","imageType":"4","imageSubtype":"14","imageSubTypeName":"增值税发票","refusePaymentStatus":None,"remark":"","deductionAccount":None,"fixedPoint":0,"fixedPointName":"非定点","imageSeqNo":"GXlhl2023022000300001-1","settlementStatus":1,"settlementStatusName":"是","eventId":"1077953558902472704","eventNo":"20230222000005","accidentType":"200","accidentReason":"","accidentReasonName":"","healthStatus":"03","cureDesc":"01","deathDate":None,"deformityDate":None,"accidentProvince":"650000","accidentCity":"652700","accidentArea":"652723","accidentAddress":"四姑娘山","hospitalAddress":"","repeatReasons":"","repeatDescribe":"","accResult2":"O47","accResult2Name":"假临产","accResult1":"OO4","accResult1Name":"与胎儿和羊膜腔及可能的分娩问题有关的孕产妇医疗(O30-O48）","hospitalNo":"","visitName":"","checkStatus":None,"fundSelfPay":0,"largeSelfPay":0,"exceedingMedicalFund":0}
        data["caseBillDeductionDetails"] = [{"id":"1628273527700357121","batchId":"1627566278761807873","caseId":"1627566278849888257","batchNo":"GXlhl20230220003","caseNo":"GXlhl2023022000300001","costType":"AM002","quantity":1,"unitPrice":10,"deductAmount":0,"billId":"1077953040624910336","amount":10,"deductCause":"","createUser":None,"createTime":None,"updateUser":None,"updateTime":None,"delFlag":0,"costNameCode":"","surgicaNo":"","surgicalDiagnosisType":"","deductionCostReason":"99","selfPay1":10,"selfPay2":0,"ownExpensePayAmount":0,"insuranceCompanyPaymentAmount":0,"otherThirdPaymentAmount":0,"drugName":"心电监护(进口)1","selfRatio":0,"specification":"个","model":"","classAFee":None,"goodsCode":"BJZLML00000244","goodsId":"3371287","checkLabelCodes":None,"checkLabelNames":None,"principalInsuredIdType":"0","principalInsuredIdCode":"152701197712100618","saveFlag":1,"costTypeName":"诊察费","costName":None,"deductionCostReasonName":"其他","channel":"XH","index":0}]
        data["insuredInfoVo"] = {"insured":{"id":"1628273507467034625","batchId":"1627566278761807873","caseId":"1627566278849888257","batchNo":"GXlhl20230220003","caseNo":"GXlhl2023022000300001","customerNo":"4198648520","dutyPlanType":"","insuredName":"袁军","idType":"0","idCard":"152701197712100618","idCardAddress":"北京市巴拉巴拉","mobile":"13255121110","birthDate":"1977-12-10","age":0,"version":1,"isLongTerm":1,"occupationType": myjob,"startTime":"2011-02-18","endTime":"2199-12-31","belongToGroup": mybelongToGroup,"createUser":"lihailong","createTime":"2023-02-22 14:00:31","updateUser":"lihailong","updateTime":"2023-02-24 11:37:34","delFlag":0,"province":"110000","city":"110100","area":"110102","address":"巴拉巴拉","repeatMsg":"","socialAddress":"","insuredTag":0,"principalInsuredRelation":"00","isSameAddress":0,"insuredState":"CHN","sex":"0"},"insuredReceiver":{"id":"","bankName":"","bankAccount":"","insuredRelationship":"00","professionType":"","version":0,"createUser":"","createTime":None,"updateUser":"","updateTime":"","delFlag":0,"bankType":1},"applyPerson":{"id":"1628273507777413121","caseId":"1627566278849888257","batchId":"1627566278761807873","batchNo":"GXlhl20230220003","caseNo":"GXlhl2023022000300001","insuredRelationship":"00","applyName":"袁军","idType":"0","idCard":"152701197712100618","applyStartTime": applyStartTime,"applyEndTime":"2199-12-31","permanentFlag":0,"mobile":"13255121110","email":"","province":"110000","city":"110100","area":"110102","address":"巴拉巴拉","idCardAddress":"北京市巴拉巴拉","isSameAddress":0,"applyState":"CHN","createUser":"lihailong","createTime":"2023-02-22 14:00:31","updateUser":"lihailong","updateTime":"2023-02-24 11:37:34","delFlag":0,"birthdate":"1977-12-10","sex":"0"},"policyNo":"202012140933","insuranceApplicationId":"3","insuranceCompanyId":"1"}
        #print(r.json())
        return None

    #初审
    def firstReceive(self):

        #查询初审待领取列表
        data = {"nodeType":["04"],"page":{"current":1,"size":10},"claimTypeName": self.expenseTypeId,"exigency":"","policyNo": tpa_config.takeOrderParam[2],"enterCurrentNodeEndTime":"","enterCurrentNodeStartTime":"","insuranceCompanyId": self.companyId,"claimTypes":[self.expenseTypeId],"insuranceApplicationIds":[self.applicationId]}
        r = requests.post(tpa_config.url + "/tpaserver/tclaimcase/unCollected/page/list", headers=self.header, data=json.dumps(data))
        #print(r.json())
        try:
            caseNo = r.json()['data']['records'][0]['caseNo']
        except IndexError:
            print("初审池列表中没有符合条件的案件!")
            return None
        data = {}
        data['workSign'] = caseNo
        #领取返回的第一个案件号
        r = requests.post(tpa_config.url + "/tpaserver/fWorkFlowConf/receiveWorkflow", headers=self.header, data=json.dumps(data))
        print(r.json())
        return None

    #复审
    def secondReceive(self):

        #查询复审待领取列表
        data = {"nodeType":["05"],"page":{"current":1,"size":10},"claimTypeName": self.expenseTypeId,"claimTypes":[self.expenseTypeId],"insuranceApplicationIds":[self.applicationId],"insuranceCompanyId": self.companyId,"enterCurrentNodeStartTime":"","enterCurrentNodeEndTime":"","policyNo": tpa_config.takeOrderParam[2],"exigency":"","caseSecondStatus":""}
        r = requests.post(tpa_config.url + "/tpaserver/tclaimcase/unCollected/page/list", headers=self.header, data=json.dumps(data))
        print(r.json())
        try:
            caseNo = r.json()['data']['records'][0]['caseNo']
        except IndexError:
            print("复审池列表中没有符合条件的案件!")
            return None
        data = {}
        data['workSign'] = caseNo
        #领取返回的第一个案件号
        r = requests.post(tpa_config.url + "/tpaserver/fWorkFlowConf/receiveWorkflow", headers=self.header, data=json.dumps(data))
        print(r.json())
        return None


if __name__ == "__main__":
    n = 1
    tpa_log.logger.info("########### 脚本开始执行 #############\n")
    mytest = tpa_process()
    for i in range(n):
        mytest.takeOrder(tpa_config.takeOrderParam)
        mytest.submitMake()
        mytest.inputReceive()
        mytest.myInput(tpa_config.idCode)
        #mytest.dataReview()
        #mytest.firstReceive()
        mytest.secondReceive()
        pass
    tpa_log.logger.debug("########### 脚本执行结束 #############")
