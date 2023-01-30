import re, time

import win32gui
import win32con

import requests
from bs4 import BeautifulSoup
import pymysql
import casjc_log


#上传本地文件
def Casjc_upload(filePath, browser_type="chrome"):
    '''
    通过pywin32模块实现文件上传的操作
    :param filePath: 文件的绝对路径
    :param browser_type: 浏览器类型（默认值为chrome）
    :return:
    '''
    if browser_type.lower() == "chrome":
        title = "打开"
    elif browser_type.lower() == "firefox":
        title = "文件上传"
    elif browser_type.lower() == "ie":
        title = "选择要加载的文件"
    else:
        title = ""  # 这里根据其它不同浏览器类型来修改
    # 找元素
    # 一级窗口"#32770","打开"
    dialog = win32gui.FindWindow("#32770", u"打开")
    # 向下传递
    ComboBoxEx32 = win32gui.FindWindowEx(dialog, 0, "ComboBoxEx32", None)  # 二级
    comboBox = win32gui.FindWindowEx(ComboBoxEx32, 0, "ComboBox", None)   # 三级
    # 编辑按钮
    edit = win32gui.FindWindowEx(comboBox, 0, 'Edit', None)  # 四级
    # 打开按钮
    button = win32gui.FindWindowEx(dialog, 0, 'Button', "打开(&O)")  # 二级
    # 输入文件的绝对路径，点击“打开”按钮
    casjc_log.logging.info("上传本地文件" + filePath)
    win32gui.SendMessage(edit, win32con.WM_SETTEXT, None, filePath)  # 发送文件路径
    win32gui.SendMessage(dialog, win32con.WM_COMMAND, 1, button)  # 点击打开按钮


#临时邮箱
def Casjc_mail():
    ug = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"
    url = "http://24mail.chacuo.net/zhtw"
    header = {}
    header['User-Agent'] = ug
    #请求临时邮箱,获取当前邮箱地址,和cookie
    try:
        r = requests.get(url, headers=header)
        l1 = re.compile(r'sid=(.*)$')
        l2 = l1.findall(r.headers['Set-Cookie'])
        token = l2[0]
#        print(token)
        html = BeautifulSoup(r.content, features='lxml')
#        print(html)
        tmp = str(html.input['value'])
        email = tmp + "@chacuo.net"
        #print((email,tmp,token))
        return((email,tmp,token))
    except requests.exceptions.ConnectionError:
        casjc_log.logging.info("无法请求24mail.chacuo.net")
        return None
        


#获取邮箱验证码
def Casjc_mailcode(*res):
    url = "http://24mail.chacuo.net/zhtw"
    ug = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"
    reheader = {}
    reheader['User-Agent'] = ug
    reheader['X-Requested-With'] = "XMLHttpRequest"
    reheader['Cookie'] = "sid=" + res[0][2]
    eparam = {}
    eparam['data'] = res[0][1]
    eparam['type'] = "refresh"
    eparam['arg'] = ""
    for i in range(20):
        time.sleep(10)
        res2 = requests.post(url, headers=reheader, params=eparam)
        casjc_log.logging.info(res2.text)
        casjc_log.logging.info("等待%d秒没有获取到邮箱验证码"%(i*10))
        if res2.json()['data'][0]['list']:
            mid = res2.json()['data'][0]['list'][0]['MID']
            #print(mid)
            cparam = {}
            cparam['data'] = res[0][1]
            cparam['type'] = "mailinfo"
            cparam['arg'] = "f=" + str(mid)
            code = requests.post(url, headers=reheader, params=cparam)
#           print(code.text)
#           print(code.json()['data'][0][1][0]['DATA'])
            cc = code.json()['data'][0][1][0]['DATA'][0]
            ehtml = BeautifulSoup(cc, features='lxml')
            #获取到的验证码
            ccd = ehtml.find_all('span')[1]
            ccd = ccd.get_text()
            casjc_log.logging.info("获取到邮箱验证码" + str(ccd))
            #print(ccd)
            return ccd
    casjc_log.logging.info("等待200秒没有获取邮箱到验证码")
    return None


