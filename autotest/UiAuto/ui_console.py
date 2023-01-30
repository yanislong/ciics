import time, sys, json, random

from selenium import webdriver
from selenium.webdriver.common.action_chains import *
from selenium.common import exceptions
from selenium.webdriver.support.wait import WebDriverWait  
from selenium.webdriver.support import expected_conditions as EC  
from selenium.webdriver.common.by import By

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


#get直接返回，不再等待界面加载完成
desired_capabilities = DesiredCapabilities.CHROME
desired_capabilities["pageLoadStrategy"] = "none"

import casjc_config
import casjc_mode
import casjc_page
import casjc_log
import ui_www

#控制台-共享存储-上传文件
def Casjc_console_upfile():
    title = "数据存储-上传文件"
    #登录控制台
    uname = myconfig["entuser2"]
    upasswd = myconfig["entpasswd"]
    uurl = myconfig["consoleUrl"]
    hailong = webdriver.Chrome()
    aaa = casjc_page.Casjc_console_page(hailong,uname,upasswd,uurl)
    #进入控制台
    casjc_log.logging.info(title + " 进入控制台")
    aaa.console()
    #聚焦总览页面菜单产品图标，页面样式已改废弃下面操作
    '''
    impl = hailong.find_element_by_css_selector('i[class="el-icon-caret-bottom"]')
    tmp =  hailong.find_element_by_tag_name('body')
    chain = ActionChains(hailong)
    chain.move_to_element(impl).perform()
    time.sleep(casjc_config.short_time)
    '''
    #点击高性能计算
    casjc_log.logging.info(title + " 点击高性能计算")
    hailong.find_elements_by_css_selector('span[class="innerText"]')[1].click()
    #chain.move_to_element(tmp).perform()
    time.sleep(casjc_config.show_time)
    #点击共享存储菜单
    casjc_log.logging.info(title + " 点击共享存储菜单")
    hailong.find_elements_by_css_selector('b[class="iconfont iconbaocun mr10 fwn"]')[0].click()
    time.sleep(casjc_config.show_time)
    #点击上传按钮
    casjc_log.logging.info(title + " 点击上传按钮")
    hailong.find_elements_by_css_selector('button[slot="reference"]')[0].click()
    time.sleep(casjc_config.short_time)
    casjc_mode.Casjc_upload(casjc_config.uppath)
    time.sleep(casjc_config.show_time)
    #获取返回信息
    try:
        WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="uploader-file-status"]')))
        casjc_config.casjc_result[title + time.strftime("%M%S",time.localtime())] = [uname, hailong.find_elements_by_css_selector('div[class="uploader-file-status"]')[0].text]
        time.sleep(casjc_config.show_time)
        aaa.console_logout(uname)
        return None
    except exceptions.TimeoutException:
        casjc_config.casjc_result[title + time.strftime("%M%S",time.localtime())] = [uname, "操作异常"]
        aaa.console_logout(uname)
        return None

#控制台-共享存储-删除文件
def Casjc_console_delfile():
    title = "数据存储-删除文件"
    #登录控制台
    uname = myconfig["entuser2"]
    upasswd = myconfig["entpasswd"]
    uurl = myconfig["consoleUrl"]
    hailong = webdriver.Chrome()
    aaa = casjc_page.Casjc_console_page(hailong,uname,upasswd,uurl)
    #进入控制台
    casjc_log.logging.info(title + " 进入控制台")
    aaa.console()
    #聚焦总览页面菜单产品图标，页面样式已改废弃下面操作
    '''
    impl = hailong.find_element_by_css_selector('i[class="el-icon-caret-bottom"]')
    tmp =  hailong.find_element_by_tag_name('body')
    chain = ActionChains(hailong)
    chain.move_to_element(impl).perform()
    time.sleep(casjc_config.short_time)
    '''
    #点击高性能计算
    casjc_log.logging.info(title + " 点击高性能计算")
    hailong.find_elements_by_css_selector('span[class="innerText"]')[1].click()
    #chain.move_to_element(tmp).perform()
    time.sleep(casjc_config.show_time)
    #点击共享存储菜单
    casjc_log.logging.info(title + " 点击共享存储菜单")
    hailong.find_elements_by_css_selector('b[class="iconfont iconbaocun mr10 fwn"]')[0].click()
    time.sleep(casjc_config.show_time)
    #点击删除按钮
    casjc_log.logging.info(title + " 点击删除按钮")
    hailong.find_elements_by_css_selector('button[class="el-button el-button--text el-button--mini"]')[4].click()
    time.sleep(casjc_config.short_time)
    hailong.find_elements_by_css_selector('button[class="el-button el-button--default el-button--small el-button--primary "]')[0].click()
    time.sleep(casjc_config.show_time)
    #获取返回信息
    try:
        WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="uploader-file-status"]')))
        casjc_config.casjc_result[title + time.strftime("%M%S",time.localtime())] = [uname, hailong.find_elements_by_css_selector('div[class="uploader-file-status"]')[0].text]
        time.sleep(casjc_config.show_time)
        aaa.console_logout(uname)
        return None
    except exceptions.TimeoutException:
        casjc_config.casjc_result[title + time.strftime("%M%S",time.localtime())] = [uname, "操作异常"]
        aaa.console_logout(uname)
        return None


#控制台-高性能计算webshell
def Casjc_console_webshell():
    title = "打开webshell"
    #登录控制台
    uname = myconfig["entuser1"]
    upasswd = myconfig["entpasswd"]
    uurl = myconfig["consoleUrl"]
    hailong = webdriver.Chrome()
    aaa = casjc_page.Casjc_console_page(hailong,uname,upasswd,uurl)
    #进入控制台
    aaa.console()
    casjc_log.logging.info(title + " 进入控制台")
    #点击总览页面的webshell按钮
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'i[class="iconfont iconWebService"]')))
    hailong.find_elements_by_css_selector('i[class="iconfont iconWebService"]')[0].click()
    #点击webshell队列下拉列表
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[0].click()
    time.sleep(casjc_config.show_time)
    #选择队列
    casjc_log.logging.info(title + " 下拉列表选择队列")
    hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')[-1].click()
    #点击确定按钮
    casjc_log.logging.info(title + " 点击选择队列的确定按钮")
    hailong.find_elements_by_css_selector('button[class="el-button el-button--primary el-button--small"]')[-1].click()
    time.sleep(casjc_config.short_time)
    #hailong.quit()
    return None

