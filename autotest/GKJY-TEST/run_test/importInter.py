#!/usr/bin/env python3

import sys, json, os
import xlrd
from lhlmysql.lhlsql import lhlSql

def readInter():
    try:
#        wb = xlrd.open_workbook(filename= os.getcwd() + '/excel/ainterfacedata.xlsx')
        wb = xlrd.open_workbook(filename= os.getcwd() + '/run_test/excel/interfacedata.xlsx')
    except FileNotFoundError:
        try:
#            wb = xlrd.open_workbook(filename= os.getcwd() + '/excel/ainterfacedata.xls')
            wb = xlrd.open_workbook(filename= os.getcwd() + '/run_test/excel/interfacedata.xls')
        except FileNotFoundError:
            return "<html><p>导入的文件名字有误,确保上传的文件名为interfacedata.xlsx的excel文件</p><a href='interfaceList'>返回待请求接口列表</a></html>"
    except xlrd.zipfile.BadZipFile:
        excelfileError = "导入的excle文件有问题"
        return "<html><p>导入的文件本身有误,确保上传的文件名为interfacedata.xlsx的excel文件</p><a href='interfaceList'>返回待请求接口列表</a></html>"
    s1 = wb.sheet_by_index(0)
    mydata = lhlSql()
    for i in range(1,s1.nrows):
        row = s1.row_values(i)
        print(row)
        row[5] = row[5].strip()
        row[8] = row[8].strip()
        print(type(row[7]))
        if row[7]:
            try:
                tmp = "请求参数"
                dd = 'json格式有误,第{0}行数据有误,{1}有误'.format(i+1,tmp)
                dataerror = "<html>" + json.dumps({'msg': "faile", 'status': -1, 'data': dd}, ensure_ascii=False) + "<br /><a href='interfaceList'>导入的数据json格式有误,返回待请求接口列表,请修改后重新导入</a></html>"
                if row[5] == "" or row[5] == None:
                    row[5] = "{}"
                else:
                   jsdata = json.dumps(json.loads(row[5]))
            except json.decoder.JSONDecodeError:
                return dataerror
            try:
                tmp2 = "测试账号密码"
                dd2 = 'json格式有误,第{0}行数据有误,{1}有误'.format(i+1,tmp2)
                dataerror2 = "<html>" + json.dumps({'msg': "faile", 'status': -1, 'data': dd2}, ensure_ascii=False) + "<br /><a href='interfaceList'>导入的数据json格式有误,返回待请求接口列表,请修改后重新导入</a></html>"
                if row[8] == "" or row[8] == None:
                    row[8] = '{}'
                else:
                    jsdata2 = json.dumps(json.loads(row[8]))
            except json.decoder.JSONDecodeError:
                return dataerror2
            if type(row[7]) == float:
                row[7] = str(int(row[7]))
            else:
                row[7] = ""
            mydata.insertInterface(row[0],row[3],row[2],json.dumps(json.loads(row[5]),ensure_ascii=False),row[4],row[6],row[1],row[7],json.dumps(json.loads(row[8]),ensure_ascii=False))
        else:
            try:
                tmp = "请求参数"
                dd = 'json格式有误,第{0}行数据有误,{1}有误'.format(i+1,tmp)
                dataerror = "<html>" + json.dumps({'msg': "faile", 'status': -1, 'data': dd}, ensure_ascii=False) + "<br /><a href='interfaceList'>导入的数据json格式有误,返回待请求接口列表,请修改后重新导入</a></html>"
                if row[5] == "" or row[5] == None:
                    row[5] = "{}"
                else:
                   jsdata = json.dumps(json.loads(row[5]))
            except json.decoder.JSONDecodeError:
                return dataerror
            try:
                tmp2 = "测试账号密码"
                dd2 = 'json格式有误,第{0}行数据有误,{1}有误'.format(i+1,tmp2)
                dataerror2 = "<html>" + json.dumps({'msg': "faile", 'status': -1, 'data': dd2}, ensure_ascii=False) + "<br /><a href='interfaceList'>导入的数据json格式有误,返回待请求接口列表,请修改后重新导入</a></html>"
                if row[8] == "" or row[8] == None:
                    row[8] = '{}'
                else:
                    jsdata2 = json.dumps(json.loads(row[8]))
            except json.decoder.JSONDecodeError:
                return dataerror2
            mydata.insertInterface(row[0],row[3],row[2],json.dumps(json.loads(row[5]),ensure_ascii=False),row[4],row[6],row[1],'None',json.dumps(json.loads(row[8]),ensure_ascii=False))
    return "<html><p>导入成功</p><a href='interfaceList'>返回待请求接口列表</a></html>"

if __name__ == "__main__":
    readInter()