#获取邮箱密码
def Casjc_mailpasswd(*res):
    url = "http://24mail.chacuo.net/zhtw"
    ug = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"
    reheader = {}
    reheader['User-Agent'] = ug
    reheader['X-Requested-With'] = "XMLHttpRequest"
    reheader['Cookie'] = "sid=" + res[0][2]
    eparam = {}
    eparam['data'] = res[0][1]
    eparam['type'] = "refresh"
    eparam['arg'] = ""
    for i in range(20):
        time.sleep(10)
        res2 = requests.post(url, headers=reheader, params=eparam)
        casjc_log.logging.info(res2.text)
        #print(res2.text)
        casjc_log.logging.info("等待%d秒没有获取到邮箱的重置密码"%(i*10))
        if res2.json()['data'][0]['list']:
            mid = res2.json()['data'][0]['list'][0]['MID']
            #print(mid)
            cparam = {}
            cparam['data'] = res[0][1]
            cparam['type'] = "mailinfo"
            cparam['arg'] = "f=" + str(mid)
            code = requests.post(url, headers=reheader, params=cparam)
            #print(code.text)
#           print(code.json()['data'][0][1][0]['DATA'])
            cc = code.json()['data'][0][1][0]['DATA'][0]
            ehtml = BeautifulSoup(cc, features='lxml')
            #获取到的密码
            ccd = ehtml.find_all('span')[2]
            ccd = ccd.get_text()
            casjc_log.logging.info("获取到邮箱的重置密码" + str(ccd))
            #print(ccd)
            return ccd
    casjc_log.logging.info("等待200秒没有获取邮箱的重置密码")
    return None

#临时手机号
def Casjc_phone(num=0):
    ug = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"
    url = "http://yunjiema.net/zhongguohaoma/"
    header = {}
    header['User-Agent'] = ug
    try:
        r = requests.get(url, headers=header)
        html = BeautifulSoup(r.content, features='lxml')
        #print(html)
        tmp = html.find_all(class_="number-boxes-item-number")[num].string
        url = url + "86" + tmp[4:] + "/"
        casjc_log.logging.info("获取可用手机号: " + url)
        return (tmp[4:],url)
    except requests.exceptions.ConnectionError:
        casjc_log.logging.info("无法请求yunjiema.net")
        return None
    

#获取手机号验证码
def Casjc_phonecode(url):
    ug = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"
    header = {}
    header['User-Agent'] = ug
    tt = 1
    while tt<31:
        r = requests.get(url, headers=header)
        html = BeautifulSoup(r.content, features='lxml')
        #print(html)
        tmp = html.find_all(class_="col-xs-12 col-md-8")
        casjc_log.logging.info("等待%d秒没有获取到手机验证码"%(tt * 8))
        for i in tmp:
            if "国科晋云" in i.text:
                casjc_log.logging.info("获取手机号收到的验证码信息: " + i.text)
                l1 = re.compile('：(\d{6})，')
                l2 = l1.findall(i.text)
                casjc_log.logging.info(l2)
                casjc_log.logging.info("获取到手机证码" + str(l2[0]))
                return l2[0]
        time.sleep(8)
        tt += 1
    casjc_log.logging.info("等待240秒没有找到国科晋云验证码")
    return None
 

#脚本执行结果插入到数据库
def Run_result(*resdic):
    tt = time.strftime("%Y/%m/%d %H:%M:%S")
    con = pymysql.connect(host="10.0.20.91", port=33060, user="root", password="root", database='portaltest', charset="utf8mb4")
    cursor = con.cursor()
    sql = "insert into uitestresult(mode,stime,etime,result,exectime,env) value('{0}','{1}','{2}','{3}','{4}','{5}')".format(resdic[0][0],resdic[0][1],resdic[0][2],resdic[0][3],tt,resdic[0][4])
    cursor.execute(sql)
    con.commit()
    casjc_log.logging.info("执行结果插入到数据库")
    cursor.close()
    con.close()
    return None

if __name__ == "__main__":
    #a = Casjc_phone()
    #Casjc_phonecode(a[1])
    a =  r"c:\usr\AutoUi.pdf"
    Casjc_upload(a)