#控制台-用户管理-新增用户
def Casjc_console_user():
    title = "控制台-用户管理-新增用户"
    #登录控制台
    uname = myconfig["entuser1"]
    upasswd = myconfig["entpasswd"]
    uurl = myconfig["consoleUrl"]
    hailong = webdriver.Chrome()
    aaa = casjc_page.Casjc_console_page(hailong,uname,upasswd,uurl)
    #进入控制台
    casjc_log.logging.info(title + " 进入控制台")
    aaa.console()
    #点击用户管理菜单
    try:
        WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="rightBox"]')))
        time.sleep(casjc_config.short_time)
        casjc_log.logging.info(title + " 点击用户管理菜单")
        hailong.find_element_by_xpath('//div[@class="rightBox"]/div[@class="navInner navTitle"]/span[1]').click()
        time.sleep(casjc_config.short_time)
    except exceptions.TimeoutException:
        casjc_config.casjc_result[title + time.strftime("%M%S",time.localtime())] = [uname, "操作异常"] 
        aaa.console_logout(uname)
        return None
    #点击用户菜单
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'ul[role="menubar"]')))
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 点击用户菜单")
    hailong.find_element_by_xpath('//ul[@role="menubar"]/li[@role="menuitem"][2]').click()
    #点击新增用户
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="handleBoxLeft"]')))
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 点击新增用户")
    hailong.find_element_by_xpath('//div[@class="handleBoxLeft"]/button').click()
    #等待弹出心中窗口
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="dialogWrap"]')))
    time.sleep(casjc_config.short_time)
    #输入用户账号
    account = "uient" + time.strftime("%H%M%S")
    hailong.find_element_by_xpath('//div[@class="el-input el-input--medium"]/input[@type="text"][1]').send_keys(account)
    #输入用户姓名
    aname = "UI自动化企业新增用户"
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[2].send_keys(aname)
    #输入手机号
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[3].send_keys("199" + time.strftime("%m%d%H%M"))
    #输入固定电话
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[4].send_keys("010-88888888")
    #输入邮箱
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[5].send_keys(str(random.randint(10000,99999)) + "@qq.com")
    #点击确定按钮
    casjc_log.logging.info(title + " 点击确定按钮")
    hailong.find_element_by_xpath('//div[@class="dialog-footer"]/button[@class="el-button el-button--primary el-button--small"][1]').click()
    #获取请求结果
    aaa.console_result(title,uname,account)
    return None


#控制台-用户管理-企业普通用户重置密码
def Casjc_console_setpwuser():
    title = "控制台-用户管理-企业普通用户重置密码"
    #登录控制台
    uname = myconfig["entuser1"]
    upasswd = myconfig["entpasswd"]
    uurl = myconfig["consoleUrl"]
    hailong = webdriver.Chrome()
    aaa = casjc_page.Casjc_console_page(hailong,uname,upasswd,uurl)
    #进入控制台
    casjc_log.logging.info(title + " 进入控制台")
    aaa.console()
    #点击用户管理菜单
    try:
        WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="rightBox"]')))
        time.sleep(casjc_config.short_time)
        casjc_log.logging.info(title + " 点击用户管理菜单")
        hailong.find_element_by_xpath('//div[@class="rightBox"]/div[@class="navInner navTitle"]/span[1]').click()
        time.sleep(casjc_config.short_time)
    except exceptions.TimeoutException:
        casjc_config.casjc_result[title + time.strftime("%M%S",time.localtime())] = [uname, "操作异常"] 
        aaa.console_logout(uname)
        return None
    #点击用户菜单
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'ul[role="menubar"]')))
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 点击用户菜单")
    hailong.find_element_by_xpath('//ul[@role="menubar"]/li[@role="menuitem"][2]').click()
    #点击重置密码
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'button[class="el-button el-button--text el-button--mini"]')))
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 点击重置密码")
    hailong.find_elements_by_css_selector('button[class="el-button el-button--text el-button--mini"]')[0].click()
    #等待弹出心中窗口
    time.sleep(casjc_config.short_time)
    #点击确定按钮
    casjc_log.logging.info(title + " 点击确定按钮")
    hailong.find_elements_by_css_selector('button[class="el-button el-button--default el-button--small el-button--primary "]')[0].click()
    #获取请求结果
    aaa.console_result(title,uname)
    return None


#控制台-用户管理-企业普通编辑
def Casjc_console_edituser():
    title = "控制台-用户管理-编辑企业普通用户"
    #登录控制台
    uname = myconfig["entuser1"]
    upasswd = myconfig["entpasswd"]
    uurl = myconfig["consoleUrl"]
    hailong = webdriver.Chrome()
    aaa = casjc_page.Casjc_console_page(hailong,uname,upasswd,uurl)
    #进入控制台
    casjc_log.logging.info(title + " 进入控制台")
    aaa.console()
    #点击用户管理菜单
    try:
        WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="rightBox"]')))
        time.sleep(casjc_config.short_time)
        casjc_log.logging.info(title + " 点击用户管理菜单")
        hailong.find_element_by_xpath('//div[@class="rightBox"]/div[@class="navInner navTitle"]/span[1]').click()
        time.sleep(casjc_config.short_time)
    except exceptions.TimeoutException:
        casjc_config.casjc_result[title + time.strftime("%M%S",time.localtime())] = [uname, "操作异常"] 
        aaa.console_logout(uname)
        return None
    #点击用户菜单
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'ul[role="menubar"]')))
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 点击用户菜单")
    hailong.find_element_by_xpath('//ul[@role="menubar"]/li[@role="menuitem"][2]').click()
    #点击编辑
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'button[class="el-button el-button--text el-button--mini"]')))
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 点击编辑")
    hailong.find_elements_by_css_selector('button[class="el-button el-button--text el-button--mini"]')[1].click()
    #等待弹出编辑用户窗口
    #WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="dialogWrap"]')))
    time.sleep(casjc_config.short_time)
    #输入用户账号
    #account = "uient" + time.strftime("%H%M%S")
    #hailong.find_element_by_xpath('//div[@class="el-input el-input--medium"]/input[@type="text"][1]').send_keys(account)
    #输入用户姓名
    #aname = "UI自动化企业新增用户"
    #hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[2].send_keys(aname)
    #输入手机号
    #hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[3].send_keys("199" + time.strftime("%m%d%H%M"))
    #输入固定电话
    #hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[4].send_keys("010-88888888")
    #输入邮箱
    #hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[5].send_keys(str(random.randint(10000,99999)) + "@qq.com")
    #点击确定按钮
    casjc_log.logging.info(title + " 点击确定按钮")
    hailong.find_elements_by_css_selector('button[class="el-button el-button--primary el-button--small')[2].click()
    #获取请求结果
    aaa.console_result(title,uname)
    return None


