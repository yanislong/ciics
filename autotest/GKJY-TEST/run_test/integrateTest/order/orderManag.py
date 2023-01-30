#!/usr/bin/env python3

import requests
import threading
import json, sys, random, os
sys.path.append(os.getcwd() + '/../../lhlmysql')
sys.path.append(os.getcwd() + '/../../../')
sys.path.append(os.getcwd() + "/../user")

from lhlsql import lhlSql, portalSql
import config
import userLogin

class orderManag():

    def __init__(self):
        self.sqldata = lhlSql()
        self.portalsql = portalSql()
        self.session = userLogin.userlogin()
        self.postheader = {}
        self.postheader['Content-Type'] = "application/json"
        self.postheader['Authorization'] = self.session.accountLogin()
        self.url = config.orderurl
        pass

    def addorder(self):
        """使用合法数据申请资源"""

        mokuai = "订单管理"
        url = self.url + "/order/addOrder"
        param = {}
        #提交申请方 0甲方1销售经理
        param["applyParty"] = 1
        #服务区ID
        param["areaId"] = 8
        #平均折扣/最低折扣\n配置方式\n0固定参数：平均折扣\n1灵活配置：最低折扣
        param["avgDiscount"] = 0
        #资源配置方式，0固定参数1灵活配置
        param['deployWay'] = 0
        #优惠总额，单位：分
        param["discountPrice"] = 0
        #用户单位ID
        param["entCompanyId"] =  0
        #甲方账号是否存在 0存在1不存在
        param["entExist"] = 1
        #甲方邮箱
        param["entMail"] = "250@qq.com"
        #甲方联系电话
        param["entPhone"] = "18911226966"
        #甲方联系电话方式0固定电话1手机
        param["entPhoneWay"] = ""
        #甲方账号ID
        param["entId"] = ""
        #订单ID
        param["orderId"] = ""
        #订单类型 0试用1新购2续费3退订
        param["orderType"] = 1
        #产品类型 1高性能计算 3数据存储 4网络资源
        param["productType"] = 1
        #项目名称
        param["projectName"] = "年会预购礼物资金计算"
        #销售经理ID
        param["salesUserId"] = 10038
        #报价总额，单位：分
        param["totalPrice"] = 1
        #订单状态：0暂存1提交
        param["status"] = 1
        #用户账号不存在时备注
        param['userRemark'] = "运营管理员添加"
        resvolist = [{"discount": 1,"number": 1,"price": 1,"resId": 1,"validDays": 1,"resProdSrvId": 1,"unitPrice": 1,"validUnit": "月","resTypeId":1}]
        #资源信息
       	param["resVOList"] = resvolist
        res = requests.post(url, headers=self.postheader, data=json.dumps(param))
        print(res.text)
        try:
            if res.json()['code'] == 200:
                result = "Success"
            else:
                result = "Faile"
        except KeyError:
            result = "Error"
        self.sqldata.insertInterfaceRespond(mokuai, url, json.dumps(param, ensure_ascii=False), res.text, res.status_code, round(res.elapsed.total_seconds(),5), self.addorder.__doc__, result)
        return None

    def applyorder(self):
        """资源申请列表"""

        mokuai = "订单管理"
        roleName = ["中國石油化工集團公司中國石油化工集團公司中國石油化工集團公司"] 
        param = {}
        param['pageNum'] = "1"
        param['pageSize'] = "10"
        param['applyNumber'] = "1"
        for j in roleName:
            url = self.url + "/order/applyOrderList"
            res = requests.get(url, headers=self.postheader, params=param)
            print(res.url)
            print(res.text)
        try:
            if res.json()['code'] != 200:
               result = "Success"
            else:
               result = "Faile"
        except KeyError:
           result = "Error"
        self.sqldata.insertInterfaceRespond(mokuai, url, json.dumps(param), res.text, res.status_code, round(res.elapsed.total_seconds(),5), self.applyorder.__doc__, result)
        return None

    def getorder(self):
        """我的申请单列表"""

        mokuai = "订单管理"
        roleName = ["中國石油化工集團公司中國石油化工集團公司中國石油化工集團公司"] 
        param = {}
        param['pageNum'] = "1"
        param['pageSize'] = "10"
        for j in roleName:
            url = self.url + "/order/myOrderList"
            res = requests.get(url, headers=self.postheader, params=param)
            print(res.url)
            print(res.text)
        try:
            if res.json()['code'] != 200:
               result = "Success"
            else:
               result = "Faile"
        except KeyError:
           result = "Error"
        self.sqldata.insertInterfaceRespond(mokuai, url, json.dumps(param), res.text, res.status_code, round(res.elapsed.total_seconds(),5), self.getorder.__doc__, result)
        return None

    def delorder(self):
        """删除订单"""

        mokuai = "订单管理"
        roleName = ["中國石油化工集團公司中國石油化工集團公司中國石油化工集團公司"] 
        param = {}
        param['orderId'] = "1"
        for j in roleName:
            url = self.url + "/order/delOrder"
            res = requests.get(url, headers=self.postheader, params=param)
            print(res.url)
            print(res.text)
        try:
            if res.json()['code'] != 200:
               result = "Success"
            else:
               result = "Faile"
        except KeyError:
           result = "Error"
        self.sqldata.insertInterfaceRespond(mokuai, url, json.dumps(param), res.text, res.status_code, round(res.elapsed.total_seconds(),5), self.delorder.__doc__, result)
        return None

    def orderinfo(self):
        """订单详情"""

        mokuai = "订单管理"
        roleName = ["中國石油化工集團公司中國石油化工集團公司中國石油化工集團公司"] 
        param = {}
        param['orderId'] = "1"
        for j in roleName:
            url = self.url + "/order/getOrder"
            res = requests.get(url, headers=self.postheader, params=param)
            print(res.url)
            print(res.text)
        try:
            if res.json()['code'] != 200:
               result = "Success"
            else:
               result = "Faile"
        except KeyError:
           result = "Error"
        self.sqldata.insertInterfaceRespond(mokuai, url, json.dumps(param), res.text, res.status_code, round(res.elapsed.total_seconds(),5), self.orderinfo.__doc__, result)
        return None

    def apvorderlist(self):
        """待审批资源列表"""

        mokuai = "订单管理"
        roleName = ["中國石油化工集團公司中國石油化工集團公司中國石油化工集團公司"] 
        param = {}
        param['pageNum'] = "1"
        param['pageSize'] = "1"
        param['applyNumber'] = "1"
        for j in roleName:
            url = self.url + "/order/apvOrderList"
            res = requests.get(url, headers=self.postheader, params=param)
            print(res.url)
            print(res.text)
        try:
            if res.json()['code'] != 200:
               result = "Success"
            else:
               result = "Faile"
        except KeyError:
           result = "Error"
        self.sqldata.insertInterfaceRespond(mokuai, url, json.dumps(param), res.text, res.status_code, round(res.elapsed.total_seconds(),5), self.apvorderlist.__doc__, result)
        return None

    def apvorder(self):
        """审批"""

        mokuai = "订单管理"
        roleName = ["中國石油化工集團公司中國石油化工集團公司中國石油化工集團公司"] 
        param = {}
        param['status'] = "1"
        param['taskId'] = "1"
        param['opinion'] = "1"
        for j in roleName:
            url = self.url + "/order/apvOrder"
            res = requests.get(url, headers=self.postheader, params=param)
            print(res.url)
            print(res.text)
        try:
            if res.json()['code'] != 200:
               result = "Success"
            else:
               result = "Faile"
        except KeyError:
           result = "Error"
        self.sqldata.insertInterfaceRespond(mokuai, url, json.dumps(param), res.text, res.status_code, round(res.elapsed.total_seconds(),5), self.apvorder.__doc__, result)
        return None

    def updateorder(self):
        """提交订单"""

        mokuai = "订单管理"
        roleName = ["中國石油化工集團公司中國石油化工集團公司中國石油化工集團公司"] 
        param = {}
        param["applyNumber"] = "a1"
        param["applyParty"] = 0
        param["approveStep"] = "a2"
        param["areaId"] = 0
        param["areaInfo"] = "a3"
        param["avgDiscount"] = 0
        param["discountPrice"] = 0
        param["entCompanyId"] = 0
        param["entCompanyName"] = "a4"
        param["entExist"] = 0
        param["entId"] = 0
        param["entMail"] = "a5"
        param["entPhone"] = "a6"
        param["orderId"] = 0
        param["orderNumber"] = "a7"
        param["orderType"] = 0
        param["productType"] = 0
        param["projectName"] = "a8"
        param["salesUserId"] = 0
        param["salesUserName"] = "a11"
        param["status"] = 0
        param["totalPrice"] = 0
        param["userId"] = 0
        reslist = [{"level": 0,"parentId": 0,"resId": 0,"resInfo": "a9","totalNumber": 0,"unitPrice": 0,"useNumber": 0}]
        param["resVOList"] = [{"discount": 0, "number": 0, "orderResId": 0, "price": 0, "resId": 0, "validDays": 0, "resList": reslist, "validUnit": "a10"}]
        for j in roleName:
            url = self.url + "/order/updateOrder"
            res = requests.post(url, headers=self.postheader, data=json.dumps(param))
            print(res.text)
        try:
            if res.json()['code'] == 200:
                result = "Success"
            else:
                result = "Faile"
        except KeyError:
            result = "Error"
        self.sqldata.insertInterfaceRespond(mokuai, url, json.dumps(param), res.text, res.status_code, round(res.elapsed.total_seconds(),5), self.updateorder.__doc__, result)
        return None

    def deployorder(self):
        """资源配置"""

        mokuai = "订单管理"
        roleName = ["中國石油化工集團公司中國石油化工集團公司中國石油化工集團公司"] 
        param = {}
        for j in roleName:
            url = self.url + "/order/deployOrderRes"
            res = requests.post(url, headers=self.postheader, params=param)
            print(res.url)
            print(res.text)
        try:
            if res.json()['code'] != 200:
               result = "Success"
            else:
               result = "Faile"
        except KeyError:
           result = "Error"
        self.sqldata.insertInterfaceRespond(mokuai, url, json.dumps(param), res.text, res.status_code, round(res.elapsed.total_seconds(),5), self.deployorder.__doc__, result)
        return None

    def checkprice(self):
        """审批人已审批额度"""

        mokuai = "订单管理"
        roleName = ["中國石油化工集團公司中國石油化工集團公司中國石油化工集團公司"] 
        param = {}
        param['flowId'] = ""
        param['userId'] = ""
        for j in roleName:
            url = self.url + "/order/getCheckPrice"
            res = requests.get(url, headers=self.postheader, params=param)
            print(res.url)
            print(res.text)
        try:
            if res.json()['code'] != 200:
                result = "Success"
            else:
                result = "Faile"
        except KeyError:
            result = "Error"
        except json.decoder.JSONDecodeError:
            result = "Error"
        self.sqldata.insertInterfaceRespond(mokuai, url, json.dumps(param), res.text, res.status_code, round(res.elapsed.total_seconds(),5), self.checkprice.__doc__, result)
        return None

    def orderpaymanag(self):
        """根据订单号进行付款"""

        mokuai = "订单支付管理"
        url = self.url + "/pay/payOrder"
        param = {}
        param['orderId'] = ""
        param['payPrice'] = ""
        param['payTimes'] = ""
        res = requests.post(url, headers=self.postheader, data=json.dumps(param))
        print(res.text)
        try:
            if res.json()['code'] == 200:
               result = "Success"
            else:
               result = "Faile"
        except KeyError:
               result = "Error"
        self.sqldata.insertInterfaceRespond(mokuai, url, json.dumps(param), res.text, res.status_code, round(res.elapsed.total_seconds(),5), self.orderpaymanag.__doc__, result)
        return None

if __name__ == "__main__":
    runtest = orderManag()
    runtest.addorder()
#    runtest.getorder()
#    runtest.applyorder()
#    runtest.orderinfo()
#    runtest.delorder()
#    runtest.apvorderlist()
#    runtest.apvorder()
#    runtest.updateorder()
#    runtest.deployorder()
#    runtest.checkprice()
#    runtest.orderpaymanag()

    tmp = []
    for i in range(0):
        t = threading.Thread(target=runtest.addrole)
        tmp.append(t)
        t.start()
    for j in tmp:
        j.join()
