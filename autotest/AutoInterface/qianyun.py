#!/usr/bin/env python3

import requests
import re, json

class NoQuoteSession(requests.Session):
    def send(self, prep, **send_kwargs):
        table = {
            urllib.parse.quote('{'): '{',
            urllib.parse.quote('}'): '}',
            urllib.parse.quote(':'): ':',
            urllib.parse.quote(','): ',',
            urllib.parse.quote('<'): '<',
            urllib.parse.quote('>'): '>',
        }
        for old, new in table.items():
            prep.url = prep.url.replace(old, new)
        return super().send(prep, **send_kwargs)

class TrickUrlSession(requests.Session):
    def setUrl(self, url):
        self._trickUrl = url
    def send(self, request, **kwargs):
        if self._trickUrl:
            request.url = self._trickUrl
        return requests.Session.send(self, request, **kwargs)

class qianyun():

    def __init__(self):
        self.myurl = "http://192.168.15.25"
        self.mycookie = self.login()
        self.header = {}
        self.header['Cookie'] = "JSESSIONID=" + self.mycookie

    def login(self):
         s = requests.Session()
         url = self.myurl + "/login"
         param = {}
         param["username"] = "sysadmin"
         param['password'] = "6b5ef696d9024671bb6cb8bff40c376b"
         param['encrypted'] = True
         param['loginType'] = "Normal"
         res = s.post(url,params=param)
      #   print(res.content)
       #  print(res.headers['Set-Cookie'])
       #  l1 = re.compile('CloudChef-Authenticate=(.*?);')
        # l2 = l1.findall(res.headers['Set-Cookie'])
         l1 = re.compile('JSESSIONID=(.*?);')
         l2 = l1.findall(res.headers['Set-Cookie'])
        # print(l2[0])
         return l2[0]    
    
    """业务功能"""


    #查询已有网络
    def queryExistNetwork(self):
        url = self.myurl + "/cloudprovider?action=queryCloudResource"
        self.header['Content-Type'] = "application/json"
        data = {
 "businessGroupId":None,
 "cloudResourceType": "cloudchef.openstack.nodes.Server::network",
 "cloudEntryId": ""
 }
        res = requests.post(url, headers=self.header, data=json.dumps(data))
        print(res.content)

    #获取卡片列表
    def queryCardList(self):
        url = self.myurl + "/catalogs/published?page=1&size=1&sort=asc"
        res = requests.get(url, headers=self.header)
        print(res.content)

    #获取卡片详情
    def queryCardInfo(self):
        url = self.myurl + "/catalogs/id"
        res = requests.get(url, headers=self.header)
        print(res.content)

    #获取卡片蓝图参数
    def queryCardParam(self):
        url = self.myurl + "/catalogs/id/inputs"
        res = requests.get(url, headers=self.header)
        print(res.content)

    #获取规格详情
    def querySpecsInfo(self):
        url = self.myurl + "/cloudprovider?action=queryCloudResource"
        self.header['Content-Type'] = "application/json"
        data = {
 "cloudResourceType":"cloudchef.openstack.nodes.Server::flavor",
    "queryProperties":{
  "physicalTemplateId":"",
  "logicTemplateId":"",
  "resourceBundleId":""
   }
}
        res = requests.post(url, headers=self.header,data=json.dumps(data))
        print(res.content)    

    #获取磁盘类型列表
    def queryDiskTypeList(self):
        url = self.myurl + "/cloudprovider?action=queryCloudResource"
        self.header['Content-Type'] = "application/json"
        data = {"cloudResourceType":"yacmp:cloudentry:type:openstack::volume-type"}
        res = requests.post(url, headers=self.header,data=json.dumps(data))
        print(res.content)  

    #申请虚机
    def applyVirtualMachine(self):
        url = self.myurl + "/catalogs/provision/deployment/id"
        self.header['Content-Type'] = "application/json"
        data = {
  "count": 1,
  "businessGroupId": "0f975778-1d94-4b61-8d6c-f369356b2a39",
  "projectId": "",
  "reason": "",
  "deploymentName": "",
  "paramJson": "[{\"Server_flavor\":\"31\",\"Server_server_vm_display_name\":\"test\",\"Server_server_logic_template_id\":\"56668877-d775-4a7a-9f14-56203a218fc6\",\"Server_server_physical_template_id\":\"e38609c1-115a-4253-be48-dd4c33e17f96\",\"Server_server_snapshotIndex\":\"\",\"Server_server_volume_type\":\"\",\"Server_server_volume_size\":null,\"Volume_volume_size\":10240,\"Volume_volume_volume_type\":\"\",\"Network_subnet_id\":\"9e454837-153a-4179-bf97-251a9347d07f\",\"Network_resource_id\":\"16c8cd40-a360-4451-86a8-338af7b88f0f\",\"FloatingIP_floatingip_floating_network_id\":\"ffa36b17-168b-4029-8ed3-ce91b239e615\",\"FloatingIP_floatingip_floating_ip_address\":\"192.168.15.58\",\"FloatingIP_floatingip_subnet_id\":\"894fe760-5c37-4e0c-b44a-f3541d78d293\",\"modify_pass_lin_root_pass\":\"Sugon@123\"}]",
  "kind": "PROVISION",
  "number": 4,
  "attachments": {},
  "ownerId": "sysadmin",
  "deploymentShutdownDuration": 3,
  "deploymentTeardownDuration": 2,
  "scheduleDate": None,
  "requestParameters": {"extensibleParameters": [{},{}, {},{}]},
  "nodes": [[],[],[],[]]
}
        res = requests.post(url, headers=self.header,data=json.dumps(data))
        print(res.content) 

    #重置密码
    def resetPasswd(self):
        url = self.myurl + "/nodes/id/execute-resource-action"
        self.header['Content-Type'] = "application/json"
        data = {"resourceActionId":"reset_password","executeParameters":{"username":"Administrator/root","newPassword":"XXXXXXXX"}}
        res = requests.post(url, headers=self.header,data=json.dumps(data))
        print(res.content) 

    #虚机关机
    def stopVirtualMachine(self):
        url = self.myurl + "/nodes/execute-action"
        self.header['Content-Type'] = "application/json"
        data = {"resourceActionId":"stop","scheduledTime":None}
        res = requests.post(url, headers=self.header,data=json.dumps(data))
        print(res.content)

    #虚机重启
    def resetVirtualMachine(self):
        url = self.myurl + "/nodes/id/execute-resource-action"
        self.header['Content-Type'] = "application/json"
        data = {"resourceActionId":"reboot","scheduledTime":None}
        res = requests.post(url, headers=self.header,data=json.dumps(data))
        print(res.content)

    #虚机卸载
    def uninstallVirtualMachine(self):
        url = self.myurl + "/deployments/execute-action"
        self.header['Content-Type'] = "application/json"
        data = {"XXXXXX(deploymentd)":{"operationName":"Tear Down","scheduledTime":None,"operationParamJson":"{}"}}
        res = requests.post(url, headers=self.header,data=json.dumps(data))
        print(res.content)

    #更新云主机名称
    def updateCloudName(self):
        url = self.myurl + "/nodes/id/execute-resource-action"
        self.header['Content-Type'] = "application/json"
        data = {"executeParameters":{"displayName":"XXXXXXX"},"resourceActionId":"update_display_name"}
        res = requests.post(url, headers=self.header,data=json.dumps(data))
        print(res.content)

    #远程登录
    def remoteLogin(self):
        url = self.myurl + "/nodes/id/consoleurl"
        res = requests.get(url, headers=self.header)
        print(res.content)

    #远程登录
    def remoteLogin(self):
        url = self.myurl + "/logic-templates/{system_id}/physical-templates"
        self.header['Content-Type'] = "application/json"
        data = {
    "flavorId":None,
    "sshPort":22,
    "validateType":"password",
    "authSecretKey":None,
    "authSshSecretKey":None,
    "authPassword":None,
    "customSpecName":None,
    "snapshotMode":"normal",
    "default":False,
    "alias":"Li001",
    "cloudEntryId":"118b14a0-76e7-4c0b-b161-85024dd9c3db",
    "templateId":"ef7ff919-34d0-496e-bee2-cb56e5cca902",
    "customSpecType":None,
    "monitorPort":9100,
    "bootType":"volumeboot",
    "deleteOnTermination":False,
    "sshEnable":True,
    "sshUserName":"root",
    "sshPassword":"123456",
    "monitorMode":"remote",
    "agentMode":"remote"
}
        res = requests.get(url, headers=self.header,data=json.dumps(data))
        print(res.content)


        """定时任务"""
        
    #云主机列表
    def hostlist(self):
        #session = TrickUrlSession()
        print(self.myurl)
        s = requests.Session()
        url = self.myurl + "/nodes/search?page=1&size=1&sort=createdDate,desc"
        param = {}
        param['page'] = "1"
        param['size'] = "10"
        param['sort'] = "CreatedDate,desc"
       # session.setUrl(url)
        res = s.get(url, headers=self.header)
        print(res.url)
        print(res.content)

    #云主机详情
    def hostInfo(self):
        print(self.myurl)
        s = requests.Session()
        url = self.myurl + "/nodes/id"
        res = s.get(url, headers=self.header)
        print(res.url)
        print(res.content)

    #查询操作系统
    def queryOperatingSystem(self):
        print(self.myurl)
        s = requests.Session()
        url = self.myurl + "/logic-templates/search?expand"
        res = s.get(url, headers=self.header)
        print(res.url)
        print(res.content)        

    #查询公共模板
    def queryPublicTemplate(self):
        print(self.myurl)
        s = requests.Session()
        url = self.myurl + "/logic-templates/{system_id}/physical-templates?expand=&businessGroupId&resourceBundleId"
        res = s.get(url, headers=self.header)
        print(res.url)
        print(res.content)  

    #查询网络
    def queryNetwork(self):
        print(self.myurl)
        s = requests.Session()
        url = self.myurl + "/cloudprovider?action=queryCloudResource"
        self.header['Content-Type'] = "application/json"
        data = {"cloudResourceType":"cloudchef.openstack.nodes.Server::network"}
        res = s.post(url, headers=self.header, data=data)
        print(res.url)
        print(res.content)  

    #查询子网
    def querySubnet(self):
        print(self.myurl)
        s = requests.Session()
        url = self.myurl + "/cloudprovider?action=queryCloudResource"
        self.header['Content-Type'] = "application/json"
        data = {"cloudResourceType":"yacmp:cloudentry:type:openstack::network-subnet","queryProperties":{"networkIds":"925e8b4e-60f3-4663-a2b1-e687953c0473"}}
        res = s.post(url, headers=self.header, data=data)
        print(res.url)
        print(res.content) 

    #查询部署操作历史
    def queryDeployOpertingHistory(self):
        print(self.myurl)
        s = requests.Session()
        url =  "http://159.226.90.23/deployments/{deploymentd}/tasks?page=1&size=10&sort=createdDate,desc"
        res = s.get(url, headers=self.header)
        print(res.url)
        print(res.content)  

    #查询部署详情
    def queryDeployInfo(self):
        print(self.myurl)
        s = requests.Session()
        url =  "http://159.226.90.23/deployments/{deploymentd}/details"
        res = s.get(url, headers=self.header)
        print(res.url)
        print(res.content) 


if __name__=="__main__":
    test = qianyun()
  #  test.hostlist()
  #  test.queryExistNetwork()
  #  test.queryCardList()
  #  test.queryCardInfo()
   # test.querySpecsInfo()
   # test.queryDiskTypeList()
   # test.applyVirtualMachineualMachine()
    test.resetPasswd()