#控制台-用户管理-企业普通修改密码
def Casjc_console_updatepwuser():
    title = "控制台-用户管理-企业普通用户修改密码"
    #登录控制台
    uname = myconfig["entuser1"]
    upasswd = myconfig["entpasswd"]
    uurl = myconfig["consoleUrl"]
    hailong = webdriver.Chrome()
    aaa = casjc_page.Casjc_console_page(hailong,uname,upasswd,uurl)
    #进入控制台
    casjc_log.logging.info(title + " 进入控制台")
    aaa.console()
    #点击用户管理菜单
    try:
        WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="rightBox"]')))
        time.sleep(casjc_config.short_time)
        casjc_log.logging.info(title + " 点击用户管理菜单")
        hailong.find_element_by_xpath('//div[@class="rightBox"]/div[@class="navInner navTitle"]/span[1]').click()
        time.sleep(casjc_config.short_time)
    except exceptions.TimeoutException:
        casjc_config.casjc_result[title + time.strftime("%M%S",time.localtime())] = [uname, "操作异常"] 
        aaa.console_logout(uname)
        return None
    #点击用户菜单
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'ul[role="menubar"]')))
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 点击用户菜单")
    hailong.find_element_by_xpath('//ul[@role="menubar"]/li[@role="menuitem"][2]').click()
    #点击修改密码
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'button[class="el-button el-button--text el-button--mini"]')))
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 点击修改密码")
    hailong.find_elements_by_css_selector('button[class="el-button el-button--text el-button--mini"]')[2].click()
    #等待弹出修改密码窗口
    time.sleep(casjc_config.short_time)
    #定义密码
    mima = "123456aA~"
    #输入新密码
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[1].send_keys(mima)
    #输入确认密码
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[2].send_keys(mima)
    #点击确定按钮
    casjc_log.logging.info(title + " 点击确定按钮")
    hailong.find_elements_by_css_selector('button[class="el-button el-button--primary el-button--small')[-1].click()
    #获取请求结果
    aaa.console_result(title,uname,mima)
    return None

#控制台-用户管理-分配高性能计算
def Casjc_console_group():
    title = "控制台-用户管理-新增工作组"
    #登录控制台
    uname = myconfig["entuser1"]
    upasswd = myconfig["entpasswd"]
    uurl = myconfig["consoleUrl"]
    hailong = webdriver.Chrome()
    aaa = casjc_page.Casjc_console_page(hailong,uname,upasswd,uurl)
    #进入控制台
    casjc_log.logging.info(title + " 进入控制台")
    aaa.console()
    #点击用户管理菜单
    try:
        WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="rightBox"]')))
        time.sleep(casjc_config.short_time)
        casjc_log.logging.info(title + " 点击用户管理菜单")
        hailong.find_element_by_xpath('//div[@class="rightBox"]/div[@class="navInner navTitle"]/span[1]').click()
        time.sleep(casjc_config.short_time)
    except exceptions.TimeoutException:
        casjc_log.logging.info(title + "点击用户管理菜单异常")
        casjc_config.casjc_result[title + time.strftime("%M%S",time.localtime())] = [uname, "操作异常"] 
        aaa.console_logout(uname)
        return None
    '''
    #新增工作组功能2.4版本调整，去掉了原有功能
    #点击新增工作组
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="handleBoxLeft"]')))
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 点击新增工作组")
    hailong.find_elements_by_css_selector('button[class="el-button el-button--primary el-button--small"]')[0].click()    
    #等待新建工作组页面
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="create-content"]')))
    time.sleep(casjc_config.short_time)
    #输入项目组
    account = "UI自动化工作组" + time.strftime("%H%M%S")
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[0].send_keys(account)
    #选择成员
    hailong.find_elements_by_css_selector('i[class="iconfont icontianjia"]')[0].click()
    time.sleep(casjc_config.short_time)
    hailong.find_elements_by_xpath('//div[@class="cell"]/label[@class="el-checkbox"]/span[@class="el-checkbox__input"]/span[@class="el-checkbox__inner"]')[0].click()
    #选择队列
    hailong.find_elements_by_css_selector('i[class="iconfont icontianjia"]')[1].click()
    time.sleep(casjc_config.short_time)
    hailong.find_elements_by_xpath('//div[@class="cell"]/label[@class="el-checkbox"]/span[@class="el-checkbox__input"]/span[@class="el-checkbox__inner"]')[0].click()
    '''
    #点击列表第一条数据的分配资源
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 点击分配资源")
    hailong.find_elements_by_css_selector('button[class="el-button el-button--text"]')[4].click()
    #点击确定按钮
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 点击确定按钮")
    hailong.find_elements_by_css_selector('button[class="el-button el-button--primary el-button--small"]')[1].click()
    #获取请求结果
    aaa.console_result(title,uname)
    return None

