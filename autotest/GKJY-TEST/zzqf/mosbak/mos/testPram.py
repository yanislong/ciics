#!/usr/bin/env python3

import json
import B01xd, B04bf, B02kk, B04qt, qcx
import pymysql


#申请扣费
testdataB01 = B01xd.b01xd

#扣款
testdataB02 = B02kk.b02kk

#部分退费
testdataB03 = B04bf.b04bf

#全部退费
testdataB04 = B04qt.b04qt

#查询订单oo
testdataq = qcx.qcx
#print(testdataB01)

con = pymysql.connect("10.9.19.71", "lihailong", "lihailong123", 'cscloudx_hospital', charset="utf8mb4")

def getOrderInfo():
    cursor = con.cursor()
    sql = "select sb_trade_num, statement_serial_num, frozen_amount from sb_settlement_records where app_id='HIS20220509DLT'";
    cursor.execute(sql)
    return cursor.fetchall()
    for i in cursor.fetchall():
        print(i)


head = {}
# 申请扣款:B01 扣费确认:B02 反交易退费:B04  药品目录:C01 诊疗项目目录:C02 收费类别:C03 病种目录:C04
head["busseID"] = "B01"
head["sendTradeNum"] = "1597730282070-10011001-0002"
head["senderCode"] = "HIS20220509DLT"
head["senderName"] = "大柳塔医院HIS"
head["receiverCode"] = "002"
head["receiverName"] = "MOS"
head["intermediaryCode"] = "HIS20220509DLT"
head["intermediaryName"] = "大柳塔医院HIS"
head["hosorgNum"] = "001"
head["hosorgName"] = "操作员姓名"
head["systemType"] = "1"
head["busenissType"] = "2"
head["standardVersionCode"] = "version:1.0.0"
head["clientmacAddress"] = "30BB7E0A5E2D"
head["recordCount "] = "1"
additionInfo = {}
additionInfo["errorCode"] = ""
additionInfo["errorMsg"] = ""
additionInfo["receiverTradeNum"] = ""
additionInfo["correlationId"] = ""
additionInfo["asyncAsk"] = "0"
additionInfo["callback"] = "http://127.0.0.1:8080/xxxx/xxxx.do"
additionInfo["curDllAddr"] = ""
data ={}
data['type'] = "1"
data["deductionType"] = 0
data["settlementSerialNumber"] = ""
#处方数据
meddata = {}
meddata['medicalNum'] = "12345678901234567890"
meddata['feeItemType'] = "001"
meddata['feeType'] = "001"
meddata['prescriptionNum'] = "20220514"
meddata['prescriptionDateStr'] = "2022-05-14 11:17"
meddata["feeItemCode"] = "001"
meddata["feeItemCenterCode"] = "001"
meddata["feeItemName"] = "检查费"
meddata['unitPrice'] = "10.05"
meddata["Quantity"] = "2"
meddata["dosageForm"] = "001"
meddata["Specification"] = "001"
meddata["perDosage"] = "1"
meddata["frequencyOfUse"] = "1"
meddata["perscritpionDocName"] = "安道全"
meddata["perscritpionDocCode"] = "001"
meddata["Usage"] = "用法"
meddata["Unit"] = "瓶"
meddata["depName"] = "检疫室"
meddata["executeDays"] = "1"
meddata["updateBy"] = "松江"
meddata["drugDosageUnit"] = "升"
#结算数据
costdata = {}
costdata['statementSerialNum'] = "1234567890"
costdata['medicalNum'] = "00001"
costdata['inHosRegisterId'] = "00001"
costdata['hospitalCode'] = "00001"
costdata['insuredUserType'] = "在职"
costdata['insuredTypeCode'] = "001"
costdata['settlementType'] = "中途结算"
costdata['settlementDateStr'] = "2022-05-14 12:12:12"
costdata['detailCount'] = 5
costdata['totalAmount'] = 10.55
costdata['IsAfterMedicare'] = 1
costdata['offsetFlag'] = "1"
costdata['feeDetailList'] = {}
#交易数据
paydata = {}
paydata["medicalNum"] = "0001"
paydata["medicalType"] = "0001"
paydata["treatDate"] = "2022-05-14 12:12:30"
paydata["inHosDiagnosisCode"] = "001"
paydata["inHosDiagnosisName"] = "新冠"
paydata["outHosDiagnosisCode"] = "002"
paydata["outHosDiagnosisName"] = "感冒"
paydata["credentialType"] = "01"
paydata["credentialNum"] = "342401198807174912"
paydata["name"] = "鲍玉虎"
paydata["gender"] = "男"
paydata["birthday"] = "19880505"
paydata["race"] = "汉"
paydata["currMedicalCost"] = "10.5"
paydata["updateBy"] = "吴承恩"
#数据拼接
data["medDataList"] = meddata
data["costData"] = costdata
data["payData"] = paydata
packag = {}
packag["head"] = head
packag["body"] = data
packag["additionInfo"] = additionInfo
mydata = {"packag":packag}
#print(mydata)

if __name__ == "__main__":
    pass
    getOrderInfo()
