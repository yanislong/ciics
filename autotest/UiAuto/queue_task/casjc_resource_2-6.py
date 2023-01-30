#!/usr/bin/env python3

import json, time, random, datetime, sys
import requests

import casjc_login
import casjc_config
import casjc_log_task


class resource():

    def __init__(self, account="gktest", userId=20650, entId=10066):
        self.header = {}
        self.url = casjc_config.global_url
        #申请，生成合同，确认参数销售经理账号
        self.saleraccount = "lihaifeng"
        self.header['Content-Type'] = "application/json"
        self.saleser = casjc_login.login(self.saleraccount,"Casjc@123",1)
        self.header['Token'] = self.saleser[0]
        self.salesuserid = self.saleser[1]
        #全局订单Id
        self.orderId = ""
        self.tryOrderId = ""
        #企业用户信息
        self.account = account
        self.userId = userId
        self.entId = entId
        #申请配置资源值
        self.pname = "斗罗大陆9层魂环理论" + str(random.randint(1,1000))
        self.phone = "18210462798"
        self.email = "18210462798@163.com"
        self.tmpnumber = 1
        self.corenumber = 2
        self.totalprice = 1000.24
        self.jobday = 1
        self.storeday = 10

    def applyTryOrder(self):

        """[申请试用资源(共享高性能和文件存储)]"""

        url = self.url + "/portal-test/order/order/addOrder"
        data = {"orderId":"","applyParty":1,"areaId":"1","avgDiscount":0,"deployWay":0,"discountPrice":0,"entCompanyId": self.entId,"entExist":0,"entMail": self.email,"entPhoneWay":1,"entPhone":"","entMobilePhone": self.phone,"entUserId": self.userId,"userRemark":"","productType":"1,3","projectName": self.pname, "salesUserId": self.salesuserid,"orderType":0,"status":1,"totalPrice":0,"giftPrice":5.12}
        data["resVOList"] = [{"areaId":1,"discount":0,"number":"1","orderResId":1,"price":0,"resId":62,"resTypeId":2,"resProdSrvId":1,"validDays":1,"validUnit":"天","unitPrice":0.12,"discountUnitPrice":0},{"areaId":1,"discount":0,"number":"1","orderResId":3,"price":0,"resId":106,"resTypeId":4,"resProdSrvId":3,"validDays":1,"validUnit":"天","unitPrice":5,"discountUnitPrice":0}]
        r = requests.post(url, headers=self.header, data=json.dumps(data))
        #print(r.json())
        self.tryOrderId = str(r.json()['data'])
        if r.json()['code'] == 200:
            casjc_log_task.logging.info(self.applyTryOrder.__doc__ + " 企业用户ID:" + str(self.userId) + " 订单号ID:" + self.tryOrderId)
            return True
        else:
            casjc_log_task.logging.info(self.applyTryOrder.__doc__ + " 企业用户ID:" + str(self.userId) + " 提交资源申请异常")
            return False

    def applyTryPrice(self):

        """[审批试用订单(共享高性能和文件存储)]"""

        #王楠审批试用
        url1 = self.url + "/portal-test/flow/task/apvList?businessId=" + self.tryOrderId + "&flowIds=1,2,3"
        header = {}
        header['Token'] = casjc_login.login(casjc_config.avpuser1, casjc_config.avppasswd, 1)[0]
        r1 = requests.get(url1, headers=header)
        #print(r.json())
        taskId = r1.json()['data'][0]['taskId']
        url2 = self.url + "/portal-test/order/order/apvOrder"
        header['Content-Type'] = "application/json"
        data2 = {}
        data2['opinion'] = "test"
        data2['status'] = 0
        data2['taskId'] = taskId - 1
        r2 = requests.post(url2, headers=header, data=json.dumps(data2))
        #print(r2.json())
        if r2.json()['code'] == 200 and r2.json()['message'] == None and r2.json()['data'] == None:
            casjc_log_task.logging.info(self.applyTryPrice.__doc__ + " 审批账号:" + casjc_config.avpuser1 + " 审批成功")
        else:
            casjc_log_task.logging.info(self.applyTryPrice.__doc__ + " 审批账号:" + casjc_config.avpuser1 + " 审批异常")
            return False

        #戴吉伟审批试用
        url3 = self.url + "/portal-test/flow/task/apvList?businessId=" + self.tryOrderId + "&flowIds=1,2,3"
        header['Token'] = casjc_login.login(casjc_config.avpuser2, casjc_config.avppasswd, 1)[0]
        r3 = requests.get(url3, headers=header)
        #print(r3.json())
        taskId = r3.json()['data'][0]['taskId']
        url4 = self.url + "/portal-test/order/order/apvOrder"
        data3 = {}
        data3['opinion'] = "test"
        data3['status'] = 0
        data3['taskId'] = taskId + 1
        r4 = requests.post(url4, headers=header, data=json.dumps(data3))
        #print(r4.json())
        if r4.json()['code'] == 200 and r4.json()['message'] == None and r4.json()['data'] == None:
            casjc_log_task.logging.info(self.applyTryPrice.__doc__ + " 审批账号:" + casjc_config.avpuser2 + " 审批成功")
            return True
        else:
            casjc_log_task.logging.info(self.applyTryPrice.__doc__ + " 审批账号:" + casjc_config.avpuser2 + " 审批异常")
            return False

 
    def confirmOrder(self):

        """[配置试用订单(共享高性能和文件存储)]"""

        #戴吉伟配置资源,获取必要参数
        url5 = self.url + "/portal-test/order/order/getOrder?times=1610011814514&orderId=" + self.tryOrderId
        header = {}
        header['Content-Type'] = "application/json"
        header['Token'] = casjc_login.login(casjc_config.avpuser2, casjc_config.avppasswd, 1)[0]
        r5 = requests.get(url5, headers=header)
        #print(r5.json())
        resInitId_file = r5.json()['data']['resInitVOList'][1]['resInitId']
        orderResId_file = r5.json()['data']['resVOList'][1]['orderResId']
        resInitId_job = r5.json()['data']['resInitVOList'][0]['resInitId']
        orderResId_job = r5.json()['data']['resVOList'][0]['orderResId']
        uptime = r5.json()['data']['resVOList'][0]['updateTime']

        #配置高性能计算
        url6 = self.url + "/portal-test/order/deploy/deployOrderRes"
        data = {}
        data["colonyId"] = 42
        data["defMemPerCpu"] = ""
        data["deployStatus"] = 3
        data["deployWay"] = 0
        data["endTime"] = time.strftime("20%y-%m-%d",time.localtime())
        data["entId"] = self.entId
        data["nodeList"] = ['low']
        data["number"] = 1
        data["orderId"] = self.tryOrderId
        data["orderResId"] = orderResId_job
        data["path"] = ""
        data["price"] = 0
        data["queueName"] = ""
        data["queueType"] = 0
        data["resInitId"] = resInitId_job
        data["resProdSrvId"] = 1
        data["resTypeId"] = 2
        data["startTime"] = time.strftime("20%y-%m-%d",time.localtime())
        data["updateTime"] = uptime
        ldata = []
        ldata.append(data)
        r6 = requests.post(url6, headers=header, data=json.dumps(ldata))
        #print(r6.json())
        if r6.json()['code'] == 200 and r6.json()['message'] == None and r6.json()['data'] == None:
            casjc_log_task.logging.info(self.confirmOrder.__doc__ + " 高性能资源配置完成, 配置人:" + casjc_config.avpuser2)
        else:
            casjc_log_task.logging.info(self.confirmOrder.__doc__ + " 高性能资源配置异常, 配置人:" + casjc_config.avpuser2)
            return False

        #配置文件存储
        data = {}
        data["colonyId"] = 43
        data["defMemPerCpu"] = ""
        data["deployStatus"] = 3
        data["deployWay"] = 0
        data["endTime"] = time.strftime("20%y-%m-%d",time.localtime())
        data["entId"] = self.entId
        data["nodeList"] = ['']
        data["number"] = 1
        data["orderId"] = self.tryOrderId
        data["orderResId"] = orderResId_file
        data["path"] = "/public1/home/" + self.account + "/" + self.account
        data["price"] = 0
        data["queueName"] = ""
        data["queueType"] = 0
        data["resInitId"] = resInitId_file
        data["resProdSrvId"] = 3
        data["resTypeId"] = 4
        data["startTime"] = time.strftime("20%y-%m-%d",time.localtime())
        data["updateTime"] = uptime
        ldata = []
        ldata.append(data)
        r7 = requests.post(url6, headers=header, data=json.dumps(ldata))
        #print(r7.json())
        if r7.json()['code'] == 200 and r7.json()['message'] == None and r7.json()['data'] == None:
            casjc_log_task.logging.info(self.confirmOrder.__doc__ + " 文件存储资源配置完成, 配置人:" + casjc_config.avpuser2)
            return True
        else:
            casjc_log_task.logging.info(self.confirmOrder.__doc__ + " 文件存储资源配置异常, 配置人:" + casjc_config.avpuser2)
            return False

    def applyOrder(self):

        """[申请新购资源 (共享高性能和文件存储)]"""

        url = self.url + "/portal-test/order/order/addOrder"
        data = {"orderId":"","applyParty":1,"areaId":"1","avgDiscount":1,"deployWay":1,"discountPrice":0,"entCompanyId": self.entId,"entExist":0,"entMail": self.email,"entPhoneWay":1,"entPhone":"","entMobilePhone": self.phone,"entUserId": self.userId,"userRemark":"","productType":"1,3","projectName": self.pname,"resVOList":[{"areaId":1,"discount":1,"number":1,"orderResId":1,"price":0.12,"resId":62,"resTypeId":2,"resProdSrvId":1,"validDays":10,"validUnit":"天","unitPrice":0.12,"discountUnitPrice":0.12},{"areaId":1,"discount":1,"number":1,"orderResId":3,"price":1000,"resId":141,"resTypeId":4,"resProdSrvId":3,"validDays": self.storeday,"validUnit":"天","unitPrice":100,"discountUnitPrice":100}],"salesUserId": self.salesuserid,"orderType":1,"status":1,"totalPrice": self.totalprice,"giftPrice":0}
        r = requests.post(url, headers=self.header, data=json.dumps(data))
        #print(r.json())
        self.orderId = str(r.json()['data'])
        if r.json()['code'] == 200:
            casjc_log_task.logging.info(self.applyOrder.__doc__ + " 企业用户ID:" + str(self.userId) + " 订单号ID:" + self.orderId)
            return True
        else:
            casjc_log_task.logging.info(self.applyOrder.__doc__ + " 企业用户ID:" + str(self.userId) + " 提交资源申请异常")
            return False

    def applyPrice(self):

        """[审批新购订单价格 (共享高性能和文件存储)]"""

        #王楠价格审批新购订单
        url1 = self.url + "/portal-test/flow/task/apvList?businessId=" + self.orderId + "&flowIds=1,2,3"
        header = {}
        header['Content-Type'] = "application/json"
        header['Token'] = casjc_login.login(casjc_config.avpuser1, casjc_config.avppasswd, 1)[0]
        r1 = requests.get(url1, headers=header)
        #print(r1.json())
        taskId = r1.json()['data'][0]['taskId']
        url2 = self.url + "/portal-test/order/order/apvOrder"
        header['Content-Type'] = "application/json"
        data2 = {}
        data2['opinion'] = "test"
        data2['status'] = 0
        data2['taskId'] = taskId - 1
        r2 = requests.post(url2, headers=header, data=json.dumps(data2))
        #print(r2.json())
        if r2.json()['code'] == 200 and r2.json()['message'] == None and r2.json()['data'] == None:
            casjc_log_task.logging.info(self.applyPrice.__doc__ + " 审批账号:" + casjc_config.avpuser1 + " 审批成功")
            return True
        else:
            casjc_log_task.logging.info(self.applyPrice.__doc__ + " 审批账号:" + casjc_config.avpuser1 + " 审批异常")
            return False

    def generateContract(self):

        """[销售经理生成新购订单合同]"""

        #提单销售经理生成合同
        #1.获取生成合同的必要参数
        curl1 = self.url + "/portal-test/order/order/getOrder?orderId=" + self.orderId
        cr1 = requests.get(curl1, headers=self.header)
        #print(cr1.json())
        orderNo = cr1.json()['data']['orderNumber']
        suserid = cr1.json()['data']['salesUserId']
        eid = cr1.json()['data']['entCompanyId']
        ename = cr1.json()['data']['entCompanyName']
        euserid = cr1.json()['data']['entUserId']
        tprice = cr1.json()['data']['totalPrice']
        if cr1.json()['code'] == 200:
            casjc_log_task.logging.info(self.generateContract.__doc__ + " 操作账号:" + self.saleraccount + " 获取生成合同必要参数成功")
        else:
            casjc_log_task.logging.info(self.generateContract.__doc__ + " 操作账号:" + self.saleraccount + " 获取生成合同必要参数异常")
            return False

        #2.获取订单taskid
        curl2 = self.url + "/portal-test/order/order/apvOrderList"
        data2 = {}
        data2['pageNum'] = 1
        data2['pageSize'] = 20
        taskid = None
        cr2 = requests.post(curl2, headers=self.header, data=json.dumps(data2))
        for i in cr2.json()['data']['list']:
            if str(i['orderId']) == str(self.orderId):
                taskid = i['taskId']
                break
        if cr2.json()['code'] == 200 and taskid:
            casjc_log_task.logging.info(self.generateContract.__doc__ + " 操作账号:" + self.saleraccount + " 获取生成合同必要参数taskid成功: " + str(taskid))
        else:
            casjc_log_task.logging.info(self.generateContract.__doc__ + " 操作账号:" + self.saleraccount + " 获取生成合同必要参数taskid异常")
            return False

        #3.获取合同编号
        curl3 = self.url + "/portal-test/contract/contractInfo/generateContractNumber?signTime="# + str(time.strftime("20%y-%m-%d",time.localtime()))
        cr3 = requests.get(curl3, headers=self.header)
        #print(cr3.json())
        contractNo = cr3.json()['data']
        if cr3.json()['code'] == 200:
            casjc_log_task.logging.info(self.generateContract.__doc__ + " 操作账号:" + self.saleraccount + " 获取生成合同必要参数合同编号成功")
        else:
            casjc_log_task.logging.info(self.generateContract.__doc__ + " 操作账号:" + self.saleraccount + " 获取生成合同必要参数合同编号异常")
            return False

        #4.上传合同文件，获取合同附件信息
        curl4 = self.url + "/portal-test/file/uploadFile/group1"
        tmpheader = {}
        tmpheader['Token'] = self.saleser[0]
        with open('/home/yanislong/myPerformance/UiAuto/queue_task/运维-世纪互联网络运维实践-李信满-世纪互联-下载版.pdf','rb') as f:
            myfile = {'file': f.read()}
        cr4 = requests.post(curl4, headers=tmpheader, files=myfile)
        #print(cr4.json())
        fpath = cr4.json()['data']['filePath']
        orginname = cr4.json()['data']['originalName']
        upname = cr4.json()['data']['uploadName']
        uptime = cr4.json()['data']['uploadDate']
        vurl = cr4.json()['data']['viewUrl']
        if cr4.json()['code'] == 200:
            casjc_log_task.logging.info(self.generateContract.__doc__ + " 操作账号:" + self.saleraccount + " 获取生成合同必要参数合同附件成功")
        else:
            casjc_log_task.logging.info(self.generateContract.__doc__ + " 操作账号:" + self.saleraccount + " 获取生成合同必要参数合同附件异常")
            return False

        #5.提交生成合同
        curl5 = self.url + "/portal-test/contract/contractInfo/save"
        now_time = datetime.datetime.now()
        cdata = {}
        cdata["taskId"] = taskid
        cdata["orderId"] = self.orderId
        cdata["entCompanyId"] = eid
        cdata["entUserId"] = euserid
        cdata["orderNo"] = orderNo
        cdata["entCompanyName"] = ename
        cdata["sealId"] = 16
        cdata["signTime"] =  time.strftime("20%y-%m-%d",time.localtime())
        cdata["contractNo"] = contractNo
        cdata["sendGoodsTime"] =  time.strftime("20%y-%m-%d",time.localtime())
        cdata["serviceBeginTime"] =  time.strftime("20%y-%m-%d",time.localtime())
        cdata["serviceFinishTime"] = (now_time+datetime.timedelta(days=+1)).strftime("%Y-%m-%d")
        cdata["contractAmount"] = tprice
        cdata["contractPro"] = "2"
        cdata["contractFileVOs"] = [{"fileName": orginname,"filePath": fpath,"fileUrl": vurl,"uploadBy": upname,"uploadTime": uptime}]
        cdata["contractPayTermsVOs"] = [{"payPercentage":1,"payTerms":"1","termsType":"1","termsTypeName":"签署合同"}]
        cr5 = requests.post(curl5, headers=self.header, data=json.dumps(cdata))
        #print(cr5.json())
        if cr5.json()['code'] == 200:
            casjc_log_task.logging.info(self.generateContract.__doc__ + " 操作账号:" + self.saleraccount + " 生成合同成功")
            return True
        else:
            casjc_log_task.logging.info(self.generateContract.__doc__ + " 操作账号:" + self.saleraccount + " 生成合同异常")
            return False
   
    def exaContract(self):

        """[审批新购订单合同]"""

        #合同审批 王楠
        url3 = self.url + "/portal-test/flow/task/apvList?businessId=" + self.orderId + "&flowIds=1,2,3"
        header = {}
        header['Content-Type'] = "application/json"
        header['Token'] = casjc_login.login(casjc_config.conuser1, casjc_config.avppasswd, 1)[0]
        r3 = requests.get(url3, headers=header)
        #print(r3.json())
        taskId = r3.json()['data'][-1]['taskId']
        url4 = self.url + "/portal-test/order/order/apvOrder"
        data3 = {}
        data3['opinion'] = "test"
        data3['status'] = 0
        data3['taskId'] = taskId - 1
        r4 = requests.post(url4, headers=header, data=json.dumps(data3))
        #print(r4.json())
        if r4.json()['code'] == 200 and r4.json()['message'] == None and r4.json()['data'] == None:
            casjc_log_task.logging.info(self.exaContract.__doc__ + " 审批账号:" + casjc_config.conuser1 + " 审批成功")
        else:
            casjc_log_task.logging.info(self.exaContract.__doc__ + " 审批账号:" + casjc_config.conuser1 + " 审批异常")
            return False

        #合同审批 孔水水
        url5 = self.url + "/portal-test/flow/task/apvList?businessId=" + self.orderId + "&flowIds=1,2,3"
        header['Token'] = casjc_login.login(casjc_config.conuser2, casjc_config.avppasswd, 1)[0]
        r5 = requests.get(url5, headers=header)
        #print(r5.json())
        taskId = r5.json()['data'][2]['taskId']
        url6 = self.url + "/portal-test/order/order/apvOrder"
        data3 = {}
        data3['opinion'] = "test"
        data3['status'] = 0
        data3['taskId'] = taskId + 1
        r6 = requests.post(url6, headers=header, data=json.dumps(data3))
        #print(r6.json())
        if r6.json()['code'] == 200 and r6.json()['message'] == None and r6.json()['data'] == None:
            casjc_log_task.logging.info(self.exaContract.__doc__ + " 审批账号:" + casjc_config.conuser2 + " 审批成功")
        else:
            casjc_log_task.logging.info(self.exaContract.__doc__ + " 审批账号:" + casjc_config.conuser2 + " 审批异常")
            return False

        #合同审批 刘凯敏
        url7 = self.url + "/portal-test/flow/task/apvList?businessId=" + self.orderId + "&flowIds=1,2,3"
        header['Token'] = casjc_login.login(casjc_config.conuser3, casjc_config.avppasswd, 1)[0]
        r7 = requests.get(url7, headers=header)
        #print(r7.json())
        taskId = r7.json()['data'][-1]['taskId']
        url8 = self.url + "/portal-test/order/order/apvOrder"
        data3 = {}
        data3['opinion'] = "test"
        data3['status'] = 0
        data3['taskId'] = taskId + 1
        r8 = requests.post(url8, headers=header, data=json.dumps(data3))
        #print(r8.json())
        if r8.json()['code'] == 200 and r8.json()['message'] == None and r8.json()['data'] == None:
            casjc_log_task.logging.info(self.exaContract.__doc__ + " 审批账号:" + casjc_config.conuser3 + " 审批成功")
            return True
        else:
            casjc_log_task.logging.info(self.exaContract.__doc__ + " 审批账号:" + casjc_config.conuser3 + " 审批异常")
            return False

    def confirmParam(self, mytype="All"):

        """[销售经理新购订单确认参数]"""

        if mytype != "All":
            self.tmpnumber = 2
            self.corenumber = 1
        #获取确认参数接口所需必要参数
        turl = self.url + "/portal-test/order/order/getOrder?times=1610011814514&orderId=" + self.orderId
        tr = requests.get(turl, headers=self.header)
        #print(tr.json())
        resInitId_file = tr.json()['data']['resInitVOList'][1]['resInitId']
        orderResId_file = tr.json()['data']['resVOList'][1]['orderResId']
        resInitId_job = tr.json()['data']['resInitVOList'][0]['resInitId']
        orderResId_job = tr.json()['data']['resVOList'][0]['orderResId']
        uptime = tr.json()['data']['resVOList'][0]['updateTime']
        if tr.json()['code'] == 200 and tr.json()['message'] == None:
            casjc_log_task.logging.info(self.confirmParam.__doc__ + " 操作账号:" + self.saleraccount + " 获取成功")
        else:
            casjc_log_task.logging.info(self.confirmParam.__doc__ + " 操作账号:" + self.saleraccount + " 获取异常")
            return False

        #销售经理确认参数
        url9 = casjc_config.global_url + "/portal-test/order/deploy/updateOrderRes"
        data9 = {"totalPrice": self.totalprice,"discountPrice": self.totalprice,"orderId": self.orderId}
        resjob = {"orderResId": orderResId_job,"resProdSrvId":1,"resTypeId":2,"resId":62,"number": self.corenumber,"validDays":10,"validUnit":"天","discount":1,"price":0.12,"unitPrice":0.12,"technicalNorms":"AMD EPYC 7742 64-Core Processor","resourceName":"双路计算节点","typeName":"共享型","productName":"高性能计算","compuResource": None,"chargeUnitCode":"2","chargeUnitDesc":"核心","chargeCycleCode":"6","chargeCycleDesc":"时","technicalId": None,"startTime": time.strftime("20%y-%m-%d",time.localtime()),"endTime": time.strftime("20%y-%m-%d",time.localtime()),"deployStatus":1,"queueName": None,"updateTime": uptime,"updateStatus":0,"defMemPerCpu": None,"deployAccount": None,"discountUnitPrice":0.12,"usedNumber": None,"leaveNumber": None,"colonyId": None,"leaveCount": None,"resCloudList": None,"areaId":1,"areaInfo":"太原一区","isInit":1,"renewOrderResId": None,"resInitId": None,"usedCount":0,"freeUsedCount":0,"freeBeingCount":0}
        resstore = {"orderResId": orderResId_file,"resProdSrvId":3,"resTypeId":4,"resId":141,"number": self.storeday / self.tmpnumber,"validDays": self.storeday,"validUnit":"天","discount":1,"price":1000 / self.tmpnumber,"unitPrice":100,"technicalNorms":"高性能并行存储（160GB/s聚合带宽、360TB SSD、18PB SAS/SATA），以TB天为单位","resourceName":"资源名称093307","typeName":"文件存储","productName":"数据存储","compuResource": None,"chargeUnitCode":"10","chargeUnitDesc":"TB","chargeCycleCode":"5","chargeCycleDesc":"天","technicalId": None,"startTime": time.strftime("20%y-%m-%d",time.localtime()),"endTime": time.strftime("20%y-%m-%d",time.localtime()),"deployStatus":1,"queueName": None,"updateTime": uptime,"updateStatus":0,"defMemPerCpu": None,"deployAccount": None,"discountUnitPrice":100,"usedNumber": None,"leaveNumber": None,"colonyId": None,"leaveCount": None,"resCloudList": None,"areaId":1,"areaInfo":"太原一区","isInit":1,"renewOrderResId": None,"resInitId": None,"usedCount":0,"freeUsedCount":0,"freeBeingCount":0}
        data9["orderResList"] = []
        data9["orderResList"].append(resjob)
        data9["orderResList"].append(resstore)
        r9 = requests.post(url9, headers=self.header, data=json.dumps(data9))
        #print(r9.content)
        if r9.json()['code'] == 200 and r9.json()['message'] == None and r9.json()['data'] == None:
            casjc_log_task.logging.info(self.confirmParam.__doc__ + " 操作账号:" + self.saleraccount + " 确认参数成功")
            return True
        else:
            casjc_log_task.logging.info(self.confirmParam.__doc__ + " 操作账号:" + self.saleraccount + " 确认参数异常")
            return False
        
    def confirmAll(self, mytype="All"):

        """[配置新购资源,全部配置]"""

        title = "[配置新购资源,全部配置]"
        if mytype != "All":
            self.tmpnumber = 2
            self.corenumber = 1
            title = "[配置新购资源,部分配置]"

        #戴吉伟配置资源,获取必要参数
        url10 = self.url + "/portal-test/order/order/getOrder?times=1610011814514&orderId=" + self.orderId
        header = {}
        header['Content-Type'] = "application/json"
        header['Token'] = casjc_login.login(casjc_config.avpuser2, casjc_config.avppasswd, 1)[0]
        r10 = requests.get(url10, headers=header)
        #print(r10.json())
        resInitId_file = r10.json()['data']['resInitVOList'][1]['resInitId']
        orderResId_file = r10.json()['data']['resVOList'][1]['orderResId']
        resInitId_job = r10.json()['data']['resInitVOList'][0]['resInitId']
        orderResId_job = r10.json()['data']['resVOList'][0]['orderResId']
        uptime = r10.json()['data']['resVOList'][0]['updateTime']


        #配置高性能计算
        url11 = self.url + "/portal-test/order/deploy/deployOrderRes"
        data = {}
        data["colonyId"] = 42
        data["defMemPerCpu"] = ""
        data["deployStatus"] = ""
        data["deployWay"] = 1
        data["endTime"] = time.strftime("20%y-%m-%d",time.localtime())
        data["entId"] = self.entId
        data["nodeList"] = ['low']
        data["number"] = self.corenumber
        data["orderId"] = self.orderId
        data["orderResId"] = orderResId_job
        data["path"] = "/public1/home/" + self.account + "/" + self.account
        data["price"] = 0.12 * self.corenumber
        data["queueName"] = ""
        data["queueType"] = 0
        data["resInitId"] = resInitId_job
        data["resProdSrvId"] = 1
        data["resTypeId"] = 2
        data["startTime"] = time.strftime("20%y-%m-%d",time.localtime())
        data["updateTime"] = uptime
        ldata = []
        ldata.append(data)
        r11 = requests.post(url11, headers=header, data=json.dumps(ldata))
        #print(r11.json())
        if r11.json()['code'] == 200 and r11.json()['message'] == None and r11.json()['data'] == None:
            casjc_log_task.logging.info(title + " 高性能资源配置完成, 配置人:" + casjc_config.avpuser2)
        else:
            casjc_log_task.logging.info(title + " 高性能资源配置异常, 配置人:" + casjc_config.avpuser2)
            return False

        #配置文件存储
        data = {}
        data["colonyId"] = 43
        data["defMemPerCpu"] = ""
        data["deployStatus"] = ""
        data["deployWay"] = 1
        data["endTime"] = time.strftime("20%y-%m-%d",time.localtime())
        data["entId"] = self.entId
        data["nodeList"] = ['']
        data["number"] = self.storeday / self.tmpnumber
        data["orderId"] = self.orderId
        data["orderResId"] = orderResId_file
        data["path"] = "/public1/home/" + self.account + "/" + self.account
        data["price"] = 1000 / self.tmpnumber
        data["queueName"] = ""
        data["queueType"] = 0
        data["resInitId"] = resInitId_file
        data["resProdSrvId"] = 3
        data["resTypeId"] = 4
        data["startTime"] = time.strftime("20%y-%m-%d",time.localtime())
        data["updateTime"] = uptime
        ldata = []
        ldata.append(data)
        r12 = requests.post(url11, headers=header, data=json.dumps(ldata))
        #print(r12.json())
        if r12.json()['code'] == 200 and r12.json()['message'] == None and r12.json()['data'] == None:
            casjc_log_task.logging.info(title + " 文件存储资源配置完成, 配置人:" + casjc_config.avpuser2)
            return True
        else:
            casjc_log_task.logging.info(title + " 文件存储资源配置异常, 配置人:" + casjc_config.avpuser2)
            return False

    def renewResource(self):

        """[续期资源结束日期加一天,共享存储和共享计算]"""

        #销售经理配置资源,获取必要参数
        url0 = self.url + "/portal-test/order/order/getOrder?times=1610011814514&orderId=" + self.orderId
        r0 = requests.get(url0, headers=self.header)
        #print(r0.json())
        orderResId_job = r0.json()['data']['resVOList'][0]['orderResId']
        endtime_j = r0.json()['data']['resVOList'][0]['endTime']
        orderResId_file = r0.json()['data']['resVOList'][1]['orderResId']
        endtime_f = r0.json()['data']['resVOList'][1]['endTime']

        #获取资源结束日期，然后加1天
        y, m, d = time.strptime(endtime_j,"%Y-%m-%d")[:3]
        endtime_job = (datetime.datetime(y,m,d) + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        y2, m2, d2 = time.strptime(endtime_j,"%Y-%m-%d")[:3]
        endtime_file = (datetime.datetime(y2,m2,d2) + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

        url = self.url + "/portal-test/order/deploy/extendValidity"
        data = [{"resTypeId":2,"orderId": self.orderId,"orderResId": orderResId_job,"endTime": endtime_job,"price":0,"diffPrice":0.12},{"resTypeId":4,"orderId": self.orderId,"orderResId": orderResId_file,"endTime": endtime_file,"price":500,"diffPrice":500}]
        r = requests.post(url, headers=self.header, data=json.dumps(data))
        #print(r.json())
        try:
            if r.json()['code'] == 200 and r.json()['message'] == None and r.json()['data'] == None:
                casjc_log_task.logging.info(self.renewResource.__doc__ + " 续期成功，存储结束日期:" + str(endtime_file) +  " 共享高性能结束日期:" + str(endtime_job) + ", 配置人:" + self.saleraccount)
                return True
            else:
                casjc_log_task.logging.info(self.renewResource.__doc__ + " 续期异常, 配置人:" + self.saleraccount + json.dumps(r.json()))
                return False
        except KeyError:
            casjc_log_task.logging.info(self.renewResource.__doc__ + " 续期异常, 配置人:" + self.saleraccount + json.dumps(r.json()))
            return False

    def testTry(self):
        self.applyTryOrder()
        self.applyTryPrice()
        self.confirmOrder()

    def testNew(self, mytype="All"):
        self.applyOrder()
        self.applyPrice()
        self.generateContract()
        self.exaContract()
        self.confirmParam(mytype)
        self.confirmAll(mytype)

    def testRenew(self, mytype="half"):
        self.applyOrder()
        self.applyPrice()
        self.generateContract()
        self.exaContract()
        self.confirmParam(mytype)
        self.confirmAll(mytype)
        #配置完存储后需要等给用户配置完成在进行续期
        time.sleep(30)
        self.renewResource()

if __name__ == "__main__":
    mytest = resource()

    try:
        if sys.argv[1] == "1":
            mytest.testNew()
        elif sys.argv[1] == "0":
            mytest.testTry()
    except IndexError:
        print('not have parames')
        

    #试用
    #mytest.testTry()

    #新购
    #mytest.testNew()
    #mytest.testNew("half")

    #续期
    #mytest.testRenew()