#控制台-用户管理-云计算分配云主机
def Casjc_console_cloudhost():
    title = "控制台-用户管理-云计算分配云主机"
    #登录控制台
    uname = myconfig["entuser2"]
    upasswd = myconfig["entpasswd"]
    uurl = myconfig["consoleUrl"]
    hailong = webdriver.Chrome()
    aaa = casjc_page.Casjc_console_page(hailong,uname,upasswd,uurl)
    #进入控制台
    casjc_log.logging.info(title + " 进入控制台")
    aaa.console()
    #点击用户管理菜单
    try:
        WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="rightBox"]')))
        time.sleep(casjc_config.short_time)
        casjc_log.logging.info(title + " 点击用户管理菜单")
        hailong.find_element_by_xpath('//div[@class="rightBox"]/div[@class="navInner navTitle"]/span[1]').click()
        time.sleep(casjc_config.short_time)
    except exceptions.TimeoutException:
        casjc_log.logging.info(title + " 点击用户管理菜单异常")
        casjc_config.casjc_result[title + time.strftime("%M%S",time.localtime())] = [uname, "操作异常"] 
        aaa.console_logout(uname)
        return None
    #点击云计算tab
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.ID, 'tab-second')))
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 点击云计算tab")
    hailong.find_element_by_id('tab-three').click()    
    #等待云计算tab页面
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="el-table el-table--fit el-table--enable-row-hover el-table--enable-row-transition"]')))
    time.sleep(casjc_config.short_time)
    #获取用户名称
    account = hailong.find_elements_by_xpath('//tr[@class="el-table__row"][1]/td/div[@class="cell el-tooltip"]')[3].text
    #点击分配云主机,点击列表第一行
    casjc_log.logging.info(title + " 选择用户: %s ，点击分配云主机" %account)
    hailong.find_elements_by_xpath('//tr[@class="el-table__row"][1]/td/div[@class="cell"]/button')[2].click()
    #等待进入分配云主机页面
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="number-content"]')))
    time.sleep(casjc_config.short_time)
    #点击确定按钮
    hailong.find_elements_by_css_selector('button[class="el-button el-button--primary el-button--small"]')[-1].click()
    #获取请求结果
    aaa.console_result(title,uname,account)
    return None
    

#控制台-用户管理-云硬盘分配云硬盘
def Casjc_console_volume():
    title = "控制台-用户管理-云硬盘分配云硬盘"
    #登录控制台
    uname = myconfig["entuser2"]
    upasswd = myconfig["entpasswd"]
    uurl = myconfig["consoleUrl"]
    hailong = webdriver.Chrome()
    aaa = casjc_page.Casjc_console_page(hailong,uname,upasswd,uurl)
    #进入控制台
    casjc_log.logging.info(title + " 进入控制台")
    aaa.console()
    #点击用户管理菜单
    try:
        WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="rightBox"]')))
        time.sleep(casjc_config.short_time)
        casjc_log.logging.info(title + " 点击用户管理菜单")
        hailong.find_element_by_xpath('//div[@class="rightBox"]/div[@class="navInner navTitle"]/span[1]').click()
        time.sleep(casjc_config.short_time)
    except exceptions.TimeoutException:
        casjc_log.logging.info(title + " 点击用户管理菜单异常")
        casjc_config.casjc_result[title + time.strftime("%M%S",time.localtime())] = [uname, "操作异常"] 
        aaa.console_logout(uname)
        return None
    #点击云硬盘tab
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.ID, 'tab-second')))
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 点击云硬盘tab")
    hailong.find_element_by_id('tab-four').click()    
    #等待云硬盘tab页面
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="el-table el-table--fit el-table--enable-row-hover el-table--enable-row-transition"]')))
    time.sleep(casjc_config.short_time)
    #获取用户名称
    account = hailong.find_elements_by_xpath('//tr[@class="el-table__row"][1]/td/div[@class="cell el-tooltip"]')[3].text
    #点击分配云硬盘,点击列表第一行
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '//tr[@class="el-table__row"][1]/td/div[@class="cell"]/button')))
    time.sleep(casjc_config.show_time)
    casjc_log.logging.info(title + " 选择用户：{0}，点击分配云硬盘".format(account))
    hailong.find_elements_by_xpath('//tr[@class="el-table__row"][1]/td/div[@class="cell"]/button')[0].click()
    #等待进入分配云硬盘页面
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="number-content"]')))
    time.sleep(casjc_config.short_time)
    #点击确定按钮
    hailong.find_elements_by_css_selector('button[class="el-button el-button--primary el-button--small"]')[-1].click()
    #获取请求结果
    aaa.console_result(title,uname,account)
    return None


#控制台-用户管理-文件存储调整配额
def Casjc_console_quota():
    title = "控制台-用户管理-文件存储调整配额"
    #登录控制台
    uname = myconfig["entuser2"]
    upasswd = myconfig["entpasswd"]
    uurl = myconfig["consoleUrl"]
    hailong = webdriver.Chrome()
    aaa = casjc_page.Casjc_console_page(hailong,uname,upasswd,uurl)
    #进入控制台
    casjc_log.logging.info(title + " 进入控制台")
    aaa.console()
    #点击用户管理菜单
    try:
        WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="rightBox"]')))
        time.sleep(casjc_config.short_time)
        casjc_log.logging.info(title + " 点击用户管理菜单")
        hailong.find_element_by_xpath('//div[@class="rightBox"]/div[@class="navInner navTitle"]/span[1]').click()
        time.sleep(casjc_config.short_time)
    except exceptions.TimeoutException:
        casjc_log.logging.info(title + " 点击用户管理菜单异常")
        casjc_config.casjc_result[title + time.strftime("%M%S",time.localtime())] = [uname, "操作异常"] 
        aaa.console_logout(uname)
        return None
    #点击文件存储tab
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.ID, 'tab-second')))
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 点击文件存储tab")
    hailong.find_element_by_id('tab-second').click()    
    #等待文件存储tab页面
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="el-table el-table--fit el-table--enable-row-hover el-table--enable-row-transition"]')))
    time.sleep(casjc_config.short_time)
    #获取用户名称
    account = hailong.find_elements_by_xpath('//tr[@class="el-table__row"]/td/div[@class="cell el-tooltip"]')[-5].text
    #点击调整配额
    if hailong.find_elements_by_css_selector('button[class="el-button el-button--text"]')[-3].text == "调整配额":
        casjc_log.logging.info(title + " 点击调整配额")
        hailong.find_elements_by_css_selector('button[class="el-button el-button--text"]')[-3].click()
    else:
        casjc_log.logging.info(title + " 点击调整配额")
        hailong.find_elements_by_css_selector('button[class="el-button el-button--text"]')[-4].click()
    #输入配额
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="el-dialog__body"]')))
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[4].send_keys(casjc_config.quota_number)
    time.sleep(casjc_config.show_time)
    #点击确定按钮
    casjc_log.logging.info(title + " 点击确定按钮")
    while True:
        if len(hailong.find_elements_by_css_selector('button[class="el-button el-button--primary el-button--small"]')) == 3:
            break
        print(len(hailong.find_elements_by_css_selector('button[class="el-button el-button--primary el-button--small"]')))
    hailong.find_elements_by_css_selector('button[class="el-button el-button--primary el-button--small"]')[-2].click()
    #获取请求结果
    aaa.console_result(title,uname,account)
    return None

