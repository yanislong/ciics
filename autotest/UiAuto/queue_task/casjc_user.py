#!/usr/bin/env python3

import time, json, random
import requests
import casjc_login
import casjc_config
import casjc_log_task

class auser():
    def __init__(self):

        #登录后台管理员,获取token
        self.header = {}
        self.header['Token'] = casjc_login.login(casjc_config.ausername,casjc_config.apasswd,1)[0] 
        self.header['Content-Type'] = "application/json"

    def _selectUser_(self, cname):

        """[管理后台通过account查询企业用户]"""

        #通过account查寻企业用户
        url2 = casjc_config.global_url + "/portal-test/user/account/enterprise/list"
        data = {}
        data['account'] = cname
        data['pageNum'] = 1
        r2 = requests.post(url2, headers=self.header, data=json.dumps(data))
        if r2.status_code == 200:
            if r2.json()['code'] == 200 and r2.json()['data']['total'] >= 1:
                for i in r2.json()['data']['list']:
                    if i['account'] == cname:
                        userid = i['id']
                        casjc_log_task.logging.info(self._selectUser_.__doc__ + " 查询企业用户完成, 账号: " + cname)
                        return userid
            else:
                casjc_log_task.logging.info(self._selectUser_.__doc__ + " 查询企业用户异常, 账号: " + cname)
                return False
        else:
            casjc_log_task.logging.info(self._selectUser_.__doc__ + " 查询企业用户异常, 账号: " + cname + ", HTTP STATUS " + str(r2.status_code))
            return False

    def addControlUser(self, entid=10066):

        """[添加企业管理员用户,并修改密码]"""

        #添加新的企业用户
        url = casjc_config.global_url + "/portal-test/user/account/enterprise/add"
        cname = "man_" + str(time.strftime("%m%d%H%M",time.localtime()))
        data = {}
        data['account'] = cname
        data['companyAdminId'] = 0
        data['companyId'] = entid
        data['email'] = cname + "@qq.com"
        data['id'] = ""
        data['name'] = "我不要晴天"
        data['roleId'] = 3
        data['vnc'] = 0
        r = requests.post(url, headers=self.header, data=json.dumps(data))
        #print(r.json())
        if r.json()['code'] == 200 and r.json()['message'] == None and r.json()['data'] == None:
            casjc_log_task.logging.info(self.addControlUser.__doc__ + " 添加新的企业用户完成, 账号: " + cname)
        else:
            casjc_log_task.logging.info(self.addControlUser.__doc__ + " 添加新的企业用户异常, 账号: " + cname)
    
        userid = self._selectUser_(cname)

        #修改企业用户密码
        url3 = casjc_config.global_url + "/portal-test/user/updateUserPassword?password=" + casjc_config.cpasswd + "&userId=" + str(userid)
        r3 = requests.get(url3, headers=self.header)
        #print(r3.json())
        if r3.json()['code'] == 200 and r3.json()['data'] == None:
            casjc_log_task.logging.info(self.addControlUser.__doc__ + " 修改企业用户密码完成, 账号: " + cname)
        else:
            casjc_log_task.logging.info(self.addControlUser.__doc__ + " 修改企业用户密码异常, 账号: " + cname)
        #返回用户账号和用户id, 企业id
        time.sleep(1)
        return  cname, userid, entid

    def changePasswd(self, myaccount):

        """[管理后台修改企业用户密码]"""

        userid = self._selectUser_(myaccount)

        mima = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','k','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','K','U','V','W','X','Y','Z','1','2','3','4','5','6','7','8','9','_','~','!','@','#','$','%','^','&','*']
        mm = random.sample(mima, 12)
        mi = ""
        for i in mm:
            mi += i
        #修改企业用户密码
        url3 = casjc_config.global_url + "/portal-test/user/updateUserPassword?password=" + mi + "&userId=" + str(userid)
        r3 = requests.get(url3, headers=self.header)
        #print(r3.json())
        if r3.json()['code'] == 200 and r3.json()['data'] == None:
            casjc_log_task.logging.info(self.changePasswd.__doc__ + " 修改企业用户密码完成, 账号: " + myaccount + ' 修改后密码:' + mi)
            time.sleep(1)
            #返回用户账号和用户id, 密码
            return  myaccount, userid, mi
        else:
            casjc_log_task.logging.info(self.changePasswd.__doc__ + " 修改企业用户密码异常, 账号: " + myaccount + ' 修改后密码:' + mi)
            return False


