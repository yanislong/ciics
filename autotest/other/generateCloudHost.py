#!/usr/bin/env python3

import requests
import json

import userInfo
import config

def submission():
    url = "http://" + config.testdata['u'] + "/portal/reApply/applyResource"
    header = {}
    header['Authorization'] = userInfo.login()
    header['Content-Type'] = "application/json"
    data = config.submitdata_GPUcentos76
    s = requests.Session()
    r = s.post(url, headers=header, data=json.dumps(data))
    print(r.text)

if __name__ == "__main__":
    submission()