#控制台-用户管理-文件存储权限设置
def Casjc_console_auth():
    title = "控制台-用户管理-云存储权限设置"
    #登录控制台
    uname = myconfig["entuser2"]
    upasswd = myconfig["entpasswd"]
    uurl = myconfig["consoleUrl"]
    hailong = webdriver.Chrome()
    aaa = casjc_page.Casjc_console_page(hailong,uname,upasswd,uurl)
    #进入控制台
    casjc_log.logging.info(title + " 进入控制台")
    aaa.console()
    #点击用户管理菜单
    try:
        WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="rightBox"]')))
        time.sleep(casjc_config.short_time)
        casjc_log.logging.info(title + " 点击用户管理菜单")
        hailong.find_element_by_xpath('//div[@class="rightBox"]/div[@class="navInner navTitle"]/span[1]').click()
        time.sleep(casjc_config.short_time)
    except exceptions.TimeoutException:
        casjc_log.logging.info(title + " 点击用户管理菜单异常")
        casjc_config.casjc_result[title + time.strftime("%M%S",time.localtime())] = [uname, "操作异常"] 
        aaa.console_logout(uname)
        return None
    #点击文件存储tab
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.ID, 'tab-second')))
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 点击文件存储tab")
    hailong.find_element_by_id('tab-second').click()    
    #等待文件存储tab页面
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="el-table el-table--fit el-table--enable-row-hover el-table--enable-row-transition"]')))
    time.sleep(casjc_config.short_time)
    #点击权限设置
    if hailong.find_elements_by_css_selector('button[class="el-button el-button--text"]')[-3].text == "权限设置":
        hailong.find_elements_by_css_selector('button[class="el-button el-button--text"]')[-3].click()
        #获取用户名称
        account = hailong.find_elements_by_xpath('//tr[@class="el-table__row"]/td/div[@class="cell el-tooltip"]')[-5].text
    elif hailong.find_elements_by_css_selector('button[class="el-button el-button--text"]')[-5].text == "权限设置":
        hailong.find_elements_by_css_selector('button[class="el-button el-button--text"]')[-5].click()
        #获取用户名称
        account = hailong.find_elements_by_xpath('//tr[@class="el-table__row"]/td/div[@class="cell el-tooltip"]')[-10].text
    else:
        casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, "最后两个用户没有权限设置按钮"] 
        aaa.console_logout(uname)
        return None
    #勾选组成员权限
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="el-dialog__body"]')))
    time.sleep(casjc_config.show_time)
    boxs = len(hailong.find_elements_by_css_selector('label[class="el-checkbox"]'))
    print(boxs)
    for i in range(boxs):
        time.sleep(casjc_config.short_time)
        hailong.find_elements_by_css_selector('label[class="el-checkbox"]')[0].click()
    #点击确定按钮
    casjc_log.logging.info(title + " 点击确定按钮")
    hailong.find_elements_by_css_selector('button[class="el-button el-button--primary el-button--small"]')[-1].click()
    #获取请求结果
    aaa.console_result(title,uname,account)
    return None

