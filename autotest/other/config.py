#!/usr/bin/env python3

import time
import random

testdata = {'u':"159.226.90.74",'u1':"159.226.90.74","username":"u3359167","passwd":"123456"}
#testdata = {'u':"1.71.191.200",'u1':"192.168.15.21","username":"u3359167","passwd":"123456"}

userinfo = {
        "applyType":1,
        "groupId":10062,
        "supportProject":"test",
        "applyNumber": time.strftime("%Y%m%d%H%M%S") + str(random.randint(100,999)), #"20190912104010309",
        "applyTime":time.strftime("%Y-%m-%d %H:%M:%S")
    }

validtime = "2019-09-30 23:59:59"

submitdata_GPUcentos76 = {
    "resourceApply": userinfo,
    "cloundResUser":{
        "serviceCard":"1f01ba45-c176-42c8-b6a8-dadf9f443a7e",
        "cardName":"通用型 - Linux",
        "instanceName":"GPUcentos7.6",
        "serverFlavor":"9",
        "applyCount":"1",
        "operationServiceId":"4a715372-0754-403d-a63b-c75cf053ba7e",
        "cpu":"1",
        "memory":"1",
        "imageType":1,
        "imageId":"e9431cde-b55c-4797-b20b-924c78d0209b",
        "imageName":"GPU镜像/centos7.6",
        "userName":"root",
        "password":"123456aA~",
        "networkId":"688cb018-8c0b-4d3d-8fb2-f9d21810b9c1",
        "subNetworkId":"0d3c5319-e305-47b1-9275-898ccc69f103",
        "validTime": validtime,
        "volumeVolumeSize":0,
        "resourceBundleId":"b7aa08e7-3417-4162-aabe-63d669842c41",
        "businessGroupId":"c0dd61c7-bbf1-406c-9fb1-7a79bb158e83",
        "serverServerVolumeType":"DS900_3_SSD",
        "serverServerVolumeSize":40,
        "crDiskList":[
            {
                "diskType":"1",
                "diskName":"SSD云盘",
                "diskSize":"40",
                "diskCount":"1"
            }
        ]
    }
}

submitdata_Hashdata = {
    "resourceApply": userinfo,
    "cloundResCard":{
        "serviceCard":"2706c460-c568-4ffe-b098-d5b5cbfaf7de",
        "cardName":"Hashdata服务",
        "applyCount":"1",
        "networkId":"688cb018-8c0b-4d3d-8fb2-f9d21810b9c1",
        "subNetworkId":"0d3c5319-e305-47b1-9275-898ccc69f103",
        "businessGroupId":"c0dd61c7-bbf1-406c-9fb1-7a79bb158e83",
        "masterServerServerVolumeSize":100,
        "masterServerServerVolumeType":"DS900_1_SSD",
        "masterServerServerLogicTemplateId":"4a715372-0754-403d-a63b-c75cf053ba7e",
        "masterResourceBundleId":"b7aa08e7-3417-4162-aabe-63d669842c41",
        "segmentServerServerVolumeSize":100,
        "segmentServerServerVolumeType":"DS900_1_SSD",
        "segmentServerServerLogicTemplateId":"4a715372-0754-403d-a63b-c75cf053ba7e",
        "segmentResourceBundleId":"b7aa08e7-3417-4162-aabe-63d669842c41",
        "ownerId":"6c491787-2628-4aef-b1f6-c171b94b0b4b",
        "hashdataUser":"hashUsername",
        "hashdataPas":"hashPasswd",
        "hashdataDB":"dataname",
        "modifyPassLinRootPass":"123456aA~",
        "modifyPassLin2RootPass":"123456aA~",
        "masterSpecifications":[
            {
                "name":"内存",
                "key":"memoryMB",
                "value":"8"
            },
            {
                "name":"vCPU",
                "key":"numCPUs",
                "value":"4"
            },
            {
                "name":"系统盘",
                "key":"rootDiskGB",
                "value":"100"
            }
        ],
        "segmentSpecifications":[
            {
                "name":"内存",
                "key":"memoryMB",
                "value":"8"
            },
            {
                "name":"vCPU",
                "key":"numCPUs",
                "value":"4"
            },
            {
                "name":"系统盘",
                "key":"rootDiskGB",
                "value":"100"
            }
        ],
        "validTime": validtime
    }
}

