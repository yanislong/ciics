#!/usr/bin/env python3

import requests
import json
from dis import dis

def test(num):
    url = "http://11.2.77.3/portal-test/org/org/insertProject"
    header = {}
    header['Content-Type'] =  "application/json;charset=utf-8"
    header['Authorization'] = "267f5c25-caa7-42cc-b0c0-0b02d375e144"
    data = {"projectName":"爱心早餐专项男友组" + str(num),"queueVos":[],"userDTO":[],"userName":"Sugon000","region":"","type":"1"}
    r = requests.post(url, headers=header, data=json.dumps(data))
    print(r.text)


if __name__ == "__main__":
    dis(test)
