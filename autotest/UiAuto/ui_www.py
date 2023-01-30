import time, sys, json, random

from selenium import webdriver
from selenium.webdriver.common.action_chains import *
from selenium.common import exceptions
from selenium.webdriver.support.wait import WebDriverWait  
from selenium.webdriver.support import expected_conditions as EC  
from selenium.webdriver.common.by import By
import requests

import casjc_config
import casjc_mode
import casjc_log

    
#用户登陆
def Casjc_www_login(uname="", upasswd=""):
    title = "官网用户登录"
    uname = myconfig["entuser1"]
    upasswd = myconfig["entpasswd"]
    hailong = webdriver.Chrome()
    hailong.get(myconfig['consoleUrl'])
    hailong.maximize_window()
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'a[href="/login"]')))
    casjc_log.logging.info(title + " 点击登录按钮，进入登录页面")
    hailong.find_element_by_css_selector('a[href="/login"]').click()
    time.sleep(casjc_config.show_time)
    hailong.find_element_by_css_selector("input[type='text']").send_keys(uname)
    hailong.find_element_by_css_selector('input[type="password"]').send_keys(upasswd)
    hailong.find_element_by_tag_name('button').click()
    #等待casjc_config.wait_time全局设置时间(10秒)，判断是否登录成功进入首页
    try:
        WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="console"]')))
        if hailong.find_elements_by_css_selector('div[class="console"]')[0].text == "控制台":
            casjc_log.logging.info(title + " 登录成功")
            casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, "官网登录成功" ]
            if __name__ == "__main__":
                hailong.quit()
            return hailong
        else:
            casjc_log.logging.info(title + " 没有找到页面元素关键字<控制台>,登录异常")
            casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, "官网登录失败" ]
            hailong.quit()
            return None
    except exceptions.TimeoutException:
        imagename = title + time.strftime("%m%d%H%M%S") + '.png'
        hailong.save_screenshot(r'C:\usr\Apache24\htdocs\image\\' + imagename)
        casjc_log.logging.info(title + " 没有找到页面元素<控制台>,登录失败,查看截图 %s" %imagename)
        casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, "官网登录失败" ]
        hailong.quit()
        return None

#邮箱用户注册
def Casjc_www_mail_regist(uurl):
    title = "邮箱注册"
    hailong = webdriver.Chrome()
    hailong.get(uurl)
    hailong.maximize_window()
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'a[href="/register"]')))
    casjc_log.logging.info(title + " 点击注册按钮，进入注册页面")
    hailong.find_element_by_css_selector('a[href="/register"]').click()
    time.sleep(casjc_config.show_time)
    #main_window = hailong.current_window_handle
    #print(main_window)
    #print(hailong.current_url)
    #输入用户账户
    account = "uireg" + time.strftime("%m%d%H%M%S",time.localtime())
    casjc_log.logging.info(title + " 输入用户账号" + account)
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="el-tabs__content"]')))
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[0].send_keys(account)
    #输入密码
    casjc_log.logging.info(title + " 输入密码")
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[1].send_keys(casjc_config.regpasswd)
    #输入确认密码
    casjc_log.logging.info(title + " 输入确认密码")
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[2].send_keys(casjc_config.regpasswd)
    #输入邮箱
    tmpmail = casjc_mode.Casjc_mail()
    #tmpmail = "mhuzcd28730@chacuo.net"
    if not tmpmail:
        casjc_config.casjc_result[title + time.strftime("%M%S",time.localtime())] = ["", "无法请求24mail.chacuo.net,不能自动注册邮箱"]
        hailong.quit()
        return None
    casjc_log.logging.info(title + " 输入邮箱" + tmpmail[0])
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[3].send_keys(tmpmail[0])
    #点击页面使邮箱输入框失去焦点
    hailong.find_element_by_css_selector('div[class="wrap-reg"]').click()
    time.sleep(casjc_config.show_time)
    #点击获取验证码按钮
    casjc_log.logging.info(title + " 点击获取验证码按钮")
    hailong.find_element_by_css_selector('div[class="yzm"]').click()
    time.sleep(casjc_config.short_time)
    mailcode = casjc_mode.Casjc_mailcode(tmpmail)
    if not mailcode:
        casjc_config.casjc_result[title + time.strftime("%M%S",time.localtime())] = ["", "邮箱: " + tmpmail[0] +" 发送验证码后，200秒没有收到验证码"]
        hailong.quit()
        return None
    #输入验证码
    casjc_log.logging.info(title + " 输入验证码" + mailcode)
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[4].send_keys(mailcode)
    #点击注册按钮
    casjc_log.logging.info(title + " 点击注册按钮")
    hailong.find_element_by_css_selector('button[class="el-button el-button--primary"]').click()
    time.sleep(casjc_config.show_time)
    try:
        WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="nav-login"]')))
        casjc_log.logging.info(title + " 注册成功")
        casjc_config.casjc_result[title + time.strftime("%M%S",time.localtime())] = ["", "账号: " + account + "邮箱: " + tmpmail[0] + " 注册成功"]
        time.sleep(casjc_config.show_time)
        hailong.quit()
        return account
    except exceptions.TimeoutException:
        imagename = title + time.strftime("%m%d%H%M%S") + '.png'
        hailong.save_screenshot(r'C:\usr\Apache24\htdocs\image\\' + imagename)
        casjc_log.logging.info(title + " 页面元素未找到,注册异常, %s "%imagename)
        casjc_config.casjc_result[title + time.strftime("%M%S",time.localtime())] = ["", "账号: " + account + "邮箱: " + tmpmail[0] + " 注册失败"]
        hailong.quit()
        return None

