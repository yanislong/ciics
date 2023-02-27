#!/usr/bin/env python3

import time
import requests
import tpa_config

def login():
    # first request /token/login?hostUrl=http://sittpapc.ciics.cn
    url0 = "http://sitsso.ciics.cn/token/login?hostUrl=http://sittpapc.ciics.cn"
    r = requests.get(url0, allow_redirects=False)
    mycookie1 = r.headers['Set-Cookie'].split(";")[0]
    mysession1 = r.headers['Set-Cookie'].split(";")[3].split(',')[1]
    mycookie = mycookie1 + ";" + mysession1
    # second request /admin/token/getToken
    url = "http://sittpapc.ciics.cn/admin/token/getToken"
    header = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"}
    header['Cookie'] = mycookie
    r = requests.get(url, headers=header, allow_redirects=False)
    # third request /oauth2/authorization/icdcode
    mysession2 = r.headers['Set-Cookie'].split(";")[0]
    header = {'Cookie': mysession2}
    url = "http://sittpapc.ciics.cn/oauth2/authorization/icdcode"
    r = requests.get(url, headers=header, allow_redirects=False)
    # fourth request /oauth/authorize?response_type=
    locationurl = r.headers['Location']
    header= {}
    header['Cookie'] = mycookie
    header['Accept'] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    r = requests.get(locationurl, headers=header, allow_redirects=False)
    locationurl2 = r.headers['Location']
    # fifth request /token/login
    r = requests.get(locationurl2, headers=header, allow_redirects=False)
    locationurl3 = r.headers['Location']
    # sixth request /token/form
    url = "http://sitsso.ciics.cn/token/form"
    header = {}
    header['Cookie'] = mycookie
    data = {}
    data['username'] = tpa_config.username
    data['password'] = tpa_config.passwd
    data['loginType'] = "username"
    r = requests.post(url, headers=header, data=data, allow_redirects=False)
    # seventh request /oauth/authorize?
    mysession3 = r.headers['Set-Cookie'].split(";")[0]
    llurl1 = r.headers['Location']
    header1 = {'Cookie': mycookie1 + "; " + mysession3}
    r1 = requests.get(llurl1, headers=header1, allow_redirects=False)
    # eighth request login/oauth2/code/icdcode?
    llurl2 = r1.headers['Location']
    header2 = {'Cookie': mycookie1 + ";" + mysession2}
    r2 = requests.get(llurl2, headers=header2, allow_redirects=False)
    # ninth request /admin/token/getToken
    mysession4 = r2.headers['Set-Cookie'].split(";")[0]
    header3 = {'Cookie': mycookie1 + ";" + mysession4}
    url3 = "http://sittpapc.ciics.cn/admin/token/getToken"
    r3 = requests.get(url3, headers=header3, allow_redirects=False)
    try:
        #print(r3.headers['Authorization'])
        return r3.headers['Authorization']
    except KeyError:
        print("TPA用户登陆异常")
        return None

if __name__ == "__main__":
    login()