class cuser():

    def __init__(self, cuser="job01181632"):

        #登录控制台管理员获取用户信息
        self.creatorName = cuser
        self.shenfen = casjc_login.login(self.creatorName,casjc_config.cpasswd,0)
        self.header = {}
        self.header['Content-Type'] = "application/json"
        self.header['Token'] = self.shenfen[0]

    def _selectUser_(self, cname):

        """[控制台通过account查询企业用户]"""

        #通过account查寻企业用户
        url2 = casjc_config.global_url + "/portal-test/user/getUserLdap?pageNum=1&pageSize=10&userId=" + str(self.shenfen[1]) + "&account=" + cname
        r2 = requests.get(url2, headers=self.header)
        #print(r2.json())
        if r2.json()['code'] == 200 and r2.json()['data']['total'] >= 1:
            for i in r2.json()['data']['list']:
                if i['account'] == cname:
                    casjc_log_task.logging.info(self._selectUser_.__doc__ + " 查询企业用户完成, 账号: " + cname)
                    userid = i['id']
                    return userid
            return False
        else:
            casjc_log_task.logging.info(self._selectUser_.__doc__ + " 查询企业用户异常, 账号: " + cname)
            return False

    def addEntUser(self):

        """[企业管理员添加普通用户,并修改密码]"""

        #控制台添加新的企业普通用户
        url = casjc_config.global_url + "/portal-test/user/insertUser?"
        cname = "cont" + str(time.strftime("%m%d%H%M",time.localtime()))
        data = {}
        data['account'] = cname
        data['companyId'] = self.shenfen[2]
        data['creatorId'] = self.shenfen[1]
        data['creatorName'] = self.creatorName
        data['parentId'] = self.shenfen[1]
        data['email'] = cname + "@qq.com"
        data['id'] = ""
        data['mobilePhone'] = None
        data['roleId'] = ""
        data['telephone'] = ""
        data['name'] = "控制台普通用户"
        data['vnc'] = 0
        r = requests.post(url, headers=self.header, data=json.dumps(data))
        #print(r.json())
        if r.json()['code'] == 200  and r.json()['data'] == True:
            casjc_log_task.logging.info(self.addEntUser.__doc__ + " 控制台添加新的企业用户完成, 账号: " + cname)
        else:
            casjc_log_task.logging.info(self.addEntUser.__doc__ + " 控制台添加新的企业用户异常, 账号: " + cname)
    
        userid = self._selectUser_(cname)

        #修复企业用户密码
        url3 = casjc_config.global_url + "/portal-test/user/updateUserPassword?password=" + casjc_config.cpasswd + "&userId=" + str(userid)
        r3 = requests.get(url3, headers=self.header)
        #print(r3.json())
        if r3.json()['code'] == 200 and r3.json()['data'] == None:
            time.sleep(1)
            casjc_log_task.logging.info(self.addEntUser.__doc__ + " 修改企业用户密码完成, 账号: " + cname)
            #返回用户账号和用户id, 用户姓名, 所属企业管理员id
            return  cname, userid, data['name'], self.shenfen[1]
        else:
            casjc_log_task.logging.info(self.addEntUser.__doc__ + " 修改企业用户密码异常, 账号: " + cname)
            return False

    def changePasswd(self, myaccount):

        """[修改企业普通用户密码]"""

        userid = self._selectUser_(myaccount)
 
        mima = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','k','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','K','U','V','W','X','Y','Z','1','2','3','4','5','6','7','8','9','_','~','!','@','#','$','%','^','&','*']
        mm = random.sample(mima, random.randint(8,20))
        mi = ""
        for i in mm:
            mi += i
        #修改企业用户密码
        url3 = casjc_config.global_url + "/portal-test/user/updateUserPassword?password=" + mi + "&userId=" + str(userid)
        r3 = requests.get(url3, headers=self.header)
        #print(r3.json())
        if r3.json()['code'] == 200 and r3.json()['data'] == None:
            time.sleep(1)
            casjc_log_task.logging.info(self.changePasswd.__doc__ + " 修改企业用户密码完成, 账号: " + myaccount + ' 修改后密码:' + mi)
            #返回用户账号和用户id, 用户姓名, 所属企业管理员id
            return  myaccount, userid, mi
        else:
            casjc_log_task.logging.info(self.changePasswd.__doc__ + " 修改企业用户密码异常, 账号: " + myaccount + ' 修改后密码:' + mi)
            return False

    def addQueueUser(self):

        """[企业管理员给普通用户,分配队列资源]"""

        #控制台添加新的企业普通用户
        myuser = self.addEntUser()

        url = casjc_config.global_url + "/portal-test/org/operationUserQueue"
        cname = "cont" + str(time.strftime("%m%d%H%M",time.localtime()))
        data = {}
        data["account"] = myuser[0]
        data["id"] = None
        data["name"] = myuser[2]
        data["queueUsers"] = [{"queueId":287,"nodeName":"low","userId": self.shenfen[1]}]
        data["usedCoreHour"] = None
        data["userId"] = myuser[1]
        r = requests.post(url, headers=self.header, data=json.dumps(data))
        #print(r.json())
        if r.json()['code'] == 200 and r.json()['message'] == None and r.json()['data'] == None:
            casjc_log_task.logging.info(self.addQueueUser.__doc__ + " 给普通企业用户分配队列资源完成, 账号: " + myuser[0])
            return myuser[0]
        else:
            casjc_log_task.logging.info(self.addQueueUser.__doc__ + " 给普通企业用户分配队列资源异常, 账号: " + myuser[0])
            return False
    
    def addStoreUser(self):

        """[企业管理员给普通用户,分配文件存储资源]"""

        #控制台添加新的企业普通用户
        myuser = self.addEntUser()

        url = casjc_config.global_url + "/portal-test/store/work/updateQuota"
        data = {}
        data["colonyId"] = 43
        data["groupLdapId"] = myuser[3]
        data["path"] = "/public1/home/" + self.creatorName + "/" + str(myuser[0])
        data["quotaSize"] = "10"
        data["quotaUnit"] = "GB"
        data["userId"] = myuser[1]
        r = requests.post(url, headers=self.header, data=json.dumps(data))
        #print(r.json())
        if r.json()['code'] == 200 and r.json()['message'] == None and r.json()['data'] == None:
            casjc_log_task.logging.info(self.addStoreUser.__doc__ + " 给普通企业用户分配文件存储资源完成, 账号: " + myuser[0])
            return myuser[0]
        else:
            casjc_log_task.logging.info(self.addStoreUser.__doc__ + " 给普通企业用户分配文件存储资源异常, 账号: " + myuser[0])
            return False

    def addQueueStoreUser(self):

        """[企业管理员给普通用户,分配队列和文件存储资源]"""

        #控制台添加新的企业普通用户
        myuser = self.addEntUser()

        #分配队列
        url = casjc_config.global_url + "/portal-test/org/operationUserQueue"
        cname = "cont" + str(time.strftime("%m%d%H%M",time.localtime()))
        data = {}
        data["account"] = myuser[0]
        data["id"] = None
        data["name"] = myuser[2]
        data["queueUsers"] = [{"queueId":287,"nodeName":"low","userId": self.shenfen[1]}]
        data["usedCoreHour"] = None
        data["userId"] = myuser[1]
        r = requests.post(url, headers=self.header, data=json.dumps(data))
        #print(r.json())
        if r.json()['code'] == 200 and r.json()['message'] == None and r.json()['data'] == None:
            casjc_log_task.logging.info(self.addQueueStoreUser.__doc__ + " 给普通企业用户分配队列资源完成, 账号: " + myuser[0])
        else:
            casjc_log_task.logging.info(self.addQueueStoreUser.__doc__ + " 给普通企业用户分配队列资源异常, 账号: " + myuser[0])
            return False

        #分配文件存储
        url = casjc_config.global_url + "/portal-test/store/work/updateQuota"
        data = {}
        data["colonyId"] = 43
        data["groupLdapId"] = myuser[3]
        data["path"] = "/public1/home/" + self.creatorName + "/" + str(myuser[0])
        data["quotaSize"] = "10"
        data["quotaUnit"] = "GB"
        data["userId"] = myuser[1]
        r = requests.post(url, headers=self.header, data=json.dumps(data))
        #print(r.json())
        if r.json()['code'] == 200 and r.json()['message'] == None and r.json()['data'] == None:
            casjc_log_task.logging.info(self.addQueueStoreUser.__doc__ + " 给普通企业用户分配文件存储资源完成, 账号: " + myuser[0])
            return myuser[0]
        else:
            casjc_log_task.logging.info(self.addQueueStoreUser.__doc__ + " 给普通企业用户分配文件存储资源异常, 账号: " + myuser[0])
            return False

if __name__ == "__main__":
    #管理后台操作
    atest = auser()
    #默认值参数企业id
    atest.addControlUser()
    #atest.changePasswd('test210125')

    #控制台操作,初始值参数企业管理员Id
    #ctest = cuser()
    #ctest.addEntUser()
    #ctest.addQueueUser()
    #ctest.addStoreUser()
    #ctest.addQueueStoreUser()
    #ctest.changePasswd('yan1819')