#手机用户注册
def Casjc_www_phone_regist(uurl):
    title = "手机号注册"
    hailong = webdriver.Chrome()
    hailong.get(uurl)
    hailong.maximize_window()
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'a[href="/register"]')))
    casjc_log.logging.info(title + " 点击注册按钮，进入注册页面")
    hailong.find_element_by_css_selector('a[href="/register"]').click()
    time.sleep(casjc_config.show_time)
    #点击手机号注册tab
    casjc_log.logging.info(title + " 点击手机号注册tab，进入手机号注册页面")
    hailong.find_element_by_id('tab-phone').click()
    time.sleep(casjc_config.show_time)
    #输入用户账户
    account = "uireg" + time.strftime("%m%d%H%M%S",time.localtime())
    casjc_log.logging.info(title + " 输入用户账户" + account)
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[5].send_keys(account)
    #输入密码
    casjc_log.logging.info(title + " 输入密码")
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[6].send_keys(casjc_config.regpasswd)
    #输入确认密码
    casjc_log.logging.info(title + " 输入确认密码")
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[7].send_keys(casjc_config.regpasswd)
    #获取手机号
    num = 2
    while num<15:
        tmpphone = casjc_mode.Casjc_phone(num)
        num += 1
        if not tmpphone:
            casjc_config.casjc_result[title + time.strftime("%M%S",time.localtime())] = ["", "无法请求yunjiema.net,不能自动注册手机号"]
            hailong.quit()
            return None
        dd = {}
        dd["mobile"] = tmpphone[0]
        r = requests.post("http://11.2.77.3:30089/portal-test/user/reg/exist/mobile", data=dd)
        if r.json()['data'] == False:
            break           
        if num == 14:
            casjc_log.logging.info(title + " yunjiema.net,没有找到可用手机号码")
            casjc_config.casjc_result[title + time.strftime("%M%S",time.localtime())] = ["", "yunjiema.net,没有找到可用手机号码"]
            hailong.quit()
            return None
    #输入手机号
    casjc_log.logging.info(title + " 输入手机号" + tmpphone[0])
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[8].send_keys(tmpphone[0])
    #点击页面使邮箱输入框失去焦点
    hailong.find_element_by_css_selector('div[class="wrap-reg"]').click()
    time.sleep(casjc_config.show_time)
    #点击获取验证码按钮
    casjc_log.logging.info(title + " 点击获取验证码按钮")
    hailong.find_element_by_css_selector('div[class="yzm"]').click()
    time.sleep(casjc_config.wait_time)
    #输入验证码
    phonecode = casjc_mode.Casjc_phonecode(tmpphone[1])
    if not phonecode:
        casjc_config.casjc_result[title + time.strftime("%M%S",time.localtime())] = ["", "手机号: " + tmpphone[0] +" 发送验证码后，240秒没有收到验证码"]
        hailong.quit()
        return None
    casjc_log.logging.info(title + " 输入验证码" + phonecode)
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[9].send_keys(phonecode)
    #点击注册按钮
    casjc_log.logging.info(title + " 点击注册按钮")
    hailong.find_elements_by_css_selector('button[class="el-button el-button--primary"]')[1].click()
    time.sleep(casjc_config.show_time)
    try:
        WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="nav-login"]')))
        casjc_log.logging.info(title + " 注册成功")
        casjc_config.casjc_result[title + time.strftime("%M%S",time.localtime())] = ["", "账号: " + account + "手机号: " + str(tmpphone[0]) + " 注册成功"]
        hailong.quit()
        return None
    except exceptions.TimeoutException:
        imagename = title + time.strftime("%m%d%H%M%S") + '.png'
        hailong.save_screenshot(r'C:\usr\Apache24\htdocs\image\\' + imagename)
        casjc_log.logging.info(title + " 页面元素未找到，注册异常,查看截图 %s" %imagename)
        casjc_config.casjc_result[title + time.strftime("%M%S",time.localtime())] = ["", "账号: " + account + "手机号: " + str(tmpphone[0]) + " 注册失败"]
    hailong.quit()
    return None

