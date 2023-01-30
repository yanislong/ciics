#!/usr/bin/env python3

import requests
import json

def test():
    url = "https://sitsehwx.ciics.cn/user/uuser/userMiniAppRegister"
    header = {}
    header['content-type'] = "application/json"
    data = {"mobile":"13141032576","verifyCode":"1111","openId":"oeV-L5X-0ebYC9_EE-2cvIDQ4IGk","unionId":"oZgdjwaVlKh97xWBo9bwgU_cwFlM","appId":"wxa46c442dea82da8e","userSource":1}
    r = requests.post(url, headers=header, data=json.dumps(data))
    print(r.json())

def test2():
    url = "https://sitsehwx.ciics.cn/user/ucsms/sendCountdown"
    header = {}
    header['content-type'] = "application/json"
    data = "13141032576"
    r = requests.post(url, headers=header, data=data)
    print(r.json())

test()
#注册成功 {"code":0,"msg":"SUCCESS","data":{"loginCode":8,"loginMessage":"注册成功！","token":"f5428e0962944549a2b6d60441e798e2","subscribe":0,"openId":null,"unionId":null,"wxId":null}}
