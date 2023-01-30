#!/usr/bin/env python3

import json, time, random, datetime, sys
import requests

import casjc_login
import casjc_config
import casjc_log_task
import casjc_user


class resource():

    def __init__(self, account="gktest", userId=20650, entId=10066):
        self.header = {}
        self.url = casjc_config.global_url
        #申请，生成合同，确认参数销售经理账号
        #self.saleraccount = "lihaifeng"
        self.saleraccount = "baishi"
        self.header['Content-Type'] = "application/json"
        self.saleser = casjc_login.login(self.saleraccount,"Casjc@123",1)
        self.header['Token'] = self.saleser[0]
        self.salesuserid = self.saleser[1]
        #全局订单Id
        self.orderId = "3438"
        self.tryOrderId = ""
        #企业用户信息
        self.account = account
        self.userId = userId
        self.entId = entId
        self.entName = "国科北京分部"
        #申请配置资源值
        self.pname = "斗罗大陆9层魂环理论" + str(random.randint(1,1000))
        self.phone = "18210462798"
        self.email = "18210462798@163.com"
        self.tmpnumber = 1
        self.corenumber = 2
        self.tprice = 5.12
        self.jobday = 1
        self.storeday = 10
        self.preDeploy = 0  #是否提前配置 0否1是
        self.deployWay = 0  #资源配置方式，0固定参数1灵活配置
        self.payWay = 0 #付费方式 0预付费1后付费

    def applyOrder(self, orderType):

        """[申请试用资源(共享高性能和文件存储)]"""

        if orderType not in (0,1,4):
            print("参数必须为0,1,4")
            return None
        url = self.url + "/portal-test/order/order/addOrder"
        data = {}
        data["orderId"] = "" 
        data["applyParty"] = 1  #提交申请方 0甲方,1销售经理
        data["entExist"] = 0  #甲方账号是否存在 0存在1不存在
        data[ "salesUserId"] = self.salesuserid
        data["projectName"] = self.pname
        data["entMail"] =  self.email
        data["entCompanyId"] =  self.entId
        data["entMobilePhone"] =  self.phone
        data["entUserId"] =  self.userId
        data["entPhoneWay"] = 1  #甲方联系电话方式0固定电话1手机
        data["entPhone"] = ""  #甲方联系电话 0固定电话时填写
        data["userRemark"] = ""  #用户账号不存在时备注
        data["orderType"] = orderType  # 订单类型 0试用1新购2续购3退订
        data["resVOList"] = []
        resinfo = {}  #文件存储
        resinfo["areaId"] = 1  #服务区ID
        resinfo["discount"] = 1  #折扣
        resinfo["number"] = 1  #申请数量
        resinfo["price"] = 5  #成交总价
        resinfo["resId"] = 28  #资源表ID
        resinfo["resTypeId"] = 4  #资源类型ID
        resinfo["resProdSrvId"] = 1  #资源产品服务ID
        resinfo["validDays"] = 1  #有效期
        resinfo["validUnit"] = "天"  #有效期单位
        resinfo["unitPrice"] = "5.00"  #标准单价
        resinfo["discountUnitPrice"] = "5.00"  #成交单价
        resinfo["costAccounting"] = 1  #成本核算
        resinfo["costUnit"] = ""  #成本核算单位
        resinfo["costPrice"] = 5  #成本总价
        resinfo["profitPrice"] = 0  #利润总价
        resinfo["originalPrice"] = 5  #标准总价
        resinfo2 = {}  #共享计算
        resinfo2["areaId"] = 1  #服务区ID
        resinfo2["discount"] = 1  #折扣
        resinfo2["number"] = 1  #申请数量
        resinfo2["price"] = 0.12  #成交总价
        resinfo2["resId"] = 194  #资源表ID
        resinfo2["resTypeId"] = 2  #资源类型ID
        resinfo2["resProdSrvId"] = 2  #资源产品服务ID
        resinfo2["validDays"] = 1  #有效期
        resinfo2["validUnit"] = "天"  #有效期单位
        resinfo2["unitPrice"] = "0.12"  #标准单价
        resinfo2["discountUnitPrice"] = "0.12"  #成交单价
        resinfo2["costAccounting"] = 1  #成本核算
        resinfo2["costUnit"] = ""  #成本核算单位
        resinfo2["costPrice"] = 0.12  #成本总价
        resinfo2["profitPrice"] = 0  #利润总价
        resinfo2["originalPrice"] = 0.12  #标准总价
        data["areaId"] = "1"  #服务区
        data["avgDiscount"] = 1  #平均折扣/最低折扣\n配置方式\n0固定参数：平均折扣\n1灵活配置：最低折扣
        data["discountPrice"] = 0  #优惠总额，单位：元
        data["productType"] = "1,2"  #产品类型 1 标准型 2共享型
        data["resType"] = "3,6"  #资源类型：前端暂存使用
        data["status"] = 1  #状态 1:待审批 2:乙方盖章 3:待邮寄 4:甲方盖章 5:待寄回 6:已寄回 7:已过期 8:作废待审批 9:已作废 10:待归档 11:已归档	
        data["totalPrice"] = 5.12  #成交总额，单位：元
        data["giftPrice"] = "0"  #赠送金额，单位：元
        data["originalPrice"] = self.tprice  #标准总价
        data["costPrice"] = 5.12  #成本总价，单位：元
        data["profitPrice"] = -5.12  #利润总价，单位：元
        data['contractInfoVO'] = {} 

        if data['orderType'] == 0:
            data["preDeploy"] = 0  #是否提前配置 0否1是
            data["deployWay"] = 0  #资源配置方式，0固定参数1灵活配置
            data["payWay"] = 0  #付费方式 0预付费1后付费
            data['resVOList'].append(resinfo)
            data['resVOList'].append(resinfo2)
        elif data['orderType'] == 1:
            data["preDeploy"] = self.preDeploy  #是否提前配置 0否1是
            data["deployWay"] = self.deployWay  #资源配置方式，0固定参数1灵活配置
            data["payWay"] = self.payWay  #付费方式 0预付费1后付费
            data['resVOList'].append(resinfo)
            data['resVOList'].append(resinfo2)

            """[生成订单合同]"""
            #2.获取盖章机构
            curl2 = self.url + "/portal-test/contract/getContractSealUserAll"
            cr2 = requests.post(curl2, headers=self.header)
            #print(cr2.json())
            sealId = cr2.json()['data'][0]['id']
            if cr2.json()['code'] == 200:
                casjc_log_task.logging.info(self.applyOrder.__doc__ + " 操作账号:" + self.saleraccount + " 获取生成合同必要参数合同编号成功")
            else:
                casjc_log_task.logging.info(self.applyOrder.__doc__ + " 操作账号:" + self.saleraccount + " 获取生成合同必要参数合同编号异常")
                return False

            #3.获取合同编号
            curl3 = self.url + "/portal-test/contract/contractInfo/generateContractNumber?signTime="# + str(time.strftime("20%y-%m-%d",time.localtime()))
            cr3 = requests.get(curl3, headers=self.header)
            #print(cr3.json())
            contractNo = cr3.json()['data']
            if cr3.json()['code'] == 200:
                casjc_log_task.logging.info(self.applyOrder.__doc__ + " 操作账号:" + self.saleraccount + " 获取生成合同必要参数合同编号成功")
            else:
                casjc_log_task.logging.info(self.applyOrder.__doc__ + " 操作账号:" + self.saleraccount + " 获取生成合同必要参数合同编号异常")
                return False

            #4.上传合同文件，获取合同附件信息
            curl4 = self.url + "/portal-test/file/uploadFile/group1"
            tmpheader = {}
            tmpheader['Token'] = self.saleser[0]
            with open('/root/运维-世纪互联网络运维实践-李信满-世纪互联-下载版.pdf','rb') as f:
                myfile = {'file': f.read()}
            cr4 = requests.post(curl4, headers=tmpheader, files=myfile)
            #print(cr4.json())
            fpath = cr4.json()['data']['filePath']
            orginname = cr4.json()['data']['originalName']
            upname = cr4.json()['data']['uploadName']
            uptime = cr4.json()['data']['uploadDate']
            vurl = cr4.json()['data']['viewUrl']
            if cr4.json()['code'] == 200:
                casjc_log_task.logging.info(self.applyOrder.__doc__ + " 操作账号:" + self.saleraccount + " 获取生成合同必要参数合同附件成功")
            else:
                casjc_log_task.logging.info(self.applyOrder.__doc__ + " 操作账号:" + self.saleraccount + " 获取生成合同必要参数合同附件异常")
                return False
            now_time = datetime.datetime.now()
            cdata = {}
            cdata["id"] = ""
            cdata["entCompanyId"] = self.entId
            cdata["entUserId"] = self.userId
            cdata["entCompanyName"] = self.entName
            cdata["sealId"] = sealId
            cdata["signTime"] =  "" #time.strftime("20%y-%m-%d",time.localtime())
            cdata["contractNo"] = contractNo
            cdata["sendGoodsTime"] =  time.strftime("20%y-%m-%d",time.localtime())
            cdata["serviceBeginTime"] =  time.strftime("20%y-%m-%d",time.localtime())
            cdata["serviceFinishTime"] = (now_time+datetime.timedelta(days=+1)).strftime("%Y-%m-%d")
            cdata["contractAmount"] = self.tprice
            cdata["originalPrice"] = self.tprice
            cdata["contractPro"] = 2
            cdata["contractFileVOs"] = [{"fileName": orginname,"filePath": fpath,"fileUrl": vurl,"uploadBy": upname,"uploadTime": uptime}]
            cdata["contractPayTermsVOs"] = [{"payPercentage":1,"payTerms":"1","termsType":"1","termsTypeName":"签署合同"}]
            cdata['remark'] = "TEST"
            data['contractInfoVO'] = cdata
        elif data['orderType'] == 4:
            data["productType"] = ""  #产品类型 1 标准型 2共享型
            data["preDeploy"] = self.preDeploy  #是否提前配置 0否1是
            data["deployWay"] = 1  #资源配置方式，0固定参数1灵活配置
            data["payWay"] = 0  #付费方式 0预付费1后付费
            data['resVOList'] = []

            """[生成订单合同]"""
            #2.获取盖章机构
            curl2 = self.url + "/portal-test/contract/getContractSealUserAll"
            cr2 = requests.post(curl2, headers=self.header)
            #print(cr2.json())
            sealId = cr2.json()['data'][0]['id']
            if cr2.json()['code'] == 200:
                casjc_log_task.logging.info(self.applyOrder.__doc__ + " 操作账号:" + self.saleraccount + " 获取生成合同必要参数合同编号成功")
            else:
                casjc_log_task.logging.info(self.applyOrder.__doc__ + " 操作账号:" + self.saleraccount + " 获取生成合同必要参数合同编号异常")
                return False

            #3.获取合同编号
            curl3 = self.url + "/portal-test/contract/contractInfo/generateContractNumber?signTime="# + str(time.strftime("20%y-%m-%d",time.localtime()))
            cr3 = requests.get(curl3, headers=self.header)
            #print(cr3.json())
            contractNo = cr3.json()['data']
            if cr3.json()['code'] == 200:
                casjc_log_task.logging.info(self.applyOrder.__doc__ + " 操作账号:" + self.saleraccount + " 获取生成合同必要参数合同编号成功")
            else:
                casjc_log_task.logging.info(self.applyOrder.__doc__ + " 操作账号:" + self.saleraccount + " 获取生成合同必要参数合同编号异常")
                return False

            #4.上传合同文件，获取合同附件信息
            curl4 = self.url + "/portal-test/file/uploadFile/group1"
            tmpheader = {}
            tmpheader['Token'] = self.saleser[0]
            with open('/root/运维-世纪互联网络运维实践-李信满-世纪互联-下载版.pdf','rb') as f:
                myfile = {'file': f.read()}
            cr4 = requests.post(curl4, headers=tmpheader, files=myfile)
            #print(cr4.json())
            fpath = cr4.json()['data']['filePath']
            orginname = cr4.json()['data']['originalName']
            upname = cr4.json()['data']['uploadName']
            uptime = cr4.json()['data']['uploadDate']
            vurl = cr4.json()['data']['viewUrl']
            if cr4.json()['code'] == 200:
                casjc_log_task.logging.info(self.applyOrder.__doc__ + " 操作账号:" + self.saleraccount + " 获取生成合同必要参数合同附件成功")
            else:
                casjc_log_task.logging.info(self.applyOrder.__doc__ + " 操作账号:" + self.saleraccount + " 获取生成合同必要参数合同附件异常")
                return False
            now_time = datetime.datetime.now()
            cdata = {}
            cdata["id"] = ""
            cdata["entCompanyId"] = self.entId
            cdata["entUserId"] = self.userId
            cdata["entCompanyName"] = self.entName
            cdata["sealId"] = sealId
            cdata["signTime"] =  "" #time.strftime("20%y-%m-%d",time.localtime())
            cdata["contractNo"] = contractNo
            cdata["sendGoodsTime"] =  time.strftime("20%y-%m-%d",time.localtime())
            cdata["serviceBeginTime"] =  time.strftime("20%y-%m-%d",time.localtime())
            cdata["serviceFinishTime"] = (now_time+datetime.timedelta(days=+1)).strftime("%Y-%m-%d")
            cdata["contractAmount"] = self.tprice
            cdata["originalPrice"] = self.tprice
            cdata["contractPro"] = 2
            cdata["contractFileVOs"] = [{"fileName": orginname,"filePath": fpath,"fileUrl": vurl,"uploadBy": upname,"uploadTime": uptime}]
            cdata["contractPayTermsVOs"] = [{"payPercentage":1,"payTerms":"1","termsType":"1","termsTypeName":"签署合同"}]
            cdata['remark'] = "TEST"
            data['contractInfoVO'] = cdata

        r = requests.post(url, headers=self.header, data=json.dumps(data))
        print(r.json())
        self.orderId = str(r.json()['data'])
        if r.json()['code'] == 200:
            casjc_log_task.logging.info(self.applyOrder.__doc__ + " 企业用户ID:" + str(self.userId) + " 订单号ID:" + self.orderId)
            return True
        else:
            casjc_log_task.logging.info(self.applyOrder.__doc__ + " 企业用户ID:" + str(self.userId) + " 提交资源申请异常")
            return False

    def applyTryPrice(self):

        """[审批试用订单(共享高性能和文件存储)]"""

        time.sleep(5)
        #王楠审批试用
        url1 = self.url + "/portal-test/flow/task/apvList?businessId=" + self.orderId + "&flowIds=1,2,3,8,9,10"
        header = {}
        header['Token'] = casjc_login.login(casjc_config.avpuser1, casjc_config.avppasswd, 1)[0]
        r1 = requests.get(url1, headers=header)
        print(r1.json())
        taskId = r1.json()['data'][0]['taskId']
        url2 = self.url + "/portal-test/order/approve/apvOrder"
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

        time.sleep(5)
        #戴吉伟审批试用
        url3 = self.url + "/portal-test/flow/task/apvList?businessId=" + self.orderId + "&flowIds=1,2,3,8,9,10"
        header['Token'] = casjc_login.login(casjc_config.avpuser2, casjc_config.avppasswd, 1)[0]
        r3 = requests.get(url3, headers=header)
        print(r3.json())
        taskId = r3.json()['data'][0]['taskId']
        url4 = self.url + "/portal-test/order/approve/apvOrder"
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

        time.sleep(5)
        #戴吉伟配置资源,获取必要参数
        url5 = self.url + "/portal-test/order/order/getOrder?times=1610011814514&orderId=" + self.tryOrderId
        header = {}
        header['Content-Type'] = "application/json"
        header['Token'] = casjc_login.login(casjc_config.avpuser2, casjc_config.avppasswd, 1)[0]
        r5 = requests.get(url5, headers=header)
        #print(r5.json())
        #resInitId_file = r5.json()['data']['resInitVOList'][1]['resInitId']
        #orderResId_file = r5.json()['data']['resVOList'][1]['orderResId']
        resInitId_job = r5.json()['data']['resInitVOList'][0]['resInitId']
        orderResId_job = r5.json()['data']['resVOList'][0]['orderResId']
        uptime = r5.json()['data']['resVOList'][0]['updateTime']

        #配置高性能计算
        url6 = self.url + "/portal-test/order/deploy/deployOrderRes"
        data = {}
        data["colonyId"] = 43
        data["defMemPerCpu"] = ""
        data["deployStatus"] = 3
        data["deployWay"] = 0
        data["endTime"] = time.strftime("20%y-%m-%d",time.localtime())
        data["entId"] = self.entId
        data["nodeList"] = []
        data["number"] = 0
        data["orderId"] = self.tryOrderId
        data["orderResId"] = orderResId_job
        data["queueName"] = ""
        data["queueType"] = 0
        data['qosName'] = "normal"
        data["resInitId"] = resInitId_job
        data["resProdSrvId"] = 1
        data["startTime"] = time.strftime("20%y-%m-%d",time.localtime())
        data["updateTime"] = uptime
        data['resBandowidthList'] = [{"networkName":"","bandwidth":1,"gateway":"","publicIp":"","subnetMask":""}]
        data['resPrivateNetworkList'] = [{"networkName":"","bandwidth":1,"gateway":"","networkSegment":"","subnetMask":""}]
        data['resVpnList'] = [] 
        data['resProdSrvId'] = 1
        data['resTypeId'] = 4
        data['discountUnitPrice'] = 5
        data['unitPrice'] = 5
        data['originalPrice'] = 5
        data['price'] = 5
        data['Path'] = "/public1/home/" + self.account + "/" + self.account
        ldata = []
        ldata.append(data)
        r6 = requests.post(url6, headers=header, data=json.dumps(ldata))
        print(r6.json())
        if r6.json()['code'] == 200 and r6.json()['message'] == None and r6.json()['data'] == None:
            casjc_log_task.logging.info(self.confirmOrder.__doc__ + " 高性能资源配置完成, 配置人:" + casjc_config.avpuser2)
        else:
            casjc_log_task.logging.info(self.confirmOrder.__doc__ + " 高性能资源配置异常, 配置人:" + casjc_config.avpuser2)
            return False


    def applyPrice(self):

        """[审批新购订单价格 ]"""

        time.sleep(5)
        #唐德兵价格审批新购订单
        url1 = self.url + "/portal-test/flow/task/apvList?businessId=" + self.orderId + "&flowIds=1,2,3,8,9,10"
        header = {}
        header['Content-Type'] = "application/json"
        header['Token'] = casjc_login.login(casjc_config.avpuser3, casjc_config.avppasswd, 1)[0]
        r1 = requests.get(url1, headers=header)
        #print(r1.json())
        taskId = r1.json()['data'][0]['taskId']
        url2 = self.url + "/portal-test/order/approve/apvOrder"
        header['Content-Type'] = "application/json"
        data2 = {}
        data2['opinion'] = "test88"
        data2['status'] = 0
        data2['taskId'] = taskId - 1
        r2 = requests.post(url2, headers=header, data=json.dumps(data2))
        print(r2.json())
        if r2.json()['code'] == 200 and r2.json()['message'] == None and r2.json()['data'] == None:
            casjc_log_task.logging.info(self.applyPrice.__doc__ + " 审批账号:" + casjc_config.avpuser1 + " 审批成功")
            return True
        else:
            casjc_log_task.logging.info(self.applyPrice.__doc__ + " 审批账号:" + casjc_config.avpuser1 + " 审批异常")
            return False

   
    def exaContract(self):

        """[审批新购订单合同]"""

        time.sleep(5)
        #合同审批 王楠
        url3 = self.url + "/portal-test/flow/task/apvList?businessId=" + self.orderId + "&flowIds=1,2,3,8,9,10"
        header = {}
        header['Content-Type'] = "application/json"
        header['Token'] = casjc_login.login(casjc_config.conuser1, casjc_config.avppasswd, 1)[0]
        r3 = requests.get(url3, headers=header)
        #print(r3.json())
        taskId = r3.json()['data'][0]['taskId']
        url4 = self.url + "/portal-test/order/approve/apvOrder"
        data3 = {}
        data3['opinion'] = "test"
        data3['status'] = 0
        data3['taskId'] = taskId + 1
        r4 = requests.post(url4, headers=header, data=json.dumps(data3))
        print(r4.json())
        if r4.json()['code'] == 200 and r4.json()['message'] == None and r4.json()['data'] == None:
            casjc_log_task.logging.info(self.exaContract.__doc__ + " 审批账号:" + casjc_config.conuser1 + " 审批成功")
        else:
            casjc_log_task.logging.info(self.exaContract.__doc__ + " 审批账号:" + casjc_config.conuser1 + " 审批异常")
            return False

        time.sleep(5)
        #合同审批 孔水水
        url5 = self.url + "/portal-test/flow/task/apvList?businessId=" + self.orderId + "&flowIds=1,2,3,8,9,10"
        header['Token'] = casjc_login.login(casjc_config.conuser2, casjc_config.avppasswd, 1)[0]
        r5 = requests.get(url5, headers=header)
        #print(r5.json())
        taskId = r5.json()['data'][-1]['taskId']
        url6 = self.url + "/portal-test/order/approve/apvOrder"
        data3 = {}
        data3['opinion'] = "test"
        data3['status'] = 0
        data3['taskId'] = taskId + 2
        r6 = requests.post(url6, headers=header, data=json.dumps(data3))
        print(r6.json())
        if r6.json()['code'] == 200 and r6.json()['message'] == None and r6.json()['data'] == None:
            casjc_log_task.logging.info(self.exaContract.__doc__ + " 审批账号:" + casjc_config.conuser2 + " 审批成功")
        else:
            casjc_log_task.logging.info(self.exaContract.__doc__ + " 审批账号:" + casjc_config.conuser2 + " 审批异常")
            return False

        time.sleep(5)
        #合同审批 刘凯敏
        url7 = self.url + "/portal-test/flow/task/apvList?businessId=" + self.orderId + "&flowIds=1,2,3,8,9,10"
        header['Token'] = casjc_login.login(casjc_config.conuser3, casjc_config.avppasswd, 1)[0]
        r7 = requests.get(url7, headers=header)
        #print(r7.json())
        taskId = r7.json()['data'][-1]['taskId']
        url8 = self.url + "/portal-test/order/approve/apvOrder"
        data3 = {}
        data3['opinion'] = "test"
        data3['status'] = 0
        data3['taskId'] = taskId + 1
        r8 = requests.post(url8, headers=header, data=json.dumps(data3))
        print(r8.json())
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
        self.applyOrder(0)
        #self.applyTryPrice()
        #self.confirmOrder()

    def testNew(self, mytype="All"):
        self.applyOrder(1)
        self.applyPrice()
        self.exaContract()
        #self.confirmParam(mytype)
        #self.confirmAll(mytype)

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
    #mytest = resource('crazy03231701','100905','10831')
    tmp = casjc_user.auser()
    a,b,c = tmp.addControlUser()
    mytest = resource(a,b,c)
    print(a)
    #mytest = resource()

    '''
    try:
        if sys.argv[1] == "1":
            mytest.testNew()
        elif sys.argv[1] == "0":
            mytest.testTry()
    except IndexError:
        print('not have parames')
    '''

    #试用
    #mytest.testTry()

    #新购
    mytest.testNew()
    #mytest.testNew("half")

    #续期
    #mytest.testRenew()