submitdata_centos73Base = {
    "resourceApply":userinfo,
    "cloundResUser":{
        "serviceCard":"1f01ba45-c176-42c8-b6a8-dadf9f443a7e",
        "cardName":"通用型 - Linux",
        "instanceName":"centos7.3Base",
        "serverFlavor":"9",
        "applyCount":"1",
        "operationServiceId":"4a715372-0754-403d-a63b-c75cf053ba7e",
        "cpu":"1",
        "memory":"1",
        "imageType":1,
        "imageId":"8d7b5068-a903-4efe-bc98-31abad2d1d58",
        "imageName":"centos7.3  基础设施版",
        "userName":"root",
        "password":"123456aA~",
        "networkId":"688cb018-8c0b-4d3d-8fb2-f9d21810b9c1",
        "subNetworkId":"0d3c5319-e305-47b1-9275-898ccc69f103",
        "validTime": validtime,
        "volumeVolumeSize":0,
        "resourceBundleId":"b7aa08e7-3417-4162-aabe-63d669842c41",
        "businessGroupId":"c0dd61c7-bbf1-406c-9fb1-7a79bb158e83",
        "serverServerVolumeType":"DS900_3_SSD",
        "serverServerVolumeSize":40,
        "crDiskList":[
            {
                "diskType":"1",
                "diskName":"SSD云盘",
                "diskSize":"40",
                "diskCount":"1"
            }
        ]
    }
}

submitdata_centos74Base = {
    "resourceApply":userinfo,
    "cloundResUser":{
        "serviceCard":"1f01ba45-c176-42c8-b6a8-dadf9f443a7e",
        "cardName":"通用型 - Linux",
        "instanceName":"centos7.4Base",
        "serverFlavor":"9",
        "applyCount":"1",
        "operationServiceId":"4a715372-0754-403d-a63b-c75cf053ba7e",
        "cpu":"1",
        "memory":"1",
        "imageType":1,
        "imageId":"564fc45b-14cd-4994-9261-0f4bcab6b813",
        "imageName":"centos7.4  基础设施版",
        "userName":"root",
        "password":"123456aA~",
        "networkId":"688cb018-8c0b-4d3d-8fb2-f9d21810b9c1",
        "subNetworkId":"0d3c5319-e305-47b1-9275-898ccc69f103",
        "validTime": validtime,
        "volumeVolumeSize":0,
        "resourceBundleId":"b7aa08e7-3417-4162-aabe-63d669842c41",
        "businessGroupId":"c0dd61c7-bbf1-406c-9fb1-7a79bb158e83",
        "serverServerVolumeType":"DS900_3_SSD",
        "serverServerVolumeSize":40,
        "crDiskList":[
            {
                "diskType":"1",
                "diskName":"SSD云盘",
                "diskSize":"40",
                "diskCount":"1"
            }
        ]
    }
}

submitdata_centos76Base = {
    "resourceApply":userinfo,
    "cloundResUser":{
        "serviceCard":"1f01ba45-c176-42c8-b6a8-dadf9f443a7e",
        "cardName":"通用型 - Linux",
        "instanceName":"centos7.6Base",
        "serverFlavor":"9",
        "applyCount":"1",
        "operationServiceId":"4a715372-0754-403d-a63b-c75cf053ba7e",
        "cpu":"1",
        "memory":"1",
        "imageType":1,
        "imageId":"39b686b8-e55d-4f64-99af-dcc39eca1757",
        "imageName":"centos7.6  基础设施版",
        "userName":"root",
        "password":"123456aA~",
        "networkId":"688cb018-8c0b-4d3d-8fb2-f9d21810b9c1",
        "subNetworkId":"0d3c5319-e305-47b1-9275-898ccc69f103",
        "validTime": validtime,
        "volumeVolumeSize":0,
        "resourceBundleId":"b7aa08e7-3417-4162-aabe-63d669842c41",
        "businessGroupId":"c0dd61c7-bbf1-406c-9fb1-7a79bb158e83",
        "serverServerVolumeType":"DS900_3_SSD",
        "serverServerVolumeSize":40,
        "crDiskList":[
            {
                "diskType":"1",
                "diskName":"SSD云盘",
                "diskSize":"40",
                "diskCount":"1"
            }
        ]
    }
}