#控制台-个人中心-修改密码
def Casjc_console_updatepw():
    title = "控制台-个人中心-修改密码"
    #登录控制台
    uname = myconfig["entuser1"]
    upasswd = myconfig["entpasswd"]
    uurl = myconfig["consoleUrl"]
    hailong = webdriver.Chrome()
    aaa = casjc_page.Casjc_console_page(hailong,uname,upasswd,uurl)
    #进入控制台
    casjc_log.logging.info(title + " 进入控制台")
    aaa.console()
    #点击用户头像进入个人中心
    try:
        WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="userinfo el-popover__reference"]')))
        time.sleep(casjc_config.short_time)
        casjc_log.logging.info(title + " 点击用户头像进入个人中心")
        hailong.find_element_by_css_selector('div[class="userinfo el-popover__reference"]').click()
        time.sleep(casjc_config.short_time)
    except exceptions.TimeoutException:
        casjc_log.logging.info(title + " 点击用户头像进入个人中心异常")
        casjc_config.casjc_result[title + time.strftime("%M%S",time.localtime())] = [uname, "操作异常"] 
        aaa.console_logout(uname)
        return None
    #点击安全设置菜单
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'li[class="el-menu-item"]')))
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 点击安全设置菜单")
    hailong.find_elements_by_css_selector('li[class="el-menu-item"]')[0].click()
    #点击账号密码的修改按钮
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'button[class="el-button p el-button--text"]')))
    casjc_log.logging.info(title + " 点击账号密码的修改按钮")
    hailong.find_elements_by_css_selector('button[class="el-button p el-button--text"]')[0].click()
    #输入旧密码
    oldpw = "123456aA~1"
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'input[class="el-input__inner"]')))
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[0].send_keys(upasswd)
    #输入新密码
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[1].send_keys(oldpw)
    #输入确认密码
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[2].send_keys(oldpw)
    #点击确定按钮
    casjc_log.logging.info(title + " 点击确定按钮")
    hailong.find_element_by_css_selector('button[class="el-button el-button--primary"]').click()
    #获取请求结果
    try:
        casjc_log.logging.info(title + " 修改完密码后等待页面元素是否进入登录页")
        WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'a[href="/login"]')))
        casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, "修改密码操作成功,当前密码: " + oldpw]
    except exceptions.TimeoutException:
        casjc_log.logging.info(title + " 获取修改密码请求返回结果异常")
        casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, " 修改密码操作异常"]
        return None
    time.sleep(casjc_config.show_time)
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'a[href="/login"]')))
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 点击登录")
    hailong.find_elements_by_css_selector('a[href="/login"]')[0].click()
    time.sleep(casjc_config.show_time)
    hailong.find_element_by_css_selector("input[type='text']").send_keys(uname)
    hailong.find_element_by_css_selector('input[type="password"]').send_keys(oldpw)
    hailong.find_element_by_tag_name('button').click()
    #等待casjc_config.wait_time全局设置时间，判断是否登录成功进入首页
    try:
        casjc_log.logging.info(title + " 登录后等待页面元素,判断是否登录成功")
        WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="console"]')))
        if hailong.find_elements_by_css_selector('div[class="console"]')[0].text == "控制台":
            time.sleep(casjc_config.show_time)
            #casjc_config.casjc_result['控制台用户登录'+ time.strftime("%M%S",time.localtime())] = [uname, "登录成功"]
        else:
            asjc_log.logging.info(title + " 登录后页面没有找到页面元素关键字<控制台>")
            casjc_config.casjc_result['控制台用户登录'+ time.strftime("%M%S",time.localtime())] = [uname, "登录失败,测试终止"]
            return None
    except exceptions.TimeoutException:
        casjc_log.logging.info(title + " 登录后没有找到页面元素,可能登录失败")
        casjc_config.casjc_result['控制台用户登录'+ time.strftime("%M%S",time.localtime())] = [uname, "登录失败,测试终止"]
        return None
    #进入控制台
    casjc_log.logging.info(title + " 进入控制台")
    aaa.console()
    #点击用户头像进入个人中心
    try:
        WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="userinfo el-popover__reference"]')))
        time.sleep(casjc_config.short_time)
        casjc_log.logging.info(title + " 点击用户头像进入个人中心")
        hailong.find_element_by_css_selector('div[class="userinfo el-popover__reference"]').click()
        time.sleep(casjc_config.short_time)
    except exceptions.TimeoutException:
        casjc_log.logging.info(title + " 点击用户头像进入个人中心异常")
        casjc_config.casjc_result[title + time.strftime("%M%S",time.localtime())] = [uname, "操作异常"] 
        aaa.console_logout(uname)
        return None
    #点击安全设置菜单
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'li[class="el-menu-item"]')))
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 点击安全设置菜单")
    hailong.find_elements_by_css_selector('li[class="el-menu-item"]')[0].click()
    #点击账号密码的修改按钮
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'button[class="el-button p el-button--text"]')))
    casjc_log.logging.info(title + " 点击账号密码的修改按钮")
    hailong.find_elements_by_css_selector('button[class="el-button p el-button--text"]')[0].click()
    #输入旧密码
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'input[class="el-input__inner"]')))
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[0].send_keys(oldpw)
    #输入新密码
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[1].send_keys(upasswd)
    #输入确认密码
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[2].send_keys(upasswd)
    #点击确定按钮
    casjc_log.logging.info(title + " 点击确定按钮")
    hailong.find_element_by_css_selector('button[class="el-button el-button--primary"]').click()
    #获取请求结果
    try:
        WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'a[href="/login"]')))
        casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, "修改密码操作成功,当前密码: " + upasswd ]
        hailong.quit()
        return None
    except exceptions.TimeoutException:
        casjc_log.logging.info(title + " 修改密码后没有跳转至登录页，修改密码操作异常")
        casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, " 修改密码操作异常"]
        hailong.quit()
        return None


