#!/usr/bin/env python3

import time
import hashlib
import base64


#################FLASK配置################################
SECRET_KEY = "1234567890"

#################全局配置################################

#测试平台名称
#name = "国科晋云"
name = "中智企服"
#追求真相
saying = "根本没有巧合, 巧合是种错觉"
#首页外链bug平台地址
#bugurl = "https://www.tapd.cn/company/participant_projects"
bugurl = "https://jira.ciics.com/"
#接口模块
intermode = ['user','order','job','flow','account','contract','invoice','file','messcenter','org','ldap']
#接口请求方法
option = ['get','post']
#接口开发者
author = ['杨东升','杜丽','丁旭','张亚辉','梁永全']
#是否开启身份认证
authorized = ""#True
#是否开启音乐
#music = "autoplay"
music = ""

#发送邮件接收人
emaillist = ["xul@ciics.com"]

#执行ui自动化远程主机ip
runui_ip = "http://10.0.20.91:8089/casjc.log?cache=0"
runui_ip2 = "192.168.97.52"
#runui_ip = "10.0.110.251"
#执行ui自动化远程主机port
runui_port = 8001
exeshell = "zzqfpython ciics_master.py"

#################################################

#########################数据库,服务器地址配置#############################

#本地数据库
mysql_host = "127.0.0.1"
mysqluser = "zzqf"
#mysqlpasswd = "Casjc@20210226"
mysqlpasswd = "zzqf123"

#测试环境应用服务地址
url = "http://11.2.77.3:30088"
testurl = "11.2.77.3:30089"
#接口模块地址
userurl = url + "/portal-test/user"
orderurl = url + "/portal-test/order"
joburl = url + "/portal-test/job"
orgurl = url + "/portal-test/org"
contracturl = url + "/portal-test/contract"

#开发环境服务地址
'''
#testurl = "11.2.77.1"
#url = "http://11.2.77.1"
#接口模块地址
userurl = url + "/portal/user"
orderurl = url + "/portal/order"
joburl = url + "/portal/job"
orgurl = url + "/portal/org"
contracturl = url + "/portal/contract"
'''

#测试环境数据库
mysqlportal_host = "192.168.15.21"
mysqlportal_user = "root"
mysqlportal_passwd = "root"
#mysqlportal_passwd = "Test~107443"

######################################################################

####################测试数据####################################

#注册不删除用户
#useaccount = {'lizongwu':'17344432202'} #,'LIZONGWU':'335916781@qq.com'}
#useaccount = {'Demo001':'17344432202'}
#useaccount = {'ZhangEmailuser163':'17344432202'} 
useaccount = 'yanislong'

#通用密码
#passwd = "12345678"
#passwd = "Test123456!"
#passwd = "Zhang@2019"
passwd = "ODc3ZmFkND"

#已注册账号手机号,长度要保持一直
account = ["test123test","a12345","ab012345678901234567890123456789","LIXIAOFENG","kali001"]
mobile = ["16688888612","16688888613","16688888614","16688888615","16688888616"]

#非法账号名
noAccount = ["0123456","a1234","abc123456789012345678901234567890","a!@#$%^&","1abcdefg","root","admin","administrator",""," ",None]

############################################################################

######################全局方法###############################

#提供参数,返回MD5值
def mm(parm):
    m1 = hashlib.md5(parm.encode())
    return m1.hexdigest()

#返回当前时间
def mydatatime():
    return time.strftime("%m%d %H%M%S",time.localtime())

#返回11位随机数([0-9a-zA-Z])
def suiji():
    a = ''.join(random.sample(['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a','Z','Y','X','U','V','W','Q','E','R','T','I','O','P','A','S','D','F','G','H','H','J','K','L','C','B','N','M','1','2','3','4','5','6','7','8','0','9'], 11))
    return a

#sale进行sha1
def jm_sha1(parm):
    jmobj = hashlib.sha1()
    jmobj.update(parm.encode('utf-8'))
#    print(jmobj.digest_size)
    return jmobj.hexdigest()

#sale加上密码进行sha256
def jm_sha256(parm,b):
    jmobj = hashlib.sha256()
    jmobj.update(parm.encode('utf-8'))
    jmobj.update(b.encode('utf-8'))
    print(jmobj.digest())
    return jmobj.hexdigest()

#十六进制转二进制(byte)
def hexStringTobytes(str):
    str = str.replace(" ", "")
    print(bytes.fromhex(str))
    return bytes.fromhex(str)

#二进制(byte)转十六进制
def bytesToHexString(bs):
    return ''.join(['%02X' % b for b in bs])

#####################################################

#####################################################

if __name__ == "__main__":
    aa = jm_sha1("574ff13b-93cd-437a-9283-524250c038bfDemo001")
    bb = jm_sha256('Test123456!', aa)
    cc = "5166D92F37C9DFA6EC863E5A2EB1B58146F8F24DA27D1BB38E9F6ED960627ED8"
#    hexStringTobytes(cc)
#    print(base64.b64encode(bb.encode('utf-8')))
    pass
