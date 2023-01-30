#!/usr/bin/env python3

import requests
import re, json


class ES():
    
    def queryPublicNetwork(self):
        url = "http://neutron.openstack.svc.cluster.local/v2.0/floatingips"
        self.header['Content-Type'] = "application/json"
        data = {
 "businessGroupId":None,
 "cloudResourceType": "cloudchef.openstack.nodes.Server::network",
 "cloudEntryId": ""
 }
        res = requests.post(url, headers=self.header, data=json.dumps(data))
        print(res.content)

    def eslogin(self):
        s = requests.Session()
        url = "http://keystone.openstack.svc.cluster.local/v3/auth/tokens"
        header = {}
        header['Content-Type'] = "application/json"
        param = { "auth": {
    "identity": {
      "methods": ["password"],
      "password": {
        "user": {
          "name": "admin",
          "domain": { "id": "default" },
          "password": "Admin@ES20!8"
        }
      }
    },
    "scope": {
      "project": {
        "name": "admin",
        "domain": { "id": "default" }
      }
    }
  }
}
        res = s.post(url, headers=header, data=json.dumps(param))
        print(res.content)
        return None
     

if __name__=="__main__":
    test = ES()
    test.eslogin()
