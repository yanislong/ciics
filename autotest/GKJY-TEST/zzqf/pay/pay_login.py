#!/usr/bin/env python3

import time
import requests

import pay_config
import ciics_log

def login(username,passwd):
    url = pay_config.global_url + "/o2ocheck/cashier/login/login_post"
    data = {}
    data['userName'] = username
    data['password'] = passwd
    r = requests.post(url, data=data)
    if r.json()['result'] == "OK":
        tt = r.json()['token']
        uname = r.json()['data']['userName']
        ciics_log.logging.info("用户登录成功,当前登陆用户为:{0},用户token值:{1}".format(uname,tt))
        return tt
    else:
        print("登陆失败")
        print(r.json())
        return None


if __name__ == "__main__":
    name = "lpsyy"
    passwd = "fMRQjArXddOlX1f1RuSypxSv7Q6t+BeC8kUZRZo7LDJusLrB6uMcbonf2L6CX7B9tjx3KLfVuwArrpoRDGrX2XQypGOVNDIIpOAJDdtYzUsOAac2pxlCYNaJpGJQ5u7SpV3rkjAeFaYFn8mDuSsoPiMFWHTde7DG+owULTH5eT0="
    login(name,passwd)
