#!/usr/bin/env python3

import requests
import hashlib
import json
import time
import random
import sys
sys.path.append('/root/lhl/myPerformance/GKJY-TEST/run_test/lhlmysql')
sys.path.append('/root/lhl/myPerformance/GKJY-TEST')

from lhlsql import lhlSql, portalSql
import  threading
import config
from multiprocessing import Process

def pt(num):
    tmp = [('gegege','13141032576')]
    url = config.userurl + "/reg/mobile/add"
    data = {}
    data['password'] = "12345678"
    header = {}
    header['Content-Type'] = "application/json"
    header['Connection'] = "close"
    for i in tmp:
        data['account'] = str(i[0])
        data['mobilePhone'] = str(i[1])
        for j in range(100000 * num, (100000 * num + 99999)):
            data['code'] = j
            print(data)
            reg = requests.post(url, headers=header, data=json.dumps(data))
            print(reg.text)
            if reg.json()['code'] == 200:
                print(i)
                print(reg.text)
                sys.exit()

def pp():
    tmp = []
    for nn in range(1,10):
        t =  threading.Thread(target=pt,args=(nn,))
        tmp.append(t)
        t.start()
    for j in tmp:
        j.join()

if __name__ == "__main__":
    print(time.strftime("%H%M%S",time.localtime()))
    time.sleep(3)
    a = (time.strftime("%H%M%S",time.localtime()))
    pp()
    print(time.strftime("%H%M%S",time.localtime()))
    print(time.strftime("%H%M%S",time.localtime()) -a )
    tmp = []
    for j in range(10,10):
        p = Process(target=pp,args=(j,))
        tmp.append(p)
        p.start()
    for j in tmp:
        j.join()
