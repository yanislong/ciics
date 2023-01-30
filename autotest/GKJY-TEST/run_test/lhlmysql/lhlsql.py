#!/usr/bin/env python3

import pymysql
import sys, os, time
sys.path.append(os.getcwd() + '/../')
sys.path.append(os.getcwd() + '/../../')

import config

class lhlSql:
    
    def __init__(self):
        self.con = pymysql.connect(config.mysql_host, config.mysqluser, config.mysqlpasswd, 'portaltest', charset="utf8mb4")

    def getTimeInfo(self, iname, num=0):
        """根据iname, num参数，查询20条接口响应的时间信息"""
        cursor = self.con.cursor()
        sql = "select id, dns_time, conn_time, startData_time, total_time, updata, downdata, insertTime, content, code from qianyun where content like '%{0}%'limit {1},20".format(iname, num)
        cursor.execute(sql)
        timeinfo = cursor.fetchall()
        return timeinfo

    def getTimeList(self,iname=""):
        timelist = []
        """
        根据startnum,stopnum参数，查询接口DNS响应,接口与服务器连接完成响,
        服务器开始传输数据,完成响应的整体的时间,上传和下载数据的大小
        """
        cursor = self.con.cursor()
        sql = "select sum(dns_time), sum(conn_time), sum(startData_time), sum(total_time), sum(updata), sum(downdata) from qianyun where content like '%{0}%'".format(iname)
        cursor.execute(sql)
        dns_time = cursor.fetchall()[0]
        timelist.append(dns_time)
        return timelist

    def getTotalNumber(self, iname):
        """查询qianyun表总条数"""
        cursor = self.con.cursor()
        sql = "select count(*) from qianyun where content like '%{0}%'".format(iname)
        cursor.execute(sql)
        getTotal = cursor.fetchall()
        cursor.close()
        return getTotal[0][0]
    
    def getInterfaceName(self):
        """查询qianyun表中接口的名字"""
        cursor = self.con.cursor()
        sql = "select distinct content from qianyun"
        cursor.execute(sql)
        Name = cursor.fetchall()
        cursor.close()
        return Name

    def getInterfaceInfoName(self):
        """查询interfaceInfo表中接口的名字"""
        cursor = self.con.cursor()
        sql = "select distinct intername from interfaceInfo"
        cursor.execute(sql)
        Name = cursor.fetchall()
        cursor.close()
        return Name
    
    def getInterfaceAuthor(self):
        """查询interfaceInfo表中接口开发者的名字"""
        cursor = self.con.cursor()
        sql = "select distinct author from interfaceInfo"
        cursor.execute(sql)
        Name = cursor.fetchall()
        cursor.close()
        return Name
    
    def getInterfaceRespondName(self):
        """查询interfaceRespond表中接口的名字"""
        cursor = self.con.cursor()
        sql = "select distinct intername from interfaceRespond"
        cursor.execute(sql)
        Name = cursor.fetchall()
        cursor.close()
        return Name

    def getShellRespondName(self):
        """查询shellRespond表中接口的名字"""
        cursor = self.con.cursor()
        sql = "select distinct intername from shellRespond"
        cursor.execute(sql)
        Name = cursor.fetchall()
        cursor.close()
        return Name

    def getInterfaceList(self, iname="", iauthor="", num=0):
        """查询interfaceInfo表中20条数据"""
        cursor = self.con.cursor()
        sql = "select id, intername, interaddr, header, param, `option`, inputtime, author, descp, expected, account from interfaceInfo where intername like '%{0}%' and author like '%{1}%' order by id Desc limit {2},20".format(iname, iauthor, num)
        cursor.execute(sql)
        inter = cursor.fetchall()
        cursor.close()
        print(inter)
        return inter

    def getInterfaceRespondList(self, iname, result, mid, num=0):
        """查询interfaceRespondList表中数据,返回20条"""
        cursor = self.con.cursor()
        sql = "select id, intername, interaddr, requestparam, respondbody, code, respondtime, inputtime, descp, result from interfaceRespond where intername like '%{0}%' and result like '%{1}%' and id like '%{2}%' order by id Desc limit {3},20".format(iname,result,mid,num)
        cursor.execute(sql)
        inter = cursor.fetchall()
        cursor.close()
        return inter

    def getShellRespondList(self, iname, result, mid, num=0):
        """查询interfaceRespondList表中数据,返回20条"""
        cursor = self.con.cursor()
        sql = "select id, intername, interaddr, requestparam, respondbody, code, respondtime, inputtime, descp, result from shellRespond where intername like '%{0}%' and result like '%{1}%' and id like '%{2}%' order by id Desc limit {3},20".format(iname,result,mid,num)
        cursor.execute(sql)
        inter = cursor.fetchall()
        cursor.close()
        return inter

    def getIdInterface(self, iid=0):
        """通过Id,查询interfaceInfo表中的数据"""
        cursor = self.con.cursor()
        sql = "select id, intername, interaddr, header, param, `option`, author, descp, expected, account from interfaceInfo where id='{0}'".format(iid)
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result

    def getAllInterface(self):
        """查询interfaceInfo表中所有数据"""
        cursor = self.con.cursor()
        sql = "select id, intername, interaddr, header, param, `option`, author, descp, expected, account from interfaceInfo"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result

    def getCollValue(self):
        """查询CollValue表中所有数据"""
        cursor = self.con.cursor()
        sql = "select id, code, value from collvaule"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result

    def insertInterface(self, iname, iaddr, iheader, iparam, ioption, iauthor, descp, expected, iuserpwd):
        """向interfaceInfo表中插入数据"""
        cursor = self.con.cursor()
        tt = time.strftime("%Y/%m/%d %H:%M:%S")
        sql = "insert into interfaceInfo(intername,interaddr,header,param,`option`,author,inputtime, descp, expected, account) value('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}')".format(iname,iaddr,iheader,iparam,ioption,iauthor,tt,descp,expected,iuserpwd)
        cursor.execute(sql)
        self.con.commit()
        cursor.close()
        return None

    def insertInterfaceRespond(self, iname, iaddr, irequestparam, irespondbody, icode, irespondtime, descp, result):
        """向interfaceRespond表中插入数据"""
        cursor = self.con.cursor()
        tt = time.strftime("%Y/%m/%d %H:%M:%S")
        sql = "insert into interfaceRespond(intername,interaddr,requestparam,respondbody,code,respondtime,inputtime,descp, result) value('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}')".format(iname,pymysql.escape_string(iaddr),pymysql.escape_string(irequestparam),pymysql.escape_string(irespondbody),icode,irespondtime,tt,descp,result)
        cursor.execute(sql)
        self.con.commit()
        cursor.close()
        return None

    def getTotalInterfaceNumber(self, iname, iauthor): 
        """获取interfaceInfo表中总条数"""
        cursor = self.con.cursor()
        sql = "select count(*) from interfaceInfo where intername like '%{0}%' and author like '%{1}%'".format(iname,iauthor)
        cursor.execute(sql)
        num = cursor.fetchall()[0][0]
        cursor.close()
        return num

    def getTotalInterfaceRespondNumber(self, iname, iresult): 
        """获取interfaceRespond表中总条数"""
        cursor = self.con.cursor()
        sql = "select count(*) from interfaceRespond where intername like '%{0}%' and result like '%{1}%'".format(iname,iresult)
        cursor.execute(sql)
        num = cursor.fetchall()[0][0]
        cursor.close()
        return num

    def getTotalShellRespondNumber(self, iname, iresult): 
        """获取shellRespond表中总条数"""
        cursor = self.con.cursor()
        sql = "select count(*) from shellRespond where intername like '%{0}%' and result like '%{1}%'".format(iname,iresult)
        cursor.execute(sql)
        num = cursor.fetchall()[0][0]
        cursor.close()
        return num

    def DelInterface(self, iid): 
        """通过id删除表中数据"""
        cursor = self.con.cursor()
        sql = "delete from interfaceInfo where id={0}".format(iid)
        cursor.execute(sql)
        self.con.commit()
        cursor.close()
        return None

    def UpdateInterfaceWithId(self, iname, iaddr, iheader, iparam, ioption, iauthor, descp, expected, iuserpwd, iid):
        """通过id指定接口,修改待请求接口信息"""
        cursor = self.con.cursor()
        tt = time.strftime("%Y/%m/%d %H:%M:%S")
        sql = "update interfaceInfo set intername='{0}', interaddr='{1}', header='{2}', param='{3}', `option`='{4}', author='{5}', inputtime='{6}', descp='{7}', expected='{8}', account='{9}' where id='{10}'".format(iname,iaddr,iheader,iparam,ioption,iauthor,tt,descp,expected,iuserpwd,iid)
        cursor.execute(sql)
        self.con.commit()
        cursor.close()
        return None

    def getUiautoResult(self, imode):
        """获取UI自动化执行结果"""
        cursor = self.con.cursor()
        sql = "select * from uitestresult where id = (SELECT max(id) FROM uitestresult where mode='{0}')".format(imode)
        cursor.execute(sql)
        uires = cursor.fetchall()
        cursor.close()
        return uires


    def __del__(self):
        pass

class portalSql:
    
    def __init__(self):
        try:
            self.con = pymysql.connect(config.mysqlportal_host, config.mysqlportal_user, config.mysqlportal_passwd, 'j_portal')
        except pymysql.err.OperationalError:
            print('数据库无法连接')
    
    def delUser(self,myname=""):
        """根据手机号，email, 账号删除用户"""
        cursor = self.con.cursor()
        sql = "select id from user where binary account='{0}' or email='{0}' or mobile_phone='{0}'".format(myname)
        cursor.execute(sql)
        try:
            tmpid = cursor.fetchall()[0][0]
        except IndexError:
            return None
#        print(tmpid)
        sql1 = "delete from user where id='{0}'".format(tmpid)
        cursor.execute(sql1)
        self.con.commit()
        sql2 = "delete from user_detail where user_id='{0}'".format(tmpid)
        cursor.execute(sql2)
        self.con.commit()
        sql3 = "delete from user_role where user_id='{0}'".format(tmpid)
        cursor.execute(sql3)
        self.con.commit()
        cursor.close()
        return None

if __name__ == "__main__":
    a = lhlSql()
#    a.getInterfaceList()
#    b = portalSql()
#    b.delUser()
