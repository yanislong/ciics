#!/usr/bin/env python3

import xlrd
import pymysql
from bs4 import BeautifulSoup
import requests
import re, json, time, random

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def readData():
    resdata = []
    kong = []
    data = xlrd.open_workbook('tyc.xls')
    table = data.sheets()[0]
    #nrows = table.nrows
    nrows = 2
    #print(nrows)
    #print(table.row(1))
    con = pymysql.connect(host="127.0.0.1",user="zzqf",passwd="zzqf123",db="portaltest",charset="utf8mb4")
    cursor = con.cursor()
    #tt = time.strftime("%Y/%m/%d %H:%M:%S")
    seq = 1
    for i in range(seq,nrows):
        rtime = random.randint(1,3)
        time.sleep(rtime)
        print(seq)
        company = table.cell_value(i,1)
        #print(company)
        #companyUrl = getBody("巴彦淖尔市惠丰堂大药房连锁有限公司")
        companyUrl = getBody(company)
        print(companyUrl)
        if not companyUrl:
            kong.append(seq)
            seq += 1
            continue
        l1 = re.compile(r"company/(\d*)")
        companyId = l1.findall(companyUrl)
        #print(companyId[0])
        result = companyInfo(companyUrl,companyId[0])
        sql = "insert into tianyan2(seq,companyname,managestatus,industry,companytype,maxholder,shareholding,comaddres,addpost,usccode,estabdate,term,approval,regaddr,regcapital,incapital,managerange,legal,beneficiary,beneficiarypro,beneficiary2,beneficiarypro2,beneficiary3,beneficiarypro3,leader) value('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}','{18}','{19}','{20}','{21}','{22}','{23}','{24}')".format(seq,company,result[0],result[1],result[2],result[3],result[4],result[5],result[6],result[7],result[8],result[9],result[10],result[11],result[12],result[13],result[14],result[15],result[16][0][0],result[16][0][1],result[16][1][0],result[16][1][1],result[16][2][0],result[16][2][1],"-")
        cursor.execute(sql)
        con.commit()
        resdata.append(result)
        seq += 1
    cursor.close()
    print(kong)
    for i in resdata:
        pass
       # print(i)
    return None
    
def getBody(keyWorld):
    global header
    url = "https://www.tianyancha.com/search?key=" + keyWorld
    r = requests.get(url, headers=header)
    #print(r.status_code)
    #print(r.content)
    html = BeautifulSoup(r.text, features='lxml')
    #print(html.find('a',target='_blank'))
    #print(html.prettify())
    lll = html.find_all(name='a',target='_blank')
    #for i in lll:
    #    pass
    #    print(i)
    for i in lll:
        tmpname = i.get_text().replace("<em>","")
        tmpname = tmpname.replace("</em>","")
        #print(tmpname)
        if tmpname == keyWorld or tmpname == keyWorld[0:-1]:
            link = i.attrs['href']
            return link
    return None