#控制台-个人中心-修改基本信息
def Casjc_console_info():
    title = "控制台-个人中心-修改基本信息"
    #登录控制台
    uname = myconfig["entuser2"]
    upasswd = myconfig["entpasswd"]
    uurl = myconfig["consoleUrl"]
    hailong = webdriver.Chrome()
    aaa = casjc_page.Casjc_console_page(hailong,uname,upasswd,uurl)
    #进入控制台
    casjc_log.logging.info(title + " 进入控制台")
    aaa.console()
    #点击用户头像进入个人中心
    try:
        WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="userinfo el-popover__reference"]')))
        time.sleep(casjc_config.short_time)
        casjc_log.logging.info(title + " 点击用户头像进入个人中心")
        hailong.find_element_by_css_selector('div[class="userinfo el-popover__reference"]').click()
        time.sleep(casjc_config.short_time)
    except exceptions.TimeoutException:
        casjc_log.logging.info(title + " 点击用户头像进入个人中心异常")
        casjc_config.casjc_result[title + time.strftime("%M%S",time.localtime())] = [uname, "操作异常"] 
        aaa.console_logout(uname)
        return None
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="change text"]')))
    time.sleep(casjc_config.short_time)
    #点击修改姓名,输入姓名后保存
    casjc_log.logging.info(title + " 修改姓名")
    aname = "健次郎" + time.strftime("%M%S")
    hailong.find_element_by_xpath('//div[@class="changeBox"]/div[@class="change text"][1]/span').click()
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'input[class="el-input__inner"]')))
    hailong.find_element_by_css_selector('input[class="el-input__inner"]').send_keys(aname)
    hailong.find_elements_by_css_selector('button[class="el-button el-button--text"]')[6].click()
    time.sleep(casjc_config.short_time)
    #点击修改(研究方向),输入研究方向
    casjc_log.logging.info(title + " 修改研究方向")
    inter = "心理学"  + time.strftime("%M%S")
    hailong.find_element_by_xpath('//div[@class="changeBox"]/div[@class="change text"][2]/span').click()
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'input[class="el-input__inner"]')))
    hailong.find_element_by_css_selector('input[class="el-input__inner"]').send_keys(inter)
    hailong.find_elements_by_css_selector('button[class="el-button el-button--text"]')[6].click()
    time.sleep(casjc_config.short_time)
    #点击修改联系电话,输入联系电话
    casjc_log.logging.info(title + " 修改联系电话")
    telephone = "8844"  + time.strftime("%M%S")
    hailong.find_elements_by_xpath('//div[@class="changeBox"]/div[@class="change text"]/span')[3].click()
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'input[class="el-input__inner"]')))
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[0].send_keys("0454")
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[1].send_keys(telephone)
    hailong.find_elements_by_css_selector('button[class="el-button el-button--text"]')[6].click()
    time.sleep(casjc_config.short_time)
    #点击修改地址,输入联系地址
    casjc_log.logging.info(title + " 修改联系地址")
    address = "河北大街"  + time.strftime("%M%S")
    hailong.find_elements_by_xpath('//div[@class="changeBox"]/div[@class="change text"]/span')[5].click()
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'input[class="el-input__inner"]')))
    hailong.find_element_by_css_selector('input[class="el-input__inner"]').send_keys(address)
    hailong.find_elements_by_css_selector('button[class="el-button el-button--text"]')[6].click()
    resstr = ""
    time.sleep(casjc_config.short_time)
    print(hailong.find_elements_by_xpath('//div[@class="details"]/div/div/span[2]')[2].text)
    if aname == hailong.find_elements_by_xpath('//div[@class="details"]/div/div/span[2]')[0].text:
        resstr += " 姓名修改成功,修改为: " + aname
    else:
        resstr += " 姓名修改失败;"
    if inter == hailong.find_elements_by_xpath('//div[@class="details"]/div/div/span[2]')[1].text:
        resstr += " 研究方向修改成功,修改为: " + inter
    else:
        resstr += " 研究方向修改失败"
    if "0454-" + telephone == hailong.find_elements_by_xpath('//div[@class="details"]/div/div/span[2]')[2].text:
        resstr += " 联系电话修改成功,修改为: " + "0454-" + telephone
    else:
        resstr += " 联系电话修改失败"
    if address == hailong.find_elements_by_xpath('//div[@class="details"]/div/div/span[2]')[3].text:
        resstr += " 联系地址修改成功,修改为: " + address
    else:
        resstr += " 联系地址修改失败"
    casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, resstr]
    aaa.console_logout(uname)
    return None

#控制台-个人中心-企业管理员申请试用
def Casjc_console_try(env=""):
    title = "控制台-个人中心-注册新企业管理员申请试用"
    hailong = webdriver.Chrome()
    uurl = myconfig['consoleUrl']
    #注册企业管理员
    casjc_log.logging.info(title + " 注册新的企业管理员")
    muser = ui_www.Casjc_www_mail_regist(uurl)
    if not muser:
        casjc_log.logging.info(title + " 注册新的企业管理员失败")
        casjc_config.casjc_result[title + time.strftime("%M%S",time.localtime())] = ["", "注册企业管理员失败"] 
        return None        
    #登录控制台
    uname = muser
    upasswd = myconfig['entpasswd']
    uurl = myconfig['consoleUrl']
    casjc_log.logging.info(title + " 登录官网")
    aaa = casjc_page.Casjc_console_page(hailong,uname,upasswd,uurl)
    try:
        #点击申请试用按钮
        WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="c-hero-aside-btn"]')))
        time.sleep(casjc_config.short_time)
        casjc_log.logging.info(title + " 登录后点击申请试用按钮")
        hailong.find_element_by_css_selector('div[class="c-hero-aside-btn"]').click()
    except exceptions.TimeoutException:
        #没有找到申请试用按钮终止程序
        casjc_log.logging.info(title + " 登录后点击申请试用按钮失败")
        casjc_config.casjc_result[title + time.strftime("%M%S",time.localtime())] = [uname, "没有找到申请试用按钮"] 
        hailong.quit()
        return None
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'form[class="el-form trial-form"]')))
    #输入用户单位
    casjc_log.logging.info(title + " 输入用户单位")
    cmp = "联合国发展集团(申请试用)" + time.strftime("%M%S")
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[2].send_keys(cmp)
    #输入项目名称
    casjc_log.logging.info(title + " 输入项目名称")
    pro = "这个时代太不浪漫，深情的人都被称为舔狗。" + time.strftime("%M%S")#"量子计算机算力计算" + time.strftime("%M%S")
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[3].send_keys(pro)
    #输入手机号
    casjc_log.logging.info(title + " 输入手机号")
    pho = "13141032576"
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[5].send_keys(pho)
    #输入备注
    casjc_log.logging.info(title + " 输入备注")
    con = "曙光信息产业股份有限公司（以下简称“中科曙光”）是中国信息产业领军企业，为中国及全球用户提供创新、高效、可靠的IT产品、解决方案及服务。"
    hailong.find_element_by_css_selector('textarea[class="el-textarea__inner"]').send_keys(con)
    #点击提交申请
    casjc_log.logging.info(title + " 点击提交申请按钮")
    hailong.find_element_by_css_selector('button[class="el-button el-button--primary').click()
    try:
        WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="trial-title"]')))
        if hailong.find_element_by_css_selector('div[class="trial-title"]').text == "提交成功":
            #登录，点击资源管理菜单
            uname2 = myconfig2['user3']
            upasswd = myconfig2['passwd2']
            uurl = myconfig2['adminUrl']
            casjc_log.logging.info(title + " 销售总监登录管理后台")
            bbb = casjc_page.Casjc_admin_page(hailong,uname2,upasswd,uurl)
            bbb.admin_resmanagement()
            if hailong.find_element_by_xpath('//tr[@class="el-table__row"][1]/td[4]/div[@class="cell"]').text == cmp:
                casjc_log.logging.info(title + " 管理后台找到刚刚提交的试用申请")
                casjc_config.casjc_result[title + time.strftime("%M%S",time.localtime())] = [uname, "项目名称:" + pro + " 提交申请试用成功"]
                bbb.Casjc_logout(uname2)
                return None
            else:
                casjc_log.logging.info(title + " 管理后台没有找到刚刚提交的试用申请,操作异常")
                casjc_config.casjc_result[title + time.strftime("%M%S",time.localtime())] = [uname, "申请试用异常,销售总监没有看到该条申请"]
                hailong.quit()
                return None                
        else:
            casjc_log.logging.info(title + " 提交试用申请异常")
            casjc_config.casjc_result[title + time.strftime("%M%S",time.localtime())] = [uname, "申请试用异常"]
            hailong.quit()
            return None
    except exceptions.TimeoutException:
        casjc_log.logging.info(title + " 提交试用申请异常")
        casjc_config.casjc_result[title + time.strftime("%M%S",time.localtime())] = [uname, "申请试用异常"] 
        hailong.quit()
        return None