#通过首页试用按钮进行登录
def Casjc_www_try(uname="aa123", upasswd="123456aA~"):
    title = "官网通过试用申请登录"
    hailong = webdriver.Chrome()
    hailong.get(myconfig['consoleUrl'])
    hailong.maximize_window()
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.LINK_TEXT, '申请试用')))
    casjc_log.logging.info(title + " 点击申请试用按钮")
    hailong.find_element_by_link_text('申请试用').click()
    time.sleep(casjc_config.short_time)
    #弹出提示框,选择马上登录
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'button[class="el-button el-button--default el-button--small el-button--primary "]')))
    hailong.find_element_by_css_selector('button[class="el-button el-button--default el-button--small el-button--primary "]').click()
    time.sleep(casjc_config.show_time)
    hailong.find_element_by_css_selector("input[type='text']").send_keys(uname)
    hailong.find_element_by_css_selector('input[type="password"]').send_keys(upasswd)
    hailong.find_element_by_tag_name('button').click()
    #等待casjc_config.wait_time全局设置时间(10秒)，判断是否登录成功进入首页
    try:
        WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="console"]')))
        if hailong.find_elements_by_css_selector('div[class="console"]')[0].text == "控制台":
            casjc_log.logging.info(title + " 登录成功")
            casjc_config.casjc_result[title + time.strftime("%M%S",time.localtime())] = [uname, "登录成功"]
            if __name__ == "__main__":
                hailong.quit()
            return hailong
        else:
            casjc_log.logging.info(title + " 页面元素未找到关键字<控制台>,登录异常")
            casjc_config.casjc_result[title + time.strftime("%M%S",time.localtime())] = [uname, "登录失败"]
            hailong.quit()
            return None
    except exceptions.TimeoutException:
        imagename = title + time.strftime("%m%d%H%M%S") + '.png'
        hailong.save_screenshot(r'C:\usr\Apache24\htdocs\image\\' + imagename)
        casjc_log.logging.info(title + " 页面元素未找到,登录失败,查看截图 %s" %imagename)
        casjc_config.casjc_result[title + time.strftime("%M%S",time.localtime())] = [uname, "登录失败"]
        hailong.quit()
        return None

    
if __name__ == "__main__":
    try:
        if sys.argv[1] == "dev":
            myconfig = casjc_config.devPerson['console']
            env = "dev"
        else:
            myconfig = casjc_config.testPerson['console']
            env = "test"
    except IndexError:
        myconfig = casjc_config.testPerson['console']
        env = "test"
    casjc_log.logging.info(">" * 15 + " UI自动化脚本开始执行执行 " + "<" * 15)

    start_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    Casjc_www_login()
    Casjc_www_mail_regist(myconfig['consoleUrl'])
    Casjc_www_phone_regist(myconfig['consoleUrl'])
    Casjc_www_try()
    
    end_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    print ("开始时间： " + start_time)
    print ("结束时间： " + end_time)
    print (">> UI自动化脚本执行完成")
    print(casjc_config.casjc_result)
    casjc_mode.Run_result(("www",start_time,end_time,json.dumps(casjc_config.casjc_result,ensure_ascii=False),env))
    casjc_log.logging.info( ">" * 15 + " 模块名: www, 本次UI自动化脚本执行完成，通过页面模块筛选查看执行结果 " + "<" * 15)