def companyInfo(url,urlId):
    global header
    global token
    myheader = header
    mydata = []
    r = requests.get(url, headers=header)
    html = BeautifulSoup(r.content, features='lxml')
    lll = html.find(name='script',id='__NEXT_DATA__')
    mytext = lll.string
    mys = json.loads(mytext)
    #mytext1 = r.text
    #with open('test.html', 'w') as f:
    #    f.write(mytext1)
    #经营状态
    s1 = mys['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['data']['regStatus']
    #print(s1)
    mydata.append(s1)
    #行业
    try:
        s1 = mys['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['data']['industry']
    except:
        s1 = "-"
    #print(s1)
    mydata.append(s1)
    #公司类型
    try:
        s1 = mys['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['data']['companyShowBizTypeName']
    except:
        s1 = "-"
    #print(s1)
    mydata.append(s1)
    #最大股东
    myheader['Content-Type'] = "application/json"
    myheader['X-AUTH-TOKEN'] = token
    mydd = {"pageSize":20,"pageNum":1,"gid": urlId,"percentLevel":-100,"sortField":"capitalAmount","sortType":-100}
    r = requests.post("https://capi.tianyancha.com/cloud-company-background/companyV2/dim/holderForWeb", headers=myheader, data=json.dumps(mydd))
    #print(r.json())
    try:
        s1 = r.json()['data']['result'][0]['name']
    except:
        s1 = "-"
    #s1 = mys['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['data']['companyShowBizTypeName']
    #print(s1)
    mydata.append(s1)
    #持股比例
    try:
        s1 = r.json()['data']['result'][0]['capital'][0]['percent']
    except:
        s1 = "-"
    #s1 = mys['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['data']['companyShowBizTypeName']
    #print(s1)
    mydata.append(s1)
    #通讯单位地址
    #s1 = mys['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['data']['companyShowBizTypeName']
    s1 = mys['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['data']['taxAddress']
    #print(s1)
    mydata.append(s1)
    #地址邮编
    #s1 = mys['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['data']['companyShowBizTypeName']
    s1 = "-"
    #print(s1)
    mydata.append(s1)
    #统一社会信用代码
    s1 = mys['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['data']['taxNumber']
    #print(s1)
    mydata.append(s1)
    #成立日期
    r = requests.post("https://capi.tianyancha.com/cloud-company-background/company/peer/analysis?companyGid=" + urlId, headers=myheader)
    try:
        s1 = r.json()['data']['establishmentDate']
        mydata.append(s1)
    except:
        try:
            s1 = mys['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['data']['baseInfo']
            #print(s1)
            l1 = re.compile(r'成立于(.*?)，')
            s2 = l1.findall(s1)
            if not s2:
                l1 = re.compile(r'公司于(.*?)在')
                s2 = l1.findall(s1)
            if not s2:
                l1 = re.compile(r'创立于(.*?)的')
                s2 = l1.findall(s1)
            #print(s2)
            mydata.append(s2[0])
        except:
            mydata.append("-")
    #营业期限
    #s1 = mys['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['data']['companyShowBizTypeName']
    s1 = "-"
    #print(s1)
    mydata.append(s1)
    #核准日期
    r = requests.post("https://capi.tianyancha.com/cloud-company-background/company/changeinfoEm?gid=" + urlId + "&pageNum=1&pageSize=10&changeItem=-100", headers=myheader)
    try:
        s1 = r.json()['data']['result'][0]['changeTime']
    except:
        try:
            s1 = mys['props']['pageProps']['dehydratedState']['queries'][10]['state']['data']['data'][0]['date']
        except:
            s1 = "-"
    #print(s1)
    mydata.append(s1)
    #注册地址
    s1 = mys['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['data']['taxAddress']
    #print(s1)
    mydata.append(s1)
    #注册资本
    try:
        s1 = mys['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['data']['regCapital']
    except:
        s1 = "-"
    #print(s1)
    mydata.append(s1)
    #实缴资本
    try:
        s1 = mys['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['data']['actualCapital']
    except:
        s1 = "-"
    #print(s1)
    mydata.append(s1)
    #经营范围
    try:
        s1 = mys['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['data']['businessScope']
    except:
        s1 = "-"
    #print(s1)
    mydata.append(s1)
    #法定代表人
    s1 = mys['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['data']['legalPersonName']
    #print(s1)
    mydata.append(s1)
    #最终受益人姓名和最终受益人占比
    tmpurl = "https://capi.tianyancha.com/cloud-equity-provider/v4/hold/humanholdingV2?id=" + str(urlId) + "&pageSize=10&pageNum=1"
    myheader['version'] = "TYC-Web"
    r = requests.get(tmpurl, headers=myheader)
    #print(r.json())
    try:
        s1 = r.json()['data']['list']
    except:
        s1 = []
    #print(len(s1))
    beneficiary = []
    if len(s1) > 3:
        s1 = s1[0:3]
    for i in s1:
        #print(i)
        try:
            bene = i['name']
        except KeyError:
            bene = "-"
        try :
            bene2 = i['percent']
        except KeyError:
            bene2 = "-"
        tmp = [bene,bene2]
        beneficiary.append(tmp)
    if len(s1) == 2:
        tmp2 = ["-","-"]
        beneficiary.append(tmp2)
    if len(s1) == 1:
        tmp3 = ["-","-"]
        tmp4 = ["-","-"]
        beneficiary.append(tmp3)
        beneficiary.append(tmp4)
    if len(s1) == 0:
        tmp3 = ["-","-"]
        tmp4 = ["-","-"]
        tmp5 = ["-","-"]
        beneficiary.append(tmp3)
        beneficiary.append(tmp4)
        beneficiary.append(tmp5)
    #print(beneficiary)
    mydata.append(beneficiary)
    #print(mydata)
    #time.sleep(100)
    return mydata
    '''
    #经营状态
    l1 = re.compile(r'regStatus":"(.*?)"')
    l2 = l1.findall(mytext)
    print(l2[0])
    mydata.append(l2[0])
    #行业
    l1 = re.compile(r'regStatus":"(.*?)"')
    l2 = l1.findall(mytext)
    print(l2[0])
    mydata.append(l2[0])
    #公司类型
    l1 = re.compile(r'regStatus":"(.*?)"')
    l2 = l1.findall(mytext)
    print(l2[0])
    mydata.append(l2[0])
    '''

if __name__ == "__main__":
    mydata = []
    header = {}
    header['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
    header['If-None-Match'] = "1b039-I7jV0burh9dyMRFKDZqStBBTmZE"
    header['Cookie'] = "HWWAFSESID=088aa1d299859b5d8cf; HWWAFSESTIME=1661503584150; csrfToken=ONw34_exyNEhDojmV-So78i4; jsid=SEO-BAIDU-ALL-SY-000001; TYCID=914e35c0251b11eda4a44f37120d21e7; bdHomeCount=0; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1661503585; _bl_uid=X5lvd7R6aq18jdgz1mU30k45kCsU; bannerFlag=true; tyc-user-info=%7B%22state%22%3A%227%22%2C%22vipManager%22%3A%220%22%2C%22mobile%22%3A%2213918484932%22%2C%22isExpired%22%3A%220%22%7D; RTYCID=8d948210e28b450f9e95d0a0d518d7a9; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%229564146%22%2C%22first_id%22%3A%22182d954bb6c843-072ddcbe3105d44-26021d51-2073600-182d954bb6dbbd%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfbG9naW5faWQiOiI5NTY0MTQ2IiwiJGlkZW50aXR5X2Nvb2tpZV9pZCI6IjE4MmQ5NTRiYjZjODQzLTA3MmRkY2JlMzEwNWQ0NC0yNjAyMWQ1MS0yMDczNjAwLTE4MmQ5NTRiYjZkYmJkIn0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%229564146%22%7D%2C%22%24device_id%22%3A%22182d954bb6c843-072ddcbe3105d44-26021d51-2073600-182d954bb6dbbd%22%7D; relatedHumanSearchGraphId=3075384519; relatedHumanSearchGraphId.sig=JvA2iERscSammEJNQQRTvRIDsuBM4TQUD7IBcDYiwC0; ssuid=3993149616; _ga=GA1.2.1987416229.1661751390; _gid=GA1.2.1013022565.1661751390; tyc-user-info-save-time=1661755009022; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzkxODQ4NDkzMiIsImlhdCI6MTY2MTc1NTAwNiwiZXhwIjoxNjY0MzQ3MDA2fQ.cmC3Tp7UbytL2BQblwCGz2An8xWN-iFYxW0anR2HMBKcoO9FOtdK55vO2WYkBvcu8QHJ2DE7pX-CZi_OE_WCTw; cloud_token=d9ab607f102d434c863c66ce9a91c63e; cloud_utm=c9a43a49c1134f91ad880cb334071301; searchSessionId=1661755032.34494607; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1661755035"
    token = ""
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0")
    driver = webdriver.PhantomJS(executable_path='./phantomjs-2.1.1-linux-x86_64/bin/phantomjs', desired_capabilities=dcap)
    driver.get('http://www.tianyancha.com/company/2310290454')
    time.sleep(5)
    # 获取网页内容
    content = driver.page_source.encode('utf-8')
    driver.close()
    print(content)
    #readData()
