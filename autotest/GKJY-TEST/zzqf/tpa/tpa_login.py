#!/usr/bin/env python3

import time
import requests
import tpa_config

def login():
    url0 = "http://sitsso.ciics.cn/token/login?hostUrl=http://sittpapc.ciics.cn"
    r0 = requests.get(url0, allow_redirects=False)
    tmp0 = r0.headers['Set-Cookie'].split(";")
    #print(tmp0[0])
    url00 = "http://sittpapc.ciics.cn/admin/token/getToken"
    header = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"}
    r00 = requests.get(url00, headers=header, allow_redirects=False)
    tmp00 = r00.headers['Set-Cookie'].split(";")
    #print(tmp00[0])
    header000 = {'Cookie': tmp00[0]}
    url000 = "http://sittpapc.ciics.cn/oauth2/authorization/icdcode"
    r000 = requests.get(url000, headers=header000, allow_redirects=False)
    locationurl = r000.headers['Location']
    #print(locationurl)
    header0000= {}
    header0000['Cookie'] = tmp0[0]
    header0000['Accept'] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    r0000 = requests.get(locationurl, headers=header0000, allow_redirects=False)
    locationurl2 = r0000.headers['Location']
    #print(locationurl2)
    r00000 = requests.get(locationurl2, headers=header0000, allow_redirects=False)
    locationurl3 = r00000.headers['Location']
    #print(locationurl3)
    url = "http://sitsso.ciics.cn/token/form"
    header = {}
    header['Cookie'] = tmp0[0]
    data = {}
    data['username'] = tpa_config.username
    data['password'] = tpa_config.passwd
    data['loginType'] = "username"
    r = requests.post(url, headers=header, data=data, allow_redirects=False)
    tmp1 = r.headers['Set-Cookie'].split(";")
    llurl1 = r.headers['Location']
    header1 = {'Cookie': tmp1[0]}
    r1 = requests.get(llurl1, headers=header1, allow_redirects=False)
    llurl2 = r1.headers['Location']
    header2 = {'Cookie': tmp00[0]}
    r2 = requests.get(llurl2, headers=header2, allow_redirects=False)
    #print(r2.headers)
    tmp2 = r2.headers['Set-Cookie'].split(";")
    url3 = "http://sittpapc.ciics.cn/admin/token/getToken"
    header3 = {'Cookie': tmp2[0]}
    r3 = requests.get(url3, headers=header3, allow_redirects=False)
    #print(r3.headers['Authorization'])
    return r3.headers['Authorization']

if __name__ == "__main__":
    login()