submitdata_windows2008 = {
    "resourceApply":userinfo,
    "cloundResUser":{
        "serviceCard":"ff3f1769-cf20-4f15-bba0-f4d111afeafa",
        "cardName":"通用型 - Windows",
        "instanceName":"windows2008",
        "serverFlavor":"37",
        "applyCount":"1",
        "operationServiceId":"8922105f-f459-45b8-bdb8-0fdb3e159a2b",
        "cpu":"2",
        "memory":"4",
        "imageType":1,
        "imageId":"01828829-8b81-48b4-b606-bbf6f59c1467",
        "imageName":"windows 2008 r2",
        "userName":"root",
        "password":"123456aA~",
        "networkId":"688cb018-8c0b-4d3d-8fb2-f9d21810b9c1",
        "subNetworkId":"0d3c5319-e305-47b1-9275-898ccc69f103",
        "validTime": validtime,
        "volumeVolumeSize":0,
        "resourceBundleId":"b7aa08e7-3417-4162-aabe-63d669842c41",
        "businessGroupId":"c0dd61c7-bbf1-406c-9fb1-7a79bb158e83",
        "serverServerVolumeType":"DS900_3_SSD",
        "serverServerVolumeSize":40,
        "crDiskList":[
            {
                "diskType":"1",
                "diskName":"SSD云盘",
                "diskSize":"40",
                "diskCount":"1"
            }
        ]
    }
}

submitdata_windows2012 = {
    "resourceApply":userinfo,
    "cloundResUser":{
        "serviceCard":"ff3f1769-cf20-4f15-bba0-f4d111afeafa",
        "cardName":"通用型 - Windows",
        "instanceName":"windows2012",
        "serverFlavor":"37",
        "applyCount":"1",
        "operationServiceId":"8922105f-f459-45b8-bdb8-0fdb3e159a2b",
        "cpu":"2",
        "memory":"4",
        "imageType":1,
        "imageId":"d4624ef2-491c-4ef9-b1c2-66d7b133e86b",
        "imageName":"windows 2012 r2",
        "userName":"root",
        "password":"123456aA~",
        "networkId":"688cb018-8c0b-4d3d-8fb2-f9d21810b9c1",
        "subNetworkId":"0d3c5319-e305-47b1-9275-898ccc69f103",
        "validTime": validtime,
        "volumeVolumeSize":0,
        "resourceBundleId":"b7aa08e7-3417-4162-aabe-63d669842c41",
        "businessGroupId":"c0dd61c7-bbf1-406c-9fb1-7a79bb158e83",
        "serverServerVolumeType":"DS900_3_SSD",
        "serverServerVolumeSize":40,
        "crDiskList":[
            {
                "diskType":"1",
                "diskName":"SSD云盘",
                "diskSize":"40",
                "diskCount":"1"
            }
        ]
    }
}

submitdata_windows2016 = {
    "resourceApply":userinfo,
    "cloundResUser":{
        "serviceCard":"ff3f1769-cf20-4f15-bba0-f4d111afeafa",
        "cardName":"通用型 - Windows",
        "instanceName":"windows2016",
        "serverFlavor":"37",
        "applyCount":"1",
        "operationServiceId":"8922105f-f459-45b8-bdb8-0fdb3e159a2b",
        "cpu":"2",
        "memory":"4",
        "imageType":1,
        "imageId":"03794007-f3c8-4639-b10e-4b7066183445",
        "imageName":"windows server 2016",
        "userName":"root",
        "password":"123456aA~",
        "networkId":"688cb018-8c0b-4d3d-8fb2-f9d21810b9c1",
        "subNetworkId":"0d3c5319-e305-47b1-9275-898ccc69f103",
        "validTime": validtime,
        "volumeVolumeSize":0,
        "resourceBundleId":"b7aa08e7-3417-4162-aabe-63d669842c41",
        "businessGroupId":"c0dd61c7-bbf1-406c-9fb1-7a79bb158e83",
        "serverServerVolumeType":"DS900_3_SSD",
        "serverServerVolumeSize":40,
        "crDiskList":[
            {
                "diskType":"1",
                "diskName":"SSD云盘",
                "diskSize":"40",
                "diskCount":"1"
            }
        ]
    }
}

'''
print(submitdata_GPUcentos76)
print(submitdata_Hashdata)
print(submitdata_centos73Base)
print(submitdata_centos74Base)
print(submitdata_centos76Base)
print(submitdata_windows2008)
print(submitdata_windows2012)
print(submitdata_windows2016)
'''
