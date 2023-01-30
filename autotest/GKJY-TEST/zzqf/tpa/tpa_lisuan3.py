#!/usr/bin/env python3

import json, time, sys
import pymysql
import requests
import tpa_login, tpa_log, tpa_config

class tpa_process():

    header = {}
    header['Content-Type'] = "application/json"
    #责任细分，责任类型，医院等级，是否医保定点，自付一，自付二，自费
    mybill = []

    def __init__(self):
        #token = tpa_login.login()
        #self.header['Authorization'] = token
        self.tpa_server = pymysql.connect(tpa_config.mysql_host, tpa_config.mysqluser, tpa_config.mysqlpasswd, 'cscloudx_tpa', charset="utf8mb4")
        self.tpa_base = pymysql.connect(tpa_config.mysql_host, tpa_config.mysqluser, tpa_config.mysqlpasswd, 'cscloudx_tpa_base', charset="utf8mb4")
        self.tpa_product = pymysql.connect(tpa_config.mysql_host, tpa_config.mysqluser, tpa_config.mysqlpasswd, 'zz_insurance_product_center', charset="utf8mb4")
        self.tpa_policy = pymysql.connect(tpa_config.mysql_host, tpa_config.mysqluser, tpa_config.mysqlpasswd, 'zz_insurance_policy_center', charset="utf8mb4")

    def getBillInfo(self, case_no="GC0215310011P"):
        """根据case_no参数，查询票据的: 责任类型,结算类型,医院等级,是否定点,自付一,自付二,自费信息"""
        tmp = []
        cursor = self.tpa_server.cursor()
        cursor2 = self.tpa_policy.cursor()
        cursor3 = self.tpa_base.cursor()
        sql = "select bill_type,hospital_flag,hospital_grade,fixed_point,count_amount,self_pay1, self_pay2, own_expense_pay_amount from t_claim_case_bill where case_no='{0}'".format(case_no)
        cursor.execute(sql)
        billInfo = cursor.fetchall()
        for i in billInfo:
            sql3 = "select dict_name from sys_dict where parent_codes='gen:bill_type' and dict_code={0}".format(i[0])
            cursor3.execute(sql3)
            dictname = cursor3.fetchall()
            tmp.append((dictname[0][0],i[0]))
            sql4 = "select dict_name from sys_dict where parent_codes='gen:hospital_flag' and dict_code={0}".format(i[1])
            cursor3.execute(sql4)
            dictname = cursor3.fetchall()
            tmp.append((dictname[0][0],i[1]))
            sql5 = "select dict_name from sys_dict where parent_codes='gen:hospital_grade' and dict_code={0}".format(i[2])
            cursor3.execute(sql5)
            dictname = cursor3.fetchall()
            tmp.append((dictname[0][0],i[2]))
            sql6 = "select dict_name from sys_dict where parent_codes='gen:yes_no' and dict_code='{0}'".format(i[3])
            cursor3.execute(sql6)
            dictname = cursor3.fetchall()
            tmp.append((dictname[0][0],i[3]))
            tmp.append(i[4])
            tmp.append(i[5])
            tmp.append(i[6])
            sql2 = "select customer_no from t_claim_case_insured where case_no='{0}'".format(case_no)
            cursor.execute(sql2)
            pInfo = cursor.fetchall()
            if pInfo:
                sql3 = "select field_name, field_value, insurer_id from insured_user_custom_sign where identify_code='{}'".format(pInfo[0][0])
                cursor2.execute(sql3)
                pCode = cursor2.fetchall() 
                tmp2 = []
                for j in pCode:
                    tmp2.append(j)
                tmp.append(tmp2)
            self.mybill.append(tmp)
            tmp = []
        for i in self.mybill:
            print(i)
        return None

    def billexpress(self):
        for i in self.mybill:
            ttotal = i[4]+i[5]+i[6]
            #print(ttotal)
            givem = 0
            if i[3][1] == tpa_config.expression[0]["是否医保定点医院"] and i[1][1] in tpa_config.expression[0]["责任类型"] and i[2][1] not in tpa_config.expression[0]['责任细分']:
                cover_id = "1506899053139464193"
                menoy = self.getResult(cover_id,i[4],i[5],i[6],i[7][1])
                print("匹配责任", menoy[1])
                if givem > ttotal:
                    givem = ttotal
                    print(givem)
                    break
                else:
                    givem = givem + menoy[0]
            if i[3][1] == tpa_config.expression[1]["是否医保定点医院"] and i[1][1] in tpa_config.expression[1]["责任类型"] and i[2][1] not in tpa_config.expression[1]['责任细分']:
                cover_id = "1506899450893701122"
                menoy = self.getResult(cover_id,i[4],i[5],i[6],i[7][1])
                print("匹配责任", menoy[1])
                if givem > ttotal:
                    givem = ttotal
                    print(givem)
                    break
                else:
                    givem = givem + menoy[0]
            if i[3][1] == tpa_config.expression[2]["是否医保定点医院"] and i[1][1] in tpa_config.expression[2]["责任类型"] and i[2][1] not in tpa_config.expression[2]['责任细分']:
                cover_id = "1506899786920366081"
                menoy = self.getResult(cover_id,i[4],i[5],i[6],i[7][1])
                print("匹配责任", menoy[1])
                if givem > ttotal:
                    givem = ttotal
                    print(givem)
                    break
                else:
                    givem = givem + menoy[0]
            if i[3][1] == tpa_config.expression[3]["是否医保定点医院"] and i[2][1]== tpa_config.expression[3]['医院等级'] and i[1][1] == tpa_config.expression[3]["责任类型"] and i[2][1] == tpa_config.expression[3]["人工指定"] and i[2][1] not in tpa_config.expression[3]['责任细分']:
                cover_id = "1506900124264042497"
                menoy = self.getResult(cover_id,i[4],i[5],i[6],i[7][1])
                print("匹配责任", menoy[1])
                if givem > ttotal:
                    givem = ttotal
                    print(givem)
                    break
                else:
                    givem = givem + menoy[0]
            if i[3][1] == tpa_config.expression[4]["是否医保定点医院"] and i[2][1]== tpa_config.expression[4]['医院等级'] and i[1][1] == tpa_config.expression[4]["责任类型"] and i[2][1] == tpa_config.expression[4]["人工指定"] and i[2][1] not in tpa_config.expression[3]['责任细分']:
                cover_id = "1506900330586050562"
                menoy = self.getResult(cover_id,i[4],i[5],i[6],i[7][1])
                print("匹配责任", menoy[1])
                if givem > ttotal:
                    givem = ttotal
                    print(givem)
                    break
                else:
                    givem = givem + menoy[0]
            if i[3][1] == tpa_config.expression[5]["是否医保定点医院"] and i[2][1]== tpa_config.expression[5]['医院等级'] and i[1][1] == tpa_config.expression[5]["责任类型"] and i[2][1] == tpa_config.expression[5]["人工指定"] and i[2][1] not in tpa_config.expression[5]['责任细分']:
                cover_id = "1506900541110751234"
                menoy = self.getResult(cover_id,i[4],i[5],i[6],i[7][1])
                print("匹配责任", menoy[1])
                if givem > ttotal:
                    givem = ttotal
                    print(givem)
                    break
                else:
                    givem = givem + menoy[0]
            if i[3][1] == tpa_config.expression[6]["是否医保定点医院"] and i[2][1] == tpa_config.expression[6]["人工指定"] and i[2][1] not in tpa_config.expression[6]['责任细分']:
                cover_id = "1506900746929442817"
                menoy = self.getResult(cover_id,i[4],i[5],i[6],i[7][1])
                print("匹配责任", menoy[1])
                if givem > ttotal:
                    givem = ttotal
                    print(givem)
                    break
                else:
                    givem = givem + menoy[0]
            if i[3][1] == tpa_config.expression[7]["是否医保定点医院"] and i[1][1] in tpa_config.expression[7]["责任类型"] and i[2][1] == tpa_config.expression[7]["人工指定"] and i[2][1] not in tpa_config.expression[7]['责任细分']:
                cover_id = "1506901033010335745"
                menoy = self.getResult(cover_id,i[4],i[5],i[6],i[7][1])
                print("匹配责任", menoy[1])
                if givem > ttotal:
                    givem = ttotal
                    print(givem)
                    break
                else:
                    givem = givem + menoy[0]
            if i[3][1] == tpa_config.expression[8]["是否医保定点医院"]  and i[1][1] in tpa_config.expression[8]["责任类型"] and i[2][1] == tpa_config.expression[8]["人工指定"] and i[2][1] not in tpa_config.expression[8]['责任细分']:
                cover_id = "1506901241064591362"
                menoy = self.getResult(cover_id,i[4],i[5],i[6],i[7][1])
                print("匹配责任", menoy[1])
                if givem > ttotal:
                    givem = ttotal
                    print(givem)
                    break
                else:
                    givem = givem + menoy[0]
            if i[3][1] == tpa_config.expression[9]["是否医保定点医院"] and i[2][1] not in tpa_config.expression[9]['责任细分']:
                cover_id = "1506901590601109505"
                menoy = self.getResult(cover_id,i[4],i[5],i[6],i[7][1])
                print("匹配责任", menoy[1])
                if givem > ttotal:
                    givem = ttotal
                    print(givem)
                    break
                else:
                    givem = givem + menoy[0]
        return None


    def getSocial(self):
        s_no = "1450731739906342913"
        cursor = self.tpa_product.cursor()
        sql = "select pay1, pay2, full_individual from product_deduction_social where cover_id='{0}'".format(s_no)
        cursor.execute(sql)
        sInfo = cursor.fetchall()
        for i in sInfo:
            print(i)

    def getUser(self):
        s_no = "1450731739906342913"
        cursor = self.tpa_product.cursor()
        sql = "select pay1, pay2, full_individual from product_deduction_social where cover_id='{0}'".format(s_no)
        cursor.execute(sql)
        sInfo = cursor.fetchall()
        for i in sInfo:
            print(i)

    def getexpre(self):
        s_no = "1506901590601109505"
        cursor = self.tpa_product.cursor()
        sql = "select expression, expression_description from product_expression_result where cover_id='{0}'".format(s_no)
        cursor.execute(sql)
        sInfo = cursor.fetchall()
        for i in sInfo:
            print(i)

    def getResult(self,cover_id,num1,num2,num3,insurer_id):
        cursor = self.tpa_product.cursor()
        cursor2 = self.tpa_policy.cursor()
        sql1 = "select cover_name from product_cover where id='{0}'".format(cover_id)
        cursor.execute(sql1)
        covername = cursor.fetchall()[0][0]
        sql2 = "select current_limit_amount from adjust_person_limit_amount where insurer_id='{}' order by current_limit_amount asc".format(insurer_id[2])
        cursor2.execute(sql2)
        insurer = cursor2.fetchall()
        tip = insurer[0]
        sql = "select pay1, pay2, full_individual from product_deduction_social where cover_id='{0}'".format(cover_id)
        cursor.execute(sql)
        ppf = cursor.fetchall()
        total = num1 + num2 + num3
        tmp1 = num1 * ppf[0][0]
        tmp2 = num2 * ppf[0][1]
        tmp3 = num3 * ppf[0][2]
        #print(tmp1)
        #print(tmp2)
        #print(tmp3)
        tmptotal = tmp1 + tmp2 + tmp3
        if tip[0] > 0 and tmptotal <= total and tmptotal <= tip[0]:
            print(tmptotal, covername)
            return tmptotal, covername
        if tip[0] > 0 and tmptotal > tip[0]:
            print(tip, covername)
            return tip, covername
        elif tip[0] <= 0:
            print(0,covername)
            return 0,covername
        else:
            print(total, covername)
            return total, covername

if __name__ == "__main__":
    tpa_log.logger.info("########### 脚本开始执行 #############\n")
    mytest = tpa_process()
    try:
        mytest.getBillInfo(sys.argv[1])
    except IndexError:
        tmp = "GC0215310011P"
        mytest.getBillInfo(tmp)
    #mytest.billexpress()
    #mytest.getSocial()
    #mytest.getexpre()