#控制台-工单-提交工单
def Casjc_console_order():
    title = "控制台-工单-提交工单"
    #登录控制台
    uname = myconfig["entuser1"]
    upasswd = myconfig["entpasswd"]
    uurl = myconfig["consoleUrl"]
    hailong = webdriver.Chrome()
    aaa = casjc_page.Casjc_console_page(hailong,uname,upasswd,uurl)
    #进入控制台
    casjc_log.logging.info(title + " 进入控制台")
    aaa.console()
    #点击用户管理菜单
    try:
        WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="rightBox"]')))
        time.sleep(casjc_config.short_time)
        casjc_log.logging.info(title + " 点击用户管理菜单")
        hailong.find_element_by_xpath('//div[@class="rightBox"]/div[@class="navInner navTitle"]/span[3]').click()
        time.sleep(casjc_config.short_time)
    except exceptions.TimeoutException:
        casjc_log.logging.info(title + " 点击用户管理菜单异常")
        casjc_config.casjc_result[title + time.strftime("%M%S",time.localtime())] = [uname, "操作异常"] 
        aaa.console_logout(uname)
        return None
    #等待页面元素,确认是否进入我的工单页面
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="btnLeft"]')))
    time.sleep(casjc_config.short_time)
    #点击提交工单
    casjc_log.logging.info(title + " 点击提交工单按钮")
    hailong.find_element_by_css_selector('div[class="btnLeft"]').click()
    time.sleep(casjc_config.short_time)
    #等待页面元素,确认是否进入提交工单页面
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'p[class="btnBox"]')))
    time.sleep(casjc_config.short_time)
    #点击高性能计算提问按钮
    casjc_log.logging.info(title + " 点击高性能计算提问按钮")
    hailong.find_elements_by_css_selector('p[class="btnBox"]')[0].click()
    time.sleep(casjc_config.short_time)
    #等待页面元素，创建工单
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="createOrder"]')))
    time.sleep(casjc_config.short_time)
    #点击高性能计算提问按钮
    casjc_log.logging.info(title + " 点击高性能计算提问按钮")
    hailong.find_element_by_css_selector('div[class="createOrder"]').click()
    time.sleep(casjc_config.short_time)
    #等待页面元素
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="formWrap"]')))
    time.sleep(casjc_config.short_time)
    #输入问题描述
    casjc_log.logging.info(title + " 输入问题描述")
    hailong.find_element_by_css_selector('textarea[class="el-textarea__inner"]').send_keys("hello")
    #输入联系电话
    casjc_log.logging.info(title + " 输入联系电话")
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[0].send_keys("13112341234")
    #点击上传附件按钮
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="blurButton"]')))
    casjc_log.logging.info(title + " 点击上传附件按钮")
    hailong.find_element_by_css_selector('div[class="blurButton"]').click()
    time.sleep(casjc_config.show_time)
    #选择本地文件上传
    casjc_mode.Casjc_upload(casjc_config.uppath)
    time.sleep(casjc_config.show_time)
    #点击提交按钮
    casjc_log.logging.info(title + " 点击提交工单按钮")
    hailong.find_element_by_css_selector('button[class="el-button el-button--primary"]').click()
    aaa.console_result(title,uname)
    return None


if __name__ == "__main__":
    try:
        if sys.argv[1] == "dev":
            myconfig = casjc_config.devPerson['console']
            myconfig2 = casjc_config.devPerson['admin']
            env = "dev"
        else:
            myconfig = casjc_config.testPerson['console']
            myconfig2 = casjc_config.testPerson['admin']
            env = "test"
    except IndexError:
        myconfig = casjc_config.testPerson['console']
        myconfig2 = casjc_config.testPerson['admin']
        env = "test"
    casjc_log.logging.info(">" * 15 + " UI自动化脚本开始执行执行 " + "<" * 15)
    start_time = time.strftime("%m-%d %H:%M:%S",time.localtime())

    #Casjc_console_group()
    
    for i in range(1):
        Casjc_console_user()
        Casjc_console_group()
        
    Casjc_console_setpwuser()
    Casjc_console_edituser()
    Casjc_console_updatepwuser()
    Casjc_console_upfile()
    Casjc_console_delfile()
    #Casjc_console_webshell()    
    #Casjc_console_user()  
    #Casjc_console_group()
    #Casjc_console_volume()
    Casjc_console_cloudhost()
    Casjc_console_quota()
    Casjc_console_auth()
    Casjc_console_updatepw()
    Casjc_console_info()
    Casjc_console_try(env)
    Casjc_console_order()
    Casjc_console_try()
    
    end_time = time.strftime("%m-%d %H:%M:%S",time.localtime())
    print ("开始时间： " + start_time)
    print ("结束时间： " + end_time)
    print (json.dumps(casjc_config.casjc_result,ensure_ascii=False))
    casjc_mode.Run_result(("console",start_time,end_time,json.dumps(casjc_config.casjc_result,ensure_ascii=False),env))
    casjc_log.logging.info( ">" * 15 + " 模块名: console, 本次UI自动化脚本执行完成，通过页面模块筛选查看执行结果 " + "<" * 15)
