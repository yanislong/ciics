#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Thu Jul 21 16:45:44 2022
@author: bfliushida

"""

# 本次整体的源代码
myak =  'LaeemuDaqGvcwciYTqrPoWrp66Fgj0iF'
 
import pandas as pd
import requests
import json
import sys, time
from itertools import combinations
 
def getPosition(address):
    global myak
    url = r"http://api.map.baidu.com/place/v2/search?query={}&region=全国&output=json&ak={}".format(
        address,
        'NAwGuQe2WmQ7RSdvQIafcZ0Kjnv8Aldc'
    )
    url = "https://api.map.baidu.com/place/v2/suggestion?query={}&region={}&city_limit=true&output=json&ak={}".format(address,address,myak)
    res = requests.get(url)
   # print(res.url)
    json_data = json.loads(res.text)
    if json_data['status'] == 0:
        try:
            lat = json_data["result"][0]["location"]["lat"]  # 纬度
            lng = json_data["result"][0]["location"]["lng"]  # 经度
        except KeyError:
            print(res.json())
            return "0,0", json_data["status"]
    else:
        print("[ERROR] Can not find {}.".format(address))
        return "0,0", json_data["status"]
    return str(lat) + "," +  str(lng), json_data["status"]
 
 
def getDistance(start, end):
    global myak
    url = "http://api.map.baidu.com/routematrix/v2/driving?output=json&origins={}&destinations={}&ak={}".format(
        start,
        end,
        'NAwGuQe2WmQ7RSdvQIafcZ0Kjnv8Aldc' 
    )
    url = "https://api.map.baidu.com/direction/v2/motorcycle?origin=4846797.3,12948640.7&destination=4836829.84,12967554.88&coord_type=bd09mc&ak=您的A"
    #未开通
    url = "https://api.map.baidu.com/logistics_direction/v1/truck?origin={}&destination={}&ak={}".format(start,end,myak)
    url = "https://api.map.baidu.com/directionlite/v1/driving?origin={}&destination={}&ak={}".format(start,end,myak)
    res = requests.get(url)
    #print(res.json())
    try :
        dist = res.json()["result"]["routes"][0]["distance"]
    except KeyError:
        return 0
    #print(dist)
    return dist
 
 
def calcDistance(startName, endName):
    start, status1 = getPosition(startName)
    print(start,status1)
    end, status2 = getPosition(endName)
    print(end,status2)
    if status1 == 0 and status2 == 0:
        return getDistance(start, end)
    else:
        return -1
 
 
if __name__ == "__main__":
    data = pd.read_excel("city_data.xlsx")
    res1 = []
    res2 = []
    for num_city in range(0,6):
        data1 = data.iloc[num_city,0]
        res1.append(data1)
    print(res1)
 
    for i in combinations(res1,2):
        startName = i[0]
        endName = i[1]
        dist = calcDistance(startName, endName)
        res2.append([startName, endName,dist/1000])
    print(res2)
    sys.exit()
 
    pd.DataFrame(res2).to_excel(
        "result2.xlsx",
        header=["起点", "终点",'距离'],
        index=None,
        encoding="utf-8"
    )

