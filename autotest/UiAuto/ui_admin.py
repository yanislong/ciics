import time, sys, json, random
import requests

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import *
from selenium.common import exceptions
from selenium.webdriver.support.wait import WebDriverWait  
from selenium.webdriver.support import expected_conditions as EC  
from selenium.webdriver.common.by import By

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


#get直接返回，不再等待界面加载完成
desired_capabilities = DesiredCapabilities.CHROME
desired_capabilities["pageLoadStrategy"] = "none"

#driver = webdriver.Chrome(executable_path='chromedriver.exe')

import casjc_config
import casjc_mode
import casjc_page
import casjc_log
 

#申请资源
def Casjc_res(*appcon):
    """
    0 固定方式
    1 灵活方式
    "gb" 高性能计算-标准型
    "gg" 高性能计算-共享型
    "yy" 云计算-云主机
    "sw" 数据存储-文件存储
    "sy" 数据存储-云硬盘
    "wg" 网络资源-公网IP
    
    申请资源返回值为一个订单号和一个元组包含：是否试用，资源类型，示例('20201026172520256', (0, 'gg'))
    """
    title = "申请资源"
    if not appcon:
        casjc_log.logging.info(title + " 没有传递appcon参数,终止执行")
        casjc_config.casjc_result[title + time.strftime("%M%S")] = ["", "没有传递appcon参数,终止执行"]
        return None    
    if appcon[0][0] == 0:
        if appcon[0][1] == "gb":
            title = "申请资源-固定方式-高性能计算-标准型"
        if appcon[0][1] == "gg":
            title = "申请资源-固定方式-高性能计算-共享型"
        if appcon[0][1] == "yy":
            title = "申请资源-固定方式-云计算-云主机"
        if appcon[0][1] == "sw":
            title = "申请资源-固定方式-数据存储-文件存储"
        if appcon[0][1] == "sy":
            title = "申请资源-固定方式-数据存储-云硬盘"
        if appcon[0][1] == "wg":
            title = "申请资源-固定方式-网络资源-公网IP"
    elif appcon[0][0] == 1:
        if appcon[0][1] == "gb":
            title = "申请资源-灵活方式-高性能计算-标准型"
        if appcon[0][1] == "gg":
            title = "申请资源-灵活方式-高性能计算-共享型"
        if appcon[0][1] == "yy":
            title = "申请资源-灵活方式-云计算-云主机"
        if appcon[0][1] == "sw":
            title = "申请资源-灵活方式-数据存储-文件存储"
        if appcon[0][1] == "sy":
            title = "申请资源-灵活方式-数据存储-云硬盘"
        if appcon[0][1] == "wg":
            title = "申请资源-灵活方式-网络资源-公网IP"
    casjc_log.logging.info(title)
    #登录，点击资源管理菜单
    uname = myconfig['user2']
    upasswd = myconfig['passwd2']
    uurl = myconfig['adminUrl']
    hailong = webdriver.Chrome()
    aaa = casjc_page.Casjc_admin_page(hailong,uname,upasswd,uurl)
    casjc_log.logging.info(title + " 进入资源管理菜单")
    aaa.admin_resmanagement()
    #点击申请资源按钮
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="el-row"]')))
    if appcon[0][0] == 0:
        casjc_log.logging.info(title + " 点击申请试用资源按钮")
        hailong.find_elements_by_tag_name('button')[1].click()
    elif appcon[0][0] == 1:
        casjc_log.logging.info(title + " 点击申请资源按钮")
        hailong.find_elements_by_tag_name('button')[0].click()
    time.sleep(casjc_config.show_time)
    #重新加载当前页面
    #hailong.refresh()
    if hailong.find_elements_by_css_selector('div[class="step-item"]')[1].text == "提交资源申请":
        casjc_log.logging.info(title + " 进入资源申请界面成功")
    else:
        casjc_log.logging.info(title + " 进入资源申请界面失败")
    #选择用户单位,选择最后一个
    casjc_log.logging.info(title + " 点击选择用户单位列表")
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[0].click()
    time.sleep(casjc_config.short_time)
    #Select(hailong.find_elements_by_css_selector('li[class="el-scrollbar__view el-select-dropdown__list""]')).select_by_value('国科北京分部')
    casjc_log.logging.info(title + " 选择单位列表中最后一个元素")
    hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')[-1].click()
    #hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')[-8].click()
    #获取选择的企业单位名称
    ent = hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')[-1].text
    #输入项目名称
    casjc_log.logging.info(title + " 输入项目名称")
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[1].send_keys('王氏集团董事千金的项目')
    #选择甲方用户
    casjc_log.logging.info(title + " 选择甲方用户")
    #指定甲方用户,没有就点击，有就搜索
    suser = ""
    if not suser:
        hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[2].click()
    else:
        hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[2].send_keys(suser)
    time.sleep(casjc_config.short_time)
    try:
        time.sleep(casjc_config.show_time)
        if hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')[-1].text == "":
            jiafang = hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')[-2].text
            hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')[-2].click()
        else:
            jiafang = hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')[-1].text
            hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')[-1].click()
    except exceptions.ElementNotInteractableException:
        casjc_log.logging.info(title + " %s企业没有找到账号"%ent)
        casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, "当前企业没有找到账号"]
        aaa.Casjc_logout()
        return None
    #输入手机号
    casjc_log.logging.info(title + " 清空当前内容,输入手机号")
    time.sleep(casjc_config.short_time)
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[3].clear()
    time.sleep(casjc_config.short_time)
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[3].send_keys('13112341234')
    #输入邮箱
    casjc_log.logging.info(title + " 清空当前内容,输入邮箱")
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[4].clear()
    time.sleep(casjc_config.short_time)
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[4].send_keys('335916781@qq.com')
    #点击配置方式下拉框
    #hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[5].click()
    #time.sleep(casjc_config.short_time)
    #li标签列表数据长度,最后一个是灵活配置
    #listelement = hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')
    #判断配置方式，如果appcon[0][0]是0固定方式，如果是1灵活方式
    if appcon[0][0] == 0:
        casjc_log.logging.info(title + " 选择配置方式，固定配置")
        #hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')[len(listelement)-2].click()
        #填写基本信息完成，提交下一步
        hailong.find_elements_by_tag_name('button')[1].click()
        time.sleep(casjc_config.short_time)
        #进入提交资源申请页面
        WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="tableBox"]')))
        if appcon[0][1] == "gb":
            n = 1
        elif appcon[0][1] == "gg":
            n = 2
        elif appcon[0][1] == "yy":
            n = 3
        elif appcon[0][1] == "sw":
            n = 4
        elif appcon[0][1] == "sy":
            n = 5
        elif appcon[0][1] == "wg":
            n = 6
        #输出当前执行资源类型
        casjc_log.logging.info(title + " 当前操作的资源类型：" + hailong.find_elements_by_xpath('//div[@class="boxOne"]/div[@class="title"]')[n-1].text.split("\n")[0])
        #点击当前资源图标，展开规格
        casjc_log.logging.info(title + " 点击资源图标，展开规格")
        resicon = hailong.find_element_by_xpath('//div[@class="boxOne"][' + str(n) + ']/div/div[@class="el-table el-table--fit el-table--enable-row-hover el-table--enable-row-transition"]/div[@class="el-table__body-wrapper is-scrolling-none"]/table/tbody/tr/td/div[@class="cell"]/div[@class="el-table__expand-icon"]')
        resicon.click()
        #获取规格数据（暂存）
        reslistnum = hailong.find_elements_by_xpath('//div[@class="boxOne"][' + str(n) + ']/div/div[@class="el-table el-table--fit el-table--enable-row-hover el-table--enable-row-transition"]/div[@class="el-table__body-wrapper is-scrolling-none"]/table/tbody/tr[@class="el-table__row el-table__row--level-1"]')
        if appcon[0][1] == "gg":
            #输入数量
            num1 = "1"
            casjc_log.logging.info(title + " 输入资源数量")
            #print(hailong.find_element_by_xpath('//div[@class="boxOne"][' + str(n) + ']/div[1]').text)
            hailong.find_element_by_xpath('//div[@class="boxOne"][' + str(n) + ']/div/div[@class="el-table el-table--fit el-table--enable-row-hover el-table--enable-row-transition"]/div[@class="el-table__body-wrapper is-scrolling-none"]/table/tbody/tr[@class="el-table__row el-table__row--level-1"]/td[5]/div/div/input').send_keys(num1)
            #输入有效期天数 
            num2 = "10"
            casjc_log.logging.info(title + " 输入资源有效期")
            hailong.find_element_by_xpath('//div[@class="boxOne"][' + str(n) + ']/div/div[@class="el-table el-table--fit el-table--enable-row-hover el-table--enable-row-transition"]/div[@class="el-table__body-wrapper is-scrolling-none"]/table/tbody/tr[@class="el-table__row el-table__row--level-1"]/td[6]/div/div/input').send_keys(num2)
        else:
            
            #输入数量
            num1 = "1"
            casjc_log.logging.info(title + " 输入资源数量")
            #print(hailong.find_element_by_xpath('//div[@class="boxOne"][' + str(n) + ']/div[1]').text)
            hailong.find_element_by_xpath('//div[@class="boxOne"][' + str(n) + ']/div/div[@class="el-table el-table--fit el-table--enable-row-hover el-table--enable-row-transition"]/div[@class="el-table__body-wrapper is-scrolling-none"]/table/tbody/tr[@class="el-table__row el-table__row--level-1"]/td[4]/div/div/input').send_keys(num1)
            #输入有效期天数 
            num2 = "10"
            casjc_log.logging.info(title + " 输入资源有效期")
            hailong.find_element_by_xpath('//div[@class="boxOne"][' + str(n) + ']/div/div[@class="el-table el-table--fit el-table--enable-row-hover el-table--enable-row-transition"]/div[@class="el-table__body-wrapper is-scrolling-none"]/table/tbody/tr[@class="el-table__row el-table__row--level-1"]/td[5]/div/div/input').send_keys(num2)
        #输入折后单价
        #num3 = "10"
        #casjc_log.logging.info(title + " 输入折后单价")
        #hailong.find_element_by_xpath('//div[@class="boxOne"][' + str(n) + ']/div/div[@class="el-table el-table--fit el-table--enable-row-hover el-table--enable-row-transition"]/div[@class="el-table__body-wrapper is-scrolling-none"]/table/tbody/tr[@class="el-table__row el-table__row--level-1"]/td[7]/div/div/div/input').clear()
        #hailong.find_element_by_xpath('//div[@class="boxOne"][' + str(n) + ']/div/div[@class="el-table el-table--fit el-table--enable-row-hover el-table--enable-row-transition"]/div[@class="el-table__body-wrapper is-scrolling-none"]/table/tbody/tr[@class="el-table__row el-table__row--level-1"]/td[7]/div/div/div/input').send_keys(num3)
    #判断配置方式，如果appcon[0][0]是0固定方式，如果是1灵活方式
    elif appcon[0][0] == 1:
        casjc_log.logging.info(title + " 选择配置方式，灵活配置")
        #目前配置方式只有一种，灵活配置不需在选择
        #hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')[len(listelement)-1].click()
        #填写基本信息完成，提交下一步
        hailong.find_elements_by_tag_name('button')[1].click()
        time.sleep(casjc_config.short_time)
        #进入提交资源申请页面
        WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="tableBox"]')))
        if appcon[0][1] == "gb":
            n = 1
        elif appcon[0][1] == "gg":
            n = 2
        elif appcon[0][1] == "yy":
            n = 3
        elif appcon[0][1] == "sw":
            n = 4
        elif appcon[0][1] == "sy":
            n = 5
        elif appcon[0][1] == "wg":
            n = 6
        #输出当前执行资源类型
        casjc_log.logging.info(title + " 当前操作的资源类型：" + hailong.find_elements_by_xpath('//div[@class="boxOne"]/div[@class="title"]')[n-1].text.split("\n")[0])
        #点击当前资源图标，展开规格
        casjc_log.logging.info(title + " 点击资源图标，展开规格")
        resicon = hailong.find_element_by_xpath('//div[@class="boxOne"][' + str(n) + ']/div/div[@class="el-table el-table--fit el-table--enable-row-hover el-table--enable-row-transition"]/div[@class="el-table__body-wrapper is-scrolling-none"]/table/tbody/tr/td/div[@class="cell"]/div[@class="el-table__expand-icon"]')
        resicon.click()
        #获取规格数据（暂存）
        reslistnum = hailong.find_elements_by_xpath('//div[@class="boxOne"][' + str(n) + ']/div/div[@class="el-table el-table--fit el-table--enable-row-hover el-table--enable-row-transition"]/div[@class="el-table__body-wrapper is-scrolling-none"]/table/tbody/tr[@class="el-table__row el-table__row--level-1"]')
        if appcon[0][1] == "gg":
             #输入有效期天数
            daynum = "1"
            casjc_log.logging.info(title + " 输入资源有效期")
            hailong.find_element_by_xpath('//div[@class="boxOne"][' + str(n) + ']/div/div[@class="el-table el-table--fit el-table--enable-row-hover el-table--enable-row-transition"]/div[@class="el-table__body-wrapper is-scrolling-none"]/table/tbody/tr[@class="el-table__row el-table__row--level-1"]/td[5]/div/div/input').send_keys(daynum)
            #输入折后单价
            pric = "2.5"
            casjc_log.logging.info(title + " 输入折后单价")
            hailong.find_element_by_xpath('//div[@class="boxOne"][' + str(n) + ']/div/div[@class="el-table el-table--fit el-table--enable-row-hover el-table--enable-row-transition"]/div[@class="el-table__body-wrapper is-scrolling-none"]/table/tbody/tr[@class="el-table__row el-table__row--level-1"]/td[7]/div/div/div/input').clear()
            hailong.find_element_by_xpath('//div[@class="boxOne"][' + str(n) + ']/div/div[@class="el-table el-table--fit el-table--enable-row-hover el-table--enable-row-transition"]/div[@class="el-table__body-wrapper is-scrolling-none"]/table/tbody/tr[@class="el-table__row el-table__row--level-1"]/td[7]/div/div/div/input').send_keys(pric)
        else:
            #输入有效期天数
            daynum = "1"
            casjc_log.logging.info(title + " 输入资源有效期")
            hailong.find_element_by_xpath('//div[@class="boxOne"][' + str(n) + ']/div/div[@class="el-table el-table--fit el-table--enable-row-hover el-table--enable-row-transition"]/div[@class="el-table__body-wrapper is-scrolling-none"]/table/tbody/tr[@class="el-table__row el-table__row--level-1"]/td[4]/div/div/input').send_keys(daynum)
            #输入折后单价
            pric = "2.5"
            casjc_log.logging.info(title + " 输入折后单价")
            hailong.find_element_by_xpath('//div[@class="boxOne"][' + str(n) + ']/div/div[@class="el-table el-table--fit el-table--enable-row-hover el-table--enable-row-transition"]/div[@class="el-table__body-wrapper is-scrolling-none"]/table/tbody/tr[@class="el-table__row el-table__row--level-1"]/td[6]/div/div/div/input').clear()
            hailong.find_element_by_xpath('//div[@class="boxOne"][' + str(n) + ']/div/div[@class="el-table el-table--fit el-table--enable-row-hover el-table--enable-row-transition"]/div[@class="el-table__body-wrapper is-scrolling-none"]/table/tbody/tr[@class="el-table__row el-table__row--level-1"]/td[6]/div/div/div/input').send_keys(pric)
        #输入报价总额
        totalpric = int(daynum) * float(pric) * 50
        hailong.find_element_by_xpath('//div[@class="footer-infor"]/span[2]/div/input').send_keys(str(totalpric))
    #点击提交申请按钮
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 点击提交申请按钮")
    hailong.find_element_by_css_selector('button[class="el-button el-button--primary el-button--small"]').click()
    #获取提交返回结果
    try:
        WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'p[class="el-message__content"]')))
        if len(hailong.find_element_by_css_selector('p[class="el-message__content"]').text) == 0:
            casjc_log.logging.info(title + " 提交申请后响应的信息为空，申请异常")
            casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, "申请资源失败,操作异常"  + " 甲方账号: " + jiafang]
            aaa.Casjc_logout()
            return None
        elif hailong.find_element_by_css_selector('p[class="el-message__content"]').text == "操作成功":
            #获取单号
            try:
                WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="details"]')))
                WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="aggregate"]')))
                time.sleep(casjc_config.short_time)
                orderavg = hailong.find_element_by_xpath('//div[@class="aggregate"]/span[1]').text
                ordernum = hailong.find_elements_by_tag_name('p')[2].text
                print(len(ordernum))
                if len(ordernum) < 6:
                    imagename = "订单号异常" + time.strftime("%m%d%H%M%S") + '.png'
                    hailong.save_screenshot(r'C:\usr\Apache24\htdocs\image\\' + imagename)
                    casjc_log.logging.info(title + " 提交申请资源后订单号显示异常,查看截图 %s" %imagename)
                    casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, "订单号显示异常"]
                    hailong.quit()
                    return None
            except exceptions.TimeoutException:
                imagename = title + time.strftime("%m%d%H%M%S") + '.png'
                hailong.save_screenshot(r'C:\usr\Apache24\htdocs\image\\' + imagename)
                casjc_log.logging.info(title + " 提交申请资源异常，未找到页面元素,查看截图 %s" %imagename)
                casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, "获取单号或平均价折扣失败，或没有进入提交成功页面"  + " 甲方账号: " + jiafang]
                hailong.quit()
                return None
            casjc_log.logging.info(title + " 提交申请资源成功," + ordernum)
            WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'p[class="el-message__content"]')))
            casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, ordernum + hailong.find_element_by_css_selector('p[class="el-message__content"]').text +  " 甲方账号: " + jiafang + orderavg]
            aaa.Casjc_logout()
            #申请成功后返回订单号，和资源类型（元组）
            return ordernum[4:],appcon[0]
        else:
            casjc_log.logging.info(title + " 提交申请资源响应异常")
            casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, hailong.find_element_by_css_selector('p[class="el-message__content"]').text + " 甲方账号: " + jiafang]
            aaa.Casjc_logout()
            return None
    except exceptions.TimeoutException:
        imagename = title + time.strftime("%m%d%H%M%S") + '.png'
        hailong.save_screenshot(r'C:\usr\Apache24\htdocs\image\\' + imagename)
        casjc_log.logging.info(title + " 提交申请资源异常，页面元素未找到,查看截图 %s" %imagename)
        casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, "申请资源失败,操作异常" + " 甲方账号: " + jiafang]
        aaa.Casjc_logout()
        return None



#申请资源跨服务区
def Casjc_res_area(*appcon):
    """
    0 固定方式
    1 灵活方式
    "gb" 高性能计算-标准型
    "gg" 高性能计算-共享型
    "yy" 云计算-云主机
    "sw" 数据存储-文件存储
    "sy" 数据存储-云硬盘
    "wg" 网络资源-公网IP
    
    申请资源返回值为一个订单号和一个元组包含：是否试用，资源类型，示例('20201026172520256', (0, 'gg'))
    """
    title = "申请资源-跨服务区"
    if not appcon:
        casjc_log.logging.info(title + " 没有传递appcon参数,终止执行")
        casjc_config.casjc_result[title + time.strftime("%M%S")] = ["", "没有传递appcon参数,终止执行"]
        return None    
    if appcon[0][0] == 0:
        if appcon[0][1] == "gb":
            title = "申请资源-固定方式-高性能计算-标准型"
        if appcon[0][1] == "gg":
            title = "申请资源-固定方式-高性能计算-共享型"
        if appcon[0][1] == "yy":
            title = "申请资源-固定方式-云计算-云主机"
        if appcon[0][1] == "sw":
            title = "申请资源-固定方式-数据存储-文件存储"
        if appcon[0][1] == "sy":
            title = "申请资源-固定方式-数据存储-云硬盘"
        if appcon[0][1] == "wg":
            title = "申请资源-固定方式-网络资源-公网IP"
    elif appcon[0][0] == 1:
        if appcon[0][1] == "gb":
            title = "申请资源-灵活方式-高性能计算-标准型"
        if appcon[0][1] == "gg":
            title = "申请资源-灵活方式-高性能计算-共享型"
        if appcon[0][1] == "yy":
            title = "申请资源-灵活方式-云计算-云主机"
        if appcon[0][1] == "sw":
            title = "申请资源-灵活方式-数据存储-文件存储"
        if appcon[0][1] == "sy":
            title = "申请资源-灵活方式-数据存储-云硬盘"
        if appcon[0][1] == "wg":
            title = "申请资源-灵活方式-网络资源-公网IP"
    casjc_log.logging.info(title)
    #登录，点击资源管理菜单
    uname = myconfig['user2']
    upasswd = myconfig['passwd2']
    uurl = myconfig['adminUrl']
    hailong = webdriver.Chrome()
    aaa = casjc_page.Casjc_admin_page(hailong,uname,upasswd,uurl)
    casjc_log.logging.info(title + " 进入资源管理菜单")
    aaa.admin_resmanagement()
    #点击申请资源按钮
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="el-row"]')))
    if appcon[0][0] == 0:
        casjc_log.logging.info(title + " 点击申请试用资源按钮")
        hailong.find_elements_by_tag_name('button')[1].click()
    elif appcon[0][0] == 1:
        casjc_log.logging.info(title + " 点击申请资源按钮")
        hailong.find_elements_by_tag_name('button')[0].click()
    time.sleep(casjc_config.show_time)
    #重新加载当前页面
    #hailong.refresh()
    if hailong.find_elements_by_css_selector('div[class="step-item"]')[1].text == "提交资源申请":
        casjc_log.logging.info(title + " 进入资源申请界面成功")
    else:
        casjc_log.logging.info(title + " 进入资源申请界面失败")
    #选择用户单位,选择最后一个
    casjc_log.logging.info(title + " 点击选择用户单位列表")
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[0].click()
    time.sleep(casjc_config.short_time)
    #Select(hailong.find_elements_by_css_selector('li[class="el-scrollbar__view el-select-dropdown__list""]')).select_by_value('国科北京分部')
    casjc_log.logging.info(title + " 选择单位列表中最后一个元素")
    hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')[-1].click()
    #hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')[-8].click()
    #获取选择的企业单位名称
    ent = hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')[-1].text
    #输入项目名称
    casjc_log.logging.info(title + " 输入项目名称")
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[1].send_keys('love爱')
    #选择甲方用户
    casjc_log.logging.info(title + " 选择甲方用户")
    #指定甲方用户,没有就点击，有就搜索
    suser = ""
    if not suser:
        hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[2].click()
    else:
        hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[2].send_keys(suser)
    time.sleep(casjc_config.short_time)
    try:
        time.sleep(casjc_config.show_time)
        if hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')[-1].text == "":
            jiafang = hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')[-2].text
            hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')[-2].click()
        else:
            jiafang = hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')[-1].text
            hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')[-1].click()
    except exceptions.ElementNotInteractableException:
        casjc_log.logging.info(title + " %s企业没有找到账号"%ent)
        casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, "当前企业没有找到账号"]
        aaa.Casjc_logout()
        return None
    #输入手机号
    casjc_log.logging.info(title + " 清空当前内容,输入手机号")
    time.sleep(casjc_config.short_time)
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[3].clear()
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[3].send_keys('13112341234')
    #输入邮箱
    casjc_log.logging.info(title + " 清空当前内容,输入邮箱")
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[4].clear()
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[4].send_keys('131@qq.com')
    #点击配置方式下拉框
    #hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[5].click()
    #time.sleep(casjc_config.short_time)
    #li标签列表数据长度,最后一个是灵活配置
    #listelement = hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')
    #判断配置方式，如果appcon[0][0]是0固定方式，如果是1灵活方式
    if appcon[0][0] == 0:
        casjc_log.logging.info(title + " 选择配置方式，固定配置")
        #hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')[len(listelement)-2].click()
        #填写基本信息完成，提交下一步
        hailong.find_elements_by_tag_name('button')[1].click()
        time.sleep(casjc_config.short_time)
        #进入提交资源申请页面
        WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="tableBox"]')))
        if appcon[0][1] == "gb":
            n = 1
        elif appcon[0][1] == "gg":
            n = 2
        elif appcon[0][1] == "yy":
            n = 3
        elif appcon[0][1] == "sw":
            n = 4
        elif appcon[0][1] == "sy":
            n = 5
        elif appcon[0][1] == "wg":
            n = 6
        #输出当前执行资源类型
        casjc_log.logging.info(title + " 当前操作的资源类型：" + hailong.find_elements_by_xpath('//div[@class="boxOne"]/div[@class="title"]')[n-1].text.split("\n")[0])
        #点击当前资源图标，展开规格
        casjc_log.logging.info(title + " 点击资源图标，展开规格")
        resicon = hailong.find_element_by_xpath('//div[@class="boxOne"][' + str(n) + ']/div/div[@class="el-table el-table--fit el-table--enable-row-hover el-table--enable-row-transition"]/div[@class="el-table__body-wrapper is-scrolling-none"]/table/tbody/tr/td/div[@class="cell"]/div[@class="el-table__expand-icon"]')
        resicon.click()
        #获取规格数据（暂存）
        reslistnum = hailong.find_elements_by_xpath('//div[@class="boxOne"][' + str(n) + ']/div/div[@class="el-table el-table--fit el-table--enable-row-hover el-table--enable-row-transition"]/div[@class="el-table__body-wrapper is-scrolling-none"]/table/tbody/tr[@class="el-table__row el-table__row--level-1"]')
        #输入数量
        num1 = "1"
        casjc_log.logging.info(title + " 输入资源数量")
        hailong.find_element_by_xpath('//div[@class="boxOne"][' + str(n) + ']/div/div[@class="el-table el-table--fit el-table--enable-row-hover el-table--enable-row-transition"]/div[@class="el-table__body-wrapper is-scrolling-none"]/table/tbody/tr[@class="el-table__row el-table__row--level-1"]/td[4]/div/div/input').send_keys(num1)
        #输入有效期天数
        num2 = "1"
        casjc_log.logging.info(title + " 输入资源有效期")
        hailong.find_element_by_xpath('//div[@class="boxOne"][' + str(n) + ']/div/div[@class="el-table el-table--fit el-table--enable-row-hover el-table--enable-row-transition"]/div[@class="el-table__body-wrapper is-scrolling-none"]/table/tbody/tr[@class="el-table__row el-table__row--level-1"]/td[5]/div/div/input').send_keys(num2)
        #点击服务区二
        casjc_log.logging.info(title + " 点击服务区--太原二区")
        hailong.find_elements_by_css_selector('span[class="el-radio-button__inner"]')[1].click()
        time.sleep(casjc_config.short_time)
        #输出当前执行资源类型
        casjc_log.logging.info(title + " 当前操作的资源类型：" + hailong.find_elements_by_xpath('//div[@class="boxOne"]/div[@class="title"]')[0].text.split("\n")[0])
        #点击当前资源图标，展开规格
        casjc_log.logging.info(title + " 点击资源图标，展开规格")
        resicon = hailong.find_element_by_xpath('//div[@class="boxOne"][1]/div/div[@class="el-table el-table--fit el-table--enable-row-hover el-table--enable-row-transition"]/div[@class="el-table__body-wrapper is-scrolling-none"]/table/tbody/tr/td/div[@class="cell"]/div[@class="el-table__expand-icon"]')
        resicon.click()
        #获取规格数据（暂存）
        reslistnum = hailong.find_elements_by_xpath('//div[@class="boxOne"][1]/div/div[@class="el-table el-table--fit el-table--enable-row-hover el-table--enable-row-transition"]/div[@class="el-table__body-wrapper is-scrolling-none"]/table/tbody/tr[@class="el-table__row el-table__row--level-1"]')
        #输入数量
        num1 = "1"
        casjc_log.logging.info(title + " 输入资源数量")
        hailong.find_element_by_xpath('//div[@class="boxOne"][1]/div/div[@class="el-table el-table--fit el-table--enable-row-hover el-table--enable-row-transition"]/div[@class="el-table__body-wrapper is-scrolling-none"]/table/tbody/tr[@class="el-table__row el-table__row--level-1"]/td[4]/div/div/input').send_keys(num1)
        #输入有效期天数
        num2 = "1"
        casjc_log.logging.info(title + " 输入资源有效期")
        hailong.find_element_by_xpath('//div[@class="boxOne"][1]/div/div[@class="el-table el-table--fit el-table--enable-row-hover el-table--enable-row-transition"]/div[@class="el-table__body-wrapper is-scrolling-none"]/table/tbody/tr[@class="el-table__row el-table__row--level-1"]/td[5]/div/div/input').send_keys(num2)

        #输入折后单价
        #num3 = "10"
        #casjc_log.logging.info(title + " 输入折后单价")
        #hailong.find_element_by_xpath('//div[@class="boxOne"][' + str(n) + ']/div/div[@class="el-table el-table--fit el-table--enable-row-hover el-table--enable-row-transition"]/div[@class="el-table__body-wrapper is-scrolling-none"]/table/tbody/tr[@class="el-table__row el-table__row--level-1"]/td[7]/div/div/div/input').clear()
        #hailong.find_element_by_xpath('//div[@class="boxOne"][' + str(n) + ']/div/div[@class="el-table el-table--fit el-table--enable-row-hover el-table--enable-row-transition"]/div[@class="el-table__body-wrapper is-scrolling-none"]/table/tbody/tr[@class="el-table__row el-table__row--level-1"]/td[7]/div/div/div/input').send_keys(num3)
    #判断配置方式，如果appcon[0][0]是0固定方式，如果是1灵活方式
    elif appcon[0][0] == 1:
        casjc_log.logging.info(title + " 选择配置方式，灵活配置")
        #目前配置方式只有一种，灵活配置不需在选择
        #hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')[len(listelement)-1].click()
        #填写基本信息完成，提交下一步
        hailong.find_elements_by_tag_name('button')[1].click()
        time.sleep(casjc_config.short_time)
        #进入提交资源申请页面
        WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="tableBox"]')))
        if appcon[0][1] == "gb":
            n = 1
        elif appcon[0][1] == "gg":
            n = 2
        elif appcon[0][1] == "yy":
            n = 3
        elif appcon[0][1] == "sw":
            n = 4
        elif appcon[0][1] == "sy":
            n = 5
        elif appcon[0][1] == "wg":
            n = 6
        #输出当前执行资源类型
        casjc_log.logging.info(title + " 当前操作的资源类型：" + hailong.find_elements_by_xpath('//div[@class="boxOne"]/div[@class="title"]')[n-1].text.split("\n")[0])
        #点击当前资源图标，展开规格
        casjc_log.logging.info(title + " 点击资源图标，展开规格")
        resicon = hailong.find_element_by_xpath('//div[@class="boxOne"][' + str(n) + ']/div/div[@class="el-table el-table--fit el-table--enable-row-hover el-table--enable-row-transition"]/div[@class="el-table__body-wrapper is-scrolling-none"]/table/tbody/tr/td/div[@class="cell"]/div[@class="el-table__expand-icon"]')
        resicon.click()
        #获取规格数据（暂存）
        reslistnum = hailong.find_elements_by_xpath('//div[@class="boxOne"][' + str(n) + ']/div/div[@class="el-table el-table--fit el-table--enable-row-hover el-table--enable-row-transition"]/div[@class="el-table__body-wrapper is-scrolling-none"]/table/tbody/tr[@class="el-table__row el-table__row--level-1"]')
        #输入有效期天数
        daynum = "10"
        casjc_log.logging.info(title + " 输入资源有效期")
        hailong.find_element_by_xpath('//div[@class="boxOne"][' + str(n) + ']/div/div[@class="el-table el-table--fit el-table--enable-row-hover el-table--enable-row-transition"]/div[@class="el-table__body-wrapper is-scrolling-none"]/table/tbody/tr[@class="el-table__row el-table__row--level-1"]/td[4]/div/div/input').send_keys(daynum)
        #输入折后单价
        pric = "2.5"
        casjc_log.logging.info(title + " 输入折后单价")
        hailong.find_element_by_xpath('//div[@class="boxOne"][' + str(n) + ']/div/div[@class="el-table el-table--fit el-table--enable-row-hover el-table--enable-row-transition"]/div[@class="el-table__body-wrapper is-scrolling-none"]/table/tbody/tr[@class="el-table__row el-table__row--level-1"]/td[6]/div/div/div/input').clear()
        hailong.find_element_by_xpath('//div[@class="boxOne"][' + str(n) + ']/div/div[@class="el-table el-table--fit el-table--enable-row-hover el-table--enable-row-transition"]/div[@class="el-table__body-wrapper is-scrolling-none"]/table/tbody/tr[@class="el-table__row el-table__row--level-1"]/td[6]/div/div/div/input').send_keys(pric)
        #点击服务区二
        casjc_log.logging.info(title + " 点击服务区--太原二区")
        hailong.find_elements_by_css_selector('span[class="el-radio-button__inner"]')[1].click()
        time.sleep(casjc_config.short_time)
        #输出当前执行资源类型--填写高性能资源申请
        casjc_log.logging.info(title + " 当前操作的资源类型：" + hailong.find_elements_by_xpath('//div[@class="boxOne"]/div[@class="title"]')[0].text.split("\n")[0])
        #点击当前资源图标，展开规格
        casjc_log.logging.info(title + " 点击资源图标，展开规格")
        resicon = hailong.find_element_by_xpath('//div[@class="boxOne"][1]/div/div[@class="el-table el-table--fit el-table--enable-row-hover el-table--enable-row-transition"]/div[@class="el-table__body-wrapper is-scrolling-none"]/table/tbody/tr/td/div[@class="cell"]/div[@class="el-table__expand-icon"]')
        resicon.click()
        #获取规格数据（暂存）
        reslistnum = hailong.find_elements_by_xpath('//div[@class="boxOne"][1]/div/div[@class="el-table el-table--fit el-table--enable-row-hover el-table--enable-row-transition"]/div[@class="el-table__body-wrapper is-scrolling-none"]/table/tbody/tr[@class="el-table__row el-table__row--level-1"]')
        #输入有效期天数
        daynum = "10"
        casjc_log.logging.info(title + " 输入资源有效期")
        hailong.find_element_by_xpath('//div[@class="boxOne"][1]/div/div[@class="el-table el-table--fit el-table--enable-row-hover el-table--enable-row-transition"]/div[@class="el-table__body-wrapper is-scrolling-none"]/table/tbody/tr[@class="el-table__row el-table__row--level-1"]/td[4]/div/div/input').send_keys(daynum)
        #输入折后单价
        pric = "0.16"
        casjc_log.logging.info(title + " 输入折后单价")
        hailong.find_element_by_xpath('//div[@class="boxOne"][1]/div/div[@class="el-table el-table--fit el-table--enable-row-hover el-table--enable-row-transition"]/div[@class="el-table__body-wrapper is-scrolling-none"]/table/tbody/tr[@class="el-table__row el-table__row--level-1"]/td[6]/div/div/div/input').clear()
        hailong.find_element_by_xpath('//div[@class="boxOne"][1]/div/div[@class="el-table el-table--fit el-table--enable-row-hover el-table--enable-row-transition"]/div[@class="el-table__body-wrapper is-scrolling-none"]/table/tbody/tr[@class="el-table__row el-table__row--level-1"]/td[6]/div/div/div/input').send_keys(pric)
        #输出当前执行资源类型--填写存储资源申请
        casjc_log.logging.info(title + " 当前操作的资源类型：" + hailong.find_elements_by_xpath('//div[@class="boxOne"]/div[@class="title"]')[1].text.split("\n")[0])
        #点击当前资源图标，展开规格
        casjc_log.logging.info(title + " 点击资源图标，展开规格")
        resicon = hailong.find_element_by_xpath('//div[@class="boxOne"][2]/div/div[@class="el-table el-table--fit el-table--enable-row-hover el-table--enable-row-transition"]/div[@class="el-table__body-wrapper is-scrolling-none"]/table/tbody/tr/td/div[@class="cell"]/div[@class="el-table__expand-icon"]')
        resicon.click()
        #获取规格数据（暂存）
        reslistnum = hailong.find_elements_by_xpath('//div[@class="boxOne"][2]/div/div[@class="el-table el-table--fit el-table--enable-row-hover el-table--enable-row-transition"]/div[@class="el-table__body-wrapper is-scrolling-none"]/table/tbody/tr[@class="el-table__row el-table__row--level-1"]')
        #输入有效期天数
        daynum = "10"
        casjc_log.logging.info(title + " 输入资源有效期")
        hailong.find_element_by_xpath('//div[@class="boxOne"][2]/div/div[@class="el-table el-table--fit el-table--enable-row-hover el-table--enable-row-transition"]/div[@class="el-table__body-wrapper is-scrolling-none"]/table/tbody/tr[@class="el-table__row el-table__row--level-1"]/td[4]/div/div/input').send_keys(daynum)
        #输入折后单价
        pric = "90"
        casjc_log.logging.info(title + " 输入折后单价")
        hailong.find_element_by_xpath('//div[@class="boxOne"][2]/div/div[@class="el-table el-table--fit el-table--enable-row-hover el-table--enable-row-transition"]/div[@class="el-table__body-wrapper is-scrolling-none"]/table/tbody/tr[@class="el-table__row el-table__row--level-1"]/td[6]/div/div/div/input').clear()
        hailong.find_element_by_xpath('//div[@class="boxOne"][2]/div/div[@class="el-table el-table--fit el-table--enable-row-hover el-table--enable-row-transition"]/div[@class="el-table__body-wrapper is-scrolling-none"]/table/tbody/tr[@class="el-table__row el-table__row--level-1"]/td[6]/div/div/div/input').send_keys(pric)
        #输入报价总额
        totalpric = int(daynum) * float(pric) * 50
        hailong.find_element_by_xpath('//div[@class="footer-infor"]/span[2]/div/input').send_keys(str(totalpric))
    #点击提交申请按钮
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 点击提交申请按钮")
    hailong.find_element_by_css_selector('button[class="el-button el-button--primary el-button--small"]').click()
    #获取提交返回结果
    try:
        WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'p[class="el-message__content"]')))
        if len(hailong.find_element_by_css_selector('p[class="el-message__content"]').text) == 0:
            casjc_log.logging.info(title + " 提交申请后响应的信息为空，申请异常")
            casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, "申请资源失败,操作异常"  + " 甲方账号: " + jiafang]
            aaa.Casjc_logout()
            return None
        elif hailong.find_element_by_css_selector('p[class="el-message__content"]').text == "操作成功":
            #获取单号
            try:
                WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="details"]')))
                WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="aggregate"]')))
                time.sleep(casjc_config.short_time)
                orderavg = hailong.find_element_by_xpath('//div[@class="aggregate"]/span[1]').text
                ordernum = hailong.find_elements_by_tag_name('p')[2].text
                print(len(ordernum))
                if len(ordernum) < 6:
                    imagename = "订单号异常" + time.strftime("%m%d%H%M%S") + '.png'
                    hailong.save_screenshot(r'C:\usr\Apache24\htdocs\image\\' + imagename)
                    casjc_log.logging.info(title + " 提交申请资源后订单号显示异常,查看截图 %s" %imagename)
                    casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, "订单号显示异常"]
                    hailong.quit()
                    return None
            except exceptions.TimeoutException:
                imagename = title + time.strftime("%m%d%H%M%S") + '.png'
                hailong.save_screenshot(r'C:\usr\Apache24\htdocs\image\\' + imagename)
                casjc_log.logging.info(title + " 提交申请资源异常，未找到页面元素,查看截图 %s" %imagename)
                casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, "获取单号或平均价折扣失败，或没有进入提交成功页面"  + " 甲方账号: " + jiafang]
                hailong.quit()
                return None
            casjc_log.logging.info(title + " 提交申请资源成功," + ordernum)
            casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, ordernum + hailong.find_element_by_css_selector('p[class="el-message__content"]').text +  " 甲方账号: " + jiafang + orderavg]
            aaa.Casjc_logout()
            #申请成功后返回订单号，和资源类型
            return ordernum[4:],appcon[0]
        else:
            casjc_log.logging.info(title + " 提交申请资源响应异常")
            casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, hailong.find_element_by_css_selector('p[class="el-message__content"]').text + " 甲方账号: " + jiafang]
            aaa.Casjc_logout()
            return None
    except exceptions.TimeoutException:
        imagename = title + time.strftime("%m%d%H%M%S") + '.png'
        hailong.save_screenshot(r'C:\usr\Apache24\htdocs\image\\' + imagename)
        casjc_log.logging.info(title + " 提交申请资源异常，页面元素未找到,查看截图 %s" %imagename)
        casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, "申请资源失败,操作异常" + " 甲方账号: " + jiafang]
        aaa.Casjc_logout()
        return None



#价格审批
def Casjc_price(priceuser="", ordernum=""):
    title = "价格审批"
    casjc_log.logging.info(title + " 本次要审批的订单号," + ordernum)
    #登录，点击资源管理菜单
    hailong = webdriver.Chrome()
    uname = priceuser
    upasswd = myconfig['passwd2']
    uurl = myconfig['adminUrl']
    aaa = casjc_page.Casjc_admin_page(hailong,uname,upasswd,uurl)
    casjc_log.logging.info(title + " 进入资源管理菜单")
    aaa.admin_resmanagement()
    #进入资源审批页面
    if priceuser != "tangdebing":
        try:
            WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="el-submenu__title"]')))
            time.sleep(casjc_config.short_time)
            casjc_log.logging.info(title + " 进入资源审批菜单")
            if uname != "daijiwei":
                hailong.find_elements_by_css_selector('i[class="el-icon- iconfont iconshenpizhong"]')[0].click()
            time.sleep(casjc_config.short_time)
            #进入待审批列表
            casjc_log.logging.info(title + " 进入待审批菜单")
            hailong.find_element_by_css_selector('li[data-index="/approveWat"]').click()
            time.sleep(casjc_config.short_time)
        except exceptions.TimeoutException:
            imagename = title + time.strftime("%m%d%H%M%S") + '.png'
            hailong.save_screenshot(r'C:\usr\Apache24\htdocs\image\\' + imagename)
            casjc_log.logging.info(title + " 进入资源审批菜单异常,查看截图 %s" % imagename)
            casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, " 操作异常"]
            aaa.Casjc_logout()
            return None
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'li[data-index="/approveWat"]')))
    if hailong.find_elements_by_css_selector('li[data-index="/approveWat"]')[0].text == "待审批":
        casjc_log.logging.info(title + " 进入资源审批-待审批列表成功")
    else:
        casjc_log.logging.info(title + " 进入资源审批-待审批列表失败")
    #调用admin_appwait获取第一页是否有符合的订单号
    aaa.admin_appwait(title, uname, ordernum)
    #等待页面元素，确认是否进入审批详情页
    try:
        WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'textarea[class="el-textarea__inner')))
    except exceptions.TimeoutException:
        imagename = title + time.strftime("%m%d%H%M%S") + '.png'
        hailong.save_screenshot(r'C:\usr\Apache24\htdocs\image\\' + imagename)
        casjc_log.logging.info(title + " 没有找到价格审批页面审批意见元素,退出审批,查看截图 %s" %imagename)
        casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, "没有找到价格审批页面审批意见元素"]
        aaa.Casjc_logout()
        return None
    #输入审批意见
    casjc_log.logging.info(title + " 输入审批意见")
    hailong.find_element_by_css_selector('textarea[class="el-textarea__inner"]').send_keys(u"UI自动化审批")
    #进入申请信息tab，获取订单号
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[role="radiogroup"]')))
    time.sleep(casjc_config.short_time)
    hailong.find_elements_by_css_selector('span[class="el-radio-button__inner"]')[1].click()
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="details"]')))
    time.sleep(casjc_config.short_time)
    ordernum2 = hailong.find_elements_by_tag_name('p')[2].text
    casjc_log.logging.info(title + " 获取当前操作的订单号," + ordernum2)
    if ordernum != ordernum2[4:]:
        casjc_log.logging.info(title + " 预期价格审批的订单号与实际操作的订单号不同,终止审批")
        casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, "预期价格审批的订单号与实际操作的订单号不同,终止审批"]
        aaa.Casjc_logout()
        return None        
    try:
        #点击审批通过
        WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'button[class="el-button el-button--primary"]')))
        casjc_log.logging.info(title + " 点击审批通过按钮")
        hailong.find_element_by_css_selector('button[class="el-button el-button--primary"]').click()
    except exceptions.TimeoutException:
        imagename = title + time.strftime("%m%d%H%M%S") + '.png'
        hailong.save_screenshot(r'C:\usr\Apache24\htdocs\image\\' + imagename)
        casjc_log.logging.info(title + " 点击审批通过异常,查看截图 %s" % imagename)
    #获取提交返回结果
    aaa.admin_result(title,uname,ordernum)
    return None


#生成合同
def Casjc_contract(ordernum="20200831141130277"):
    title = "生成合同"
    casjc_log.logging.info(title + " 本次要生成合同的订单号," + ordernum)
    #登录，点击资源管理菜单
    hailong = webdriver.Chrome()
    uname = myconfig['user2']
    upasswd = myconfig['passwd2']
    uurl = myconfig['adminUrl']
    aaa = casjc_page.Casjc_admin_page(hailong,uname,upasswd,uurl)
    casjc_log.logging.info(title + " 进入资源管理菜单")
    aaa.admin_resmanagement()         
    #进入资源审批页面
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="el-submenu__title"]')))
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 进入资源审批页面")
    hailong.find_elements_by_css_selector('div[class="el-submenu__title"]')[0].click()
    time.sleep(casjc_config.short_time)
    #进入待审批列表
    casjc_log.logging.info(title + " 进入待审批列表")
    hailong.find_elements_by_css_selector('li[role="menuitem"]')[2].click()
    time.sleep(casjc_config.short_time)
    if hailong.find_elements_by_css_selector('span[class="el-breadcrumb__inner"]')[2].text == "待审批":
        casjc_log.logging.info(title + " 进入资源审批-待审批列表成功")
    else:
        casjc_log.logging.info(title + " 进入资源审批-待审批列表失败")
    #调用admin_appwait获取第一页是否有符合的订单号
    aaa.admin_appwait(title, uname, ordernum)
    try:
        #等待页面元素，确认是否进入生产合同详情页
        WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="title"]')))    
    except exceptions.TimeoutException:
        imagename = title + time.strftime("%m%d%H%M%S") + '.png'
        hailong.save_screenshot(r'C:\usr\Apache24\htdocs\image\\' + imagename)
        casjc_log.logging.info(title + " 没有找到生成合同页面附件列表元素,退出生成合同,查看截图 %s" %imagename)
        casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, "没有找到生成合同页面附件列表元素"]
        aaa.Casjc_logout()
        return None
    #点击上传按钮
    casjc_log.logging.info(title + " 点击上传文件按钮")
    hailong.find_elements_by_css_selector('button[class="el-button el-button--primary el-button--small"]')[0].click()
    time.sleep(casjc_config.short_time)
    #上传文件
    casjc_mode.Casjc_upload(casjc_config.uppath)
    time.sleep(casjc_config.short_time)
    #选择付款条件
    casjc_log.logging.info(title + " 选择付款条件")
    hailong.find_elements_by_css_selector('input[placeholder="请选择付款条件"]')[0].click()
    time.sleep(casjc_config.short_time)
    bb = hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')
    bb[1].click()
    hailong.find_elements_by_css_selector('input[placeholder="付款期限"]')[0].send_keys('1')
    hailong.find_elements_by_css_selector('input[placeholder="付款百分比"]')[0].send_keys('100')
    #获取合同编号
    contractnum = hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[3].get_attribute('title')
    if contractnum == "" or contractnum == None:
        imagename = title + time.strftime("%m%d%H%M%S") + '.png'
        hailong.save_screenshot(r'C:\usr\Apache24\htdocs\image\\' + imagename)
        casjc_log.logging.info(title + " 没有显示合同号,查看截图 %s" %imagename)
        casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, "没有显示合同号"]
        aaa.Casjc_logout()
        return None
    #选择签署日期
    casjc_log.logging.info(title + " 当前操作合同号：%s" %contractnum)
    casjc_log.logging.info(title + " 选择签署日期")
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[5].click()
    time.sleep(casjc_config.short_time)
    hailong.find_elements_by_css_selector('td[class="available today"]')[0].click()
    #选择发货日期
    casjc_log.logging.info(title + " 选择发货日期")
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[6].click()
    time.sleep(casjc_config.short_time)
    hailong.find_elements_by_css_selector('td[class="available today"]')[0].click()
    #选择服务起始日期
    casjc_log.logging.info(title + " 选择服务起始日期")
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[7].click()
    time.sleep(casjc_config.short_time)
    hailong.find_elements_by_css_selector('td[class="available today"]')[0].click()
    #选择服务截止日期
    casjc_log.logging.info(title + " 选择服务截至日期")
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[8].click()
    time.sleep(casjc_config.short_time)
    #获取日期元素中数据长度，倒数第十个是日期
    #listelement = hailong.find_elements_by_css_selector('td[class="available"]')
    #hailong.find_elements_by_css_selector('td[class="available"]')[len(listelement) - 10].click()
    #当月没有可选日期，用这个
    try:
        hailong.find_elements_by_xpath('//tr[@class="el-date-table__row"]/td[@class="available"]/div/span')[-1].click()
    except:
        #选择日历页最后一天
        hailong.find_elements_by_xpath('//td[@class="next-month"]')[-1].click()
    time.sleep(casjc_config.short_time)
    #选择合同章
    casjc_log.logging.info(title + " 选择合同章")
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[10].click()
    time.sleep(casjc_config.short_time)
    hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')[-1].click()
    #进入申请信息tab，获取订单号
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[role="radiogroup"]')))
    time.sleep(casjc_config.short_time)
    hailong.find_elements_by_css_selector('span[class="el-radio-button__inner"]')[1].click()
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="details"]')))
    time.sleep(casjc_config.short_time)
    ordernum2 = hailong.find_elements_by_tag_name('p')[2].text
    casjc_log.logging.info(title + " 获取当前操的订单号，" + ordernum2)
    if ordernum != ordernum2[4:]:
        casjc_log.logging.info(title + " 预期生成合同的订单号与实际操作的订单号不同,终止生成")
        casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, "预期生成合同的订单号与实际操作的订单号不同,终止生成"]
        aaa.Casjc_logout()
        return None
    #点击生产合同
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 点击生成合同按钮")
    hailong.find_element_by_css_selector('button[class="el-button el-button--primary"').click()
    #获取提交返回结果
    ordernum = ordernum + " 合同号: " + contractnum
    aaa.admin_result(title,uname,ordernum)
    return None



#合同审批
def Casjc_contract_apply(appuser,ordernum):
    title = "合同审批"
    casjc_log.logging.info(title + " 本次要审批的订单号," + ordernum)
    #登录，点击资源管理菜单
    hailong = webdriver.Chrome()
    uname = appuser
    upasswd = myconfig['passwd2']
    uurl = myconfig['adminUrl']
    aaa = casjc_page.Casjc_admin_page(hailong,uname,upasswd,uurl)
    casjc_log.logging.info(title + " 进入资源管理菜单")
    aaa.admin_resmanagement()
    if uname == "wangnan":
        try:
            WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="el-submenu__title"]')))
            time.sleep(casjc_config.short_time)
            casjc_log.logging.info(title + " 进入资源审批菜单")
            hailong.find_elements_by_css_selector('i[class="el-icon- iconfont iconshenpizhong"]')[0].click()
            time.sleep(casjc_config.short_time)
            #进入待审批列表
            casjc_log.logging.info(title + " 进入待审批菜单")
            hailong.find_element_by_css_selector('li[data-index="/approveWat"]').click()
            time.sleep(casjc_config.short_time)
        except exceptions.TimeoutException:
            imagename = title + time.strftime("%m%d%H%M%S") + '.png'
            hailong.save_screenshot(r'C:\usr\Apache24\htdocs\image\\' + imagename)
            casjc_log.logging.info(title + " 进入资源审批菜单异常,查看截图 %s" % imagename)
            casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, " 操作异常"]
            aaa.Casjc_logout()
            return None
        
    #进入资源审批页面,点击审批按钮
    try:        
        WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="table-btn"]')))
        #调用admin_appwait获取第一页是否有符合的订单号
        aaa.admin_appwait(title, uname, ordernum)
        try:
            #等待页面元素，确认是否进入生产合同详情页
            WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'label[class="el-checkbox"]')))    
        except exceptions.TimeoutException:
            imagename = title + time.strftime("%m%d%H%M%S") + '.png'
            hailong.save_screenshot(r'C:\usr\Apache24\htdocs\image\\' + imagename)
            casjc_log.logging.info(title + " 没有找到合同审批页面复选框元素,操作异常退出审批,查看截图 %s" %imagename)
            casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, "没有找到合同审批页面复选框元素"]
            aaa.Casjc_logout()
            return None
    except:
        imagename = title + time.strftime("%m%d%H%M%S") + '.png'
        hailong.save_screenshot(r'C:\usr\Apache24\htdocs\image\\' + imagename)
        casjc_log.logging.info(title + " 没有找到资源审批页面元素，操作异常退出审批,查看截图 %s" %imagename)
        casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, " 操作异常"]
        aaa.Casjc_logout()
        return None
    #勾选复选框,附件内容已确认
    try:
        WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'label[class="el-checkbox"]')))
        casjc_log.logging.info(title + " 勾选合同审批复选框")
        hailong.find_element_by_css_selector('label[class="el-checkbox"]').click()
    except exceptions.TimeoutException:
        imagename = title + time.strftime("%m%d%H%M%S") + '.png'
        hailong.save_screenshot(r'C:\usr\Apache24\htdocs\image\\' + imagename)
        casjc_log.logging.info(title + " 勾选合同审批页面复选框异常，退出审批, 查看截图 %s" %imagename)
        casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, " 操作异常"]
        aaa.Casjc_logout()
        return None
    #输入审批意见
    casjc_log.logging.info(title + " 输入审批意见")
    hailong.find_elements_by_css_selector('textarea[class="el-textarea__inner"]')[0].send_keys(u"UI自动化合同审批")
    #进入申请信息tab，获取订单号
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[role="radiogroup"]')))
    time.sleep(casjc_config.short_time)
    hailong.find_elements_by_css_selector('span[class="el-radio-button__inner"]')[1].click()
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="details"]')))
    time.sleep(casjc_config.short_time)
    ordernum2 = hailong.find_elements_by_tag_name('p')[2].text
    casjc_log.logging.info(title + " 获取当前操作订单号," + ordernum2)
    if ordernum != ordernum2[4:]:
        casjc_log.logging.info(title + " 预期审批合同的订单号与实际操作的订单号不同,终止审批")
        casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, "预期审批合同的订单号与实际操作的订单号不同,终止审批"]
        aaa.Casjc_logout()
        return None
    try:
        #点击审批通过
        time.sleep(casjc_config.short_time)
        casjc_log.logging.info(title + " 点击审批通过按钮")
        hailong.find_element_by_css_selector('button[class="el-button el-button--primary"]').click()
    except:
        imagename = title + time.strftime("%m%d%H%M%S") + '.png'
        hailong.save_screenshot(r'C:\usr\Apache24\htdocs\image\\' + imagename)
        casjc_log.logging.info(title + " 点击审批通过按钮异常，查看截图 %s" %imagename)
        ordernum = "合同审批按钮点击异常"
  #获取提交返回结果
    aaa.admin_result(title,uname,ordernum)
    return None



#确认参数
def Casjc_change_config(*myorderes):
    title = "确认参数"
    orderes = myorderes[0]
    ordernum = orderes[0]
    casjc_log.logging.info(title + " 本次预期要操作的订单，" + ordernum)
    #登录，点击资源管理菜单
    hailong = webdriver.Chrome()
    uname = myconfig['user2']
    upasswd = myconfig['passwd2']
    uurl = myconfig['adminUrl']
    aaa = casjc_page.Casjc_admin_page(hailong,uname,upasswd,uurl)
    casjc_log.logging.info(title + " 进入资源管理菜单")
    aaa.admin_resmanagement() 
    #进入配置资源页面
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'li[data-index="/configTable"]')))
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 进入配置资源页面")
    hailong.find_elements_by_css_selector('li[data-index="/configTable"]')[0].click()
    time.sleep(casjc_config.short_time)
    try:
        #等待加载待审批列表页面元素
        WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'thead[class="has-gutter"]')))
        time.sleep(casjc_config.short_time)
        WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'tr[class="el-table__row"]')))
        time.sleep(casjc_config.short_time)
        #获取第一页列表数据条数
        listnum = hailong.find_elements_by_css_selector('tr[class="el-table__row"]')
        #如果条数0，退出
        casjc_log.logging.info(title + " 当前列表页数据条数: %s" %len(listnum))
        if len(listnum) == 0:
            casjc_log.logging.info(title + " 没有待配置资源,退出操作")
            casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, "没有待配置资源"]
            aaa.Casjc_logout()
            return None
        mytmp = 0
        #循环遍历第一页列表是否有符合的订单号，如果有点击生成合同，没有退出
        for i in range(len(listnum)):
            if hailong.find_element_by_xpath('//tr[@class="el-table__row"][' + str(i+1) + ']/td/div[@class="cell el-tooltip"][1]').text == ordernum:
                casjc_log.logging.info(title + " 找到预期订单，点击变更或确认按钮")
                hailong.find_element_by_xpath('//tr[@class="el-table__row"][' + str(i+1) + ']/td/div[@class="cell"]/div[@class="table-btn"]/button[2]').click()
                time.sleep(casjc_config.short_time)
                mytmp = 1
                break
        if mytmp == 0:
            casjc_log.logging.info(title + " 配置资源列表第一页没有找到符合的订单号")
            casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, "配置资源列表第一页没有找到符合的订单号"]
            aaa.Casjc_logout()
            return None            
    except exceptions.TimeoutException:
        imagename = title + time.strftime("%m%d%H%M%S") + '.png'
        hailong.save_screenshot(r'C:\usr\Apache24\htdocs\image\\' + imagename)
        casjc_log.logging.info(title + " 配置资源列表页缺失元素，退出登录, 查看截图 %s" %imagename)
        casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, "配置资源列表页缺失元素"]
        aaa.Casjc_logout()
        return None
    #等待页面元素，确认是否进入变更配置或确认参数详情页
    try:
        WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'thead[class="has-gutter')))
    except exceptions.TimeoutException:
        imagename = title + time.strftime("%m%d%H%M%S") + '.png'
        hailong.save_screenshot(r'C:\usr\Apache24\htdocs\image\\' + imagename)
        casjc_log.logging.info(title + " 没有找到页面元素，退出登录,查看截图 %s" %imagename)
        casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, "没有找到页面元素"]
        aaa.Casjc_logout()
        return None
    #云计算-云主机
    if orderes[1][1] == "yy":
        #选择集群
        casjc_log.logging.info(title + " 选择集群")
        hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[0].click()
        time.sleep(casjc_config.short_time)
        hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')[-2].click()
        time.sleep(casjc_config.short_time)
        #选择镜像
        casjc_log.logging.info(title + " 选择镜像")
        hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[1].click()
        time.sleep(casjc_config.short_time)
        hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')[-1].click()
        print(hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')[-1].text)
        #输入数量
        casjc_log.logging.info(title + " 输入数量")
        hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[2].clear()
        hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[2].send_keys("1")
        #有效期开始时间
        hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[3].click()
        casjc_log.logging.info(title + " 选择有效期开始时间")
        time.sleep(casjc_config.short_time)
        hailong.find_elements_by_css_selector('td[class="available today"]')[0].click()
        #有效期结束时间
        casjc_log.logging.info(title + " 选择有效期结束时间")
        hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[4].click()
        time.sleep(casjc_config.short_time)
        #2.3x需求已去掉试用类型的变更配置，下面功能正常只会执行try
        #如果是试用只能选择固定的天数，此处根据报错判断选择日期方式
        try:
            hailong.find_elements_by_css_selector('td[class="available today"]')[0].click()
        except exceptions.ElementNotInteractableException:
            aa = hailong.find_elements_by_xpath('//div[@class="el-picker-panel__content"]/table[@class="el-date-table"]/tbody/tr[@class="el-date-table__row"]/td[@class="available"][1]')
            aa[-1].click()
    #高性能计算-共享型
    elif orderes[1][1] == "gg":
        #输入数量(核心时)
        casjc_log.logging.info(title + " 输入数量(核心时)")
        hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[0].clear()
        hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[0].send_keys("1")
        #有效期开始时间
        hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[1].click()
        casjc_log.logging.info(title + " 选择有效期开始时间")
        time.sleep(casjc_config.short_time)
        hailong.find_elements_by_css_selector('td[class="available today"]')[0].click()
        #有效期结束时间
        casjc_log.logging.info(title + " 选择有效期结束时间")
        hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[2].click()
        time.sleep(casjc_config.short_time)
        #2.3x需求已去掉试用类型的变更配置，下面功能正常只会执行try
        #如果是试用只能选择固定的天数，此处根据报错判断选择日期方式
        try:
            hailong.find_elements_by_css_selector('td[class="available today"]')[0].click()
        except exceptions.ElementNotInteractableException:
            aa = hailong.find_elements_by_xpath('//div[@class="el-picker-panel__content"]/table[@class="el-date-table"]/tbody/tr[@class="el-date-table__row"]/td[@class="available"]')
            aa[-1].click()
    #数据存储-文件存储
    elif orderes[1][1] == "sw":
        #输入数量(TB)
        num1 = "1"
        casjc_log.logging.info(title + " 输入数量(TB)")
        hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[0].clear()
        hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[0].send_keys(num1)
        #有效期开始时间
        hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[1].click()
        casjc_log.logging.info(title + " 选择有效期开始时间")
        time.sleep(casjc_config.short_time)
        hailong.find_elements_by_css_selector('td[class="available today"]')[0].click()
        #有效期结束时间
        casjc_log.logging.info(title + " 选择有效期结束时间")
        hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[2].click()
        time.sleep(casjc_config.short_time)
        #2.3x需求已去掉试用类型的变更配置，下面功能正常只会执行try
        #如果是试用只能选择固定的天数，此处根据报错判断选择日期方式
        try:
            hailong.find_elements_by_css_selector('td[class="available today"]')[0].click()
        except exceptions.ElementNotInteractableException:
            aa = hailong.find_elements_by_xpath('//div[@class="el-picker-panel__content"]/table[@class="el-date-table"]/tbody/tr[@class="el-date-table__row"]/td[@class="available"]')
            aa[-1].click()
    #数据存储-云硬盘
    elif orderes[1][1] == "sy":
        #选择集群
        casjc_log.logging.info(title + " 选择集群")
        hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[0].click()
        time.sleep(casjc_config.short_time)
        hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')[-2].click()
        time.sleep(casjc_config.short_time)
        #选择云硬盘
        casjc_log.logging.info(title + " 选择云硬盘")
        hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[1].click()
        time.sleep(casjc_config.short_time)
        try:
            hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')[-1].click()
        except:
            casjc_log.logging.info(title + " 没有找到云硬盘，退出操作")
            casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, "没有找到云硬盘"]
            aaa.Casjc_logout()
            return None
        #输入数量（TB）
        casjc_log.logging.info(title + " 输入数量(TB)")
        hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[2].clear()
        hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[2].send_keys("1")
        #输入数量（块）
        casjc_log.logging.info(title + " 输入数量(块)")
        hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[3].clear()
        hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[3].send_keys("1")
        #有效期开始时间
        hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[4].click()
        casjc_log.logging.info(title + " 选择有效期开始时间")
        time.sleep(casjc_config.short_time)
        hailong.find_elements_by_css_selector('td[class="available today"]')[0].click()
        time.sleep(casjc_config.short_time)
        #有效期结束时间
        casjc_log.logging.info(title + " 选择有效期结束时间")
        hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[5].click()
        time.sleep(casjc_config.short_time)
        #2.3x需求已去掉试用类型的变更配置，下面功能正常只会执行try
        #如果是试用只能选择固定的天数，此处根据报错判断选择日期方式
        try:
            hailong.find_elements_by_css_selector('td[class="available today"]')[0].click()
        except exceptions.ElementNotInteractableException:
            aa = hailong.find_elements_by_xpath('//div[@class="el-picker-panel__content"]/table[@class="el-date-table"]/tbody/tr[@class="el-date-table__row"]/td[@class="available"][1]')
            aa[-1].click()
    #网络资源-公网IP
    elif orderes[1][1] == "wg":
        #输入数量(个)
        casjc_log.logging.info(title + " 输入数量(个)")
        hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[0].clear()
        hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[0].send_keys("2")
        #有效期开始时间
        hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[1].click()
        casjc_log.logging.info(title + " 选择有效期开始时间")
        time.sleep(casjc_config.short_time)
        hailong.find_elements_by_css_selector('td[class="available today"]')[0].click()
        #有效期结束时间
        casjc_log.logging.info(title + " 选择有效期结束时间")
        hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[2].click()
        time.sleep(casjc_config.short_time)
        #2.3x需求已去掉试用类型的变更配置，下面功能正常只会执行try
        #如果是试用只能选择固定的天数，此处根据报错判断选择日期方式
        try:
            hailong.find_elements_by_css_selector('td[class="available today"]')[0].click()
        except exceptions.ElementNotInteractableException:
            aa = hailong.find_elements_by_xpath('//div[@class="el-picker-panel__content"]/table[@class="el-date-table"]/tbody/tr[@class="el-date-table__row"]/td[@class="available"]')
            aa[-1].click()
        
    #进入申请信息tab，获取订单号
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="details"]')))
    time.sleep(casjc_config.short_time)
    ordernum2 = hailong.find_elements_by_tag_name('p')[1].text
    casjc_log.logging.info(title + " 当前操作订单号，" + ordernum2)
    if ordernum != ordernum2[4:]:
        casjc_log.logging.info(title + " 预期变更或确认参数的订单号与实际操作的订单号不同,终止变更或确认")
        casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, "预期变更或确认参数的订单号与实际操作的订单号不同,终止变更或确认"]
        aaa.Casjc_logout()
        return None
    try:
        #点击确认参数
        casjc_log.logging.info(title + " 点击确认参数按钮")
        hailong.find_element_by_css_selector('button[class="el-button el-button--primary"]').click()
    except:
        imagename = title + time.strftime("%m%d%H%M%S") + '.png'
        hailong.save_screenshot(r'C:\usr\Apache24\htdocs\image\\' + imagename)
        casjc_log.logging.info(title + " 点击确认参数按钮异常，退出登录, 查看截图  %s" %imagename)
        casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, "订单号:" + ordernum + " 操作异常"]
        aaa.Casjc_logout()
        return None
    #判断是否弹出确认提示框,如果弹出点击确定按钮
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="el-message-box__message"]')))
    casjc_log.logging.info(title + " 点击确认提示框的确定按钮")
    hailong.find_elements_by_css_selector('button[class="el-button el-button--default el-button--small el-button--primary "]')[0].click()
    #获取提交请求返回信息
    aaa.admin_result(title,uname,ordernum)
    return 1


#配置资源
def Casjc_config(*myorderes):
    title = "配置资源"
    print(myorderes)
    orderes = myorderes[0]
    ordernum = orderes[0]
    casjc_log.logging.info(title + " 本次预期要操作的订单，" + ordernum)
    #登录，点击资源管理菜单
    hailong = webdriver.Chrome()
    uname = myconfig['user6']
    upasswd = myconfig['passwd2']
    uurl = myconfig['adminUrl']
    aaa = casjc_page.Casjc_admin_page(hailong,uname,upasswd,uurl)
    casjc_log.logging.info(title + " 进入资源管理菜单")
    aaa.admin_resmanagement()
    #进入配置资源页面
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'li[data-index="/configTable"]')))
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 进入配置资源页面")
    hailong.find_elements_by_css_selector('li[data-index="/configTable"]')[0].click()
    time.sleep(casjc_config.short_time)   
    try:
        #等待加载配置资源列表页面元素
        WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'thead[class="has-gutter"]')))
        time.sleep(casjc_config.short_time)
        WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'tr[class="el-table__row"]')))
        time.sleep(casjc_config.short_time)
        #获取第一页列表数据条数
        listnum = hailong.find_elements_by_css_selector('tr[class="el-table__row"]')
        casjc_log.logging.info(title + " 当前列表页数据条数: %s" % len(listnum))
        #如果条数0，退出
        if len(listnum) == 0:
            casjc_log.logging.info(title + " 没有待配置资源，退出登录")
            casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, "没有待配置资源"]
            aaa.Casjc_logout()
            return None
        mytmp = 0
        #循环遍历第一页列表是否有符合的订单号，如果有点击生成合同，没有退出
        for i in range(len(listnum)):
            if hailong.find_element_by_xpath('//tr[@class="el-table__row"][' + str(i+1) + ']/td/div[@class="cell el-tooltip"][1]').text == ordernum:
                casjc_log.logging.info(title + " 找到预期订单号，点击配置资源")
                try:
                    hailong.find_element_by_xpath('//tr[@class="el-table__row"][' + str(i+1) + ']/td/div[@class="cell"]/div[@class="table-btn"]/button[2]').click()
                    time.sleep(casjc_config.short_time)
                    mytmp = 1
                    break
                except:
                    casjc_log.logging.info(title + " 点击配置资源按钮异常，退出登录")
                    casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, "点击配置资源按钮异常，退出登录"]
                    aaa.Casjc_logout()
                    return None
        if mytmp == 0:
            casjc_log.logging.info(title + " 列表第一页没有找到符合的订单号")
            casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, "待审批列表第一页没有找到符合的订单号"]
            aaa.Casjc_logout()
            return None            
    except exceptions.TimeoutException:
        imagename = title + time.strftime("%m%d%H%M%S") + '.png'
        hailong.save_screenshot(r'C:\usr\Apache24\htdocs\image\\' + imagename)
        casjc_log.logging.info(title + " 配置资源列表页缺失元素，退出登录, 查看截图 %s" %imagename)
        casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, "配置资源列表页缺失元素"]
        aaa.Casjc_logout()
        return None    
    #点击产品服务下拉列表
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[1].click()
    time.sleep(casjc_config.short_time)
    #选择产品服务 -4:高性能计算 -3:云计算 -2:数据存储 -1:网络资源
    if orderes[1][1] == "gg" or orderes[1][1] == "gb":
        casjc_log.logging.info(title + " 选择产品服务-高性能计算")
        #选择高性能计算
        hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')[-4].click()
        #点击计算资源下拉列表
        casjc_log.logging.info(title + " 点击计算资源下拉列表")
        hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[2].click()
        time.sleep(casjc_config.short_time)
        #选择共享型
        casjc_log.logging.info(title + " 选择共享型")
        hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')[-1].click()
        #点击集群下拉列表
        casjc_log.logging.info(title + " 点击集群下拉列表")
        hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[3].click()
        time.sleep(casjc_config.short_time)
        #选择硅立方东侧
        casjc_log.logging.info(title + " 选择硅立方东侧")
        hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')[-1].click()
        #点击规格下拉列表
        casjc_log.logging.info(title + " 点击规格下拉列表")
        hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[4].click()
        time.sleep(casjc_config.short_time)
        #选择规格
        casjc_log.logging.info(title + " 选择规格")
        hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')[-1].click()
        #如果是试用类型,需要选择日期
        if str(orderes[1][0]) == "0":
            #试用类型没有提前配置日期，需要配置资源时选择日期
            #有效期开始时间
            hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[5].click()
            casjc_log.logging.info(title + " 选择有效期开始时间")
            time.sleep(casjc_config.short_time)
            hailong.find_elements_by_css_selector('td[class="available today"]')[0].click()
            #有效期结束时间
            casjc_log.logging.info(title + " 选择有效期结束时间")
            hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[6].click()
            time.sleep(casjc_config.short_time)
            try:
                hailong.find_elements_by_css_selector('td[class="available today"]')[0].click()
            except exceptions.ElementNotInteractableException:
                aa = hailong.find_elements_by_xpath('//div[@class="el-picker-panel__content"]/table[@class="el-date-table"]/tbody/tr[@class="el-date-table__row"]/td[@class="available"]')
                aa[-1].click()    
        #选择队列
        WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.ID, 'low')))
        hailong.find_element_by_id('low').click()
    elif orderes[1][1] == "yy":
        casjc_log.logging.info(title + " 选择产品服务-云计算")
        #选择云计算
        hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')[-3].click()
        #点击计算资源下拉列表
        casjc_log.logging.info(title + " 点击计算资源下拉列表")
        hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[2].click()
        time.sleep(casjc_config.short_time)
        #选择云主机
        casjc_log.logging.info(title + " 选择云主机")
        hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')[-1].click()
        #如果是试用类型,需要选择日期
        if str(orderes[1][0]) == "0":
            #选择集群
            casjc_log.logging.info(title + " 选择集群")
            hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[3].click()
            time.sleep(casjc_config.short_time)
            hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')[-2].click()
            time.sleep(casjc_config.short_time)
            #选择云主机规格
            casjc_log.logging.info(title + " 选择云主机规格")
            hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[4].click()
            time.sleep(casjc_config.short_time)
            try:
                hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')[-1].click()
            except:
                casjc_log.logging.info(title + " 没有找到云主机规格，退出操作")
                casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, "没有找到云主机规格"]
                aaa.Casjc_logout()
                return None
            #输入数量（台）
            casjc_log.logging.info(title + " 输入数量(台)")
            hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[5].clear()
            hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[5].send_keys("1")
            #有效期开始时间
            hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[6].click()
            casjc_log.logging.info(title + " 选择有效期开始时间")
            time.sleep(casjc_config.short_time)
            hailong.find_elements_by_css_selector('td[class="available today"]')[0].click()
            time.sleep(casjc_config.short_time)
            #有效期结束时间
            casjc_log.logging.info(title + " 选择有效期结束时间")
            hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[7].click()
            time.sleep(casjc_config.short_time)
            try:
                hailong.find_elements_by_css_selector('td[class="available today"]')[0].click()
            except exceptions.ElementNotInteractableException:
                aa = hailong.find_elements_by_xpath('//div[@class="el-picker-panel__content"]/table[@class="el-date-table"]/tbody/tr[@class="el-date-table__row"]/td[@class="available"]')
                aa[-1].click()
    elif orderes[1][1] == "sw":
        casjc_log.logging.info(title + " 选择产品服务-数据存储")
        #选择数据存储
        hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')[-2].click()
        #点击计算资源下拉列表
        casjc_log.logging.info(title + " 点击计算资源下拉列表")
        hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[2].click()
        time.sleep(casjc_config.short_time)
        #选择文件存储
        casjc_log.logging.info(title + " 选择文件存储")
        hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')[-2].click()
        #点击集群下拉列表
        casjc_log.logging.info(title + " 点击集群下拉列表")
        hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[3].click()
        time.sleep(casjc_config.short_time)
        #选择GPFS集群测试环境
        casjc_log.logging.info(title + " 选择GPFS集群测试环境")
        hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')[-1].click()
        #点击规格下拉列表
        casjc_log.logging.info(title + " 点击规格下拉列表")
        hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[4].click()
        time.sleep(casjc_config.short_time)
        #选择规格
        casjc_log.logging.info(title + " 选择规格")
        hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')[-1].click()
        #如果是试用类型,需要选择日期
        if str(orderes[1][0]) == "0": 
            #试用类型没有提前配置日期，需要配置资源时选择日期
            #有效期开始时间
            hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[5].click()
            casjc_log.logging.info(title + " 选择有效期开始时间")
            time.sleep(casjc_config.short_time)
            hailong.find_elements_by_css_selector('td[class="available today"]')[0].click()
            #有效期结束时间,26版本呢用类型存储自动计算结束日期不用再选
            '''
            casjc_log.logging.info(title + " 选择有效期结束时间")
            hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[6].click()
            time.sleep(casjc_config.short_time)
            try:
                hailong.find_elements_by_css_selector('td[class="available today"]')[0].click()
            except exceptions.ElementNotInteractableException:
                aa = hailong.find_elements_by_xpath('//div[@class="el-picker-panel__content"]/table[@class="el-date-table"]/tbody/tr[@class="el-date-table__row"]/td[@class="available"]')
                aa[-1].click()
            '''
        #casjc_log.logging.info(title + " 输入家目录")
        #hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[7].send_keys('/public1/home/test/test')
        #time.sleep(casjc_config.short_time)
    elif orderes[1][1] == "sy":
        casjc_log.logging.info(title + " 选择产品服务-数据存储")
        #选择数据存储
        hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')[-2].click()
        #点击计算资源下拉列表
        casjc_log.logging.info(title + " 点击计算资源下拉列表")
        hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[2].click()
        time.sleep(casjc_config.short_time)
        #选择云硬盘
        casjc_log.logging.info(title + " 选择云硬盘")
        hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')[-1].click()
        #如果是试用类型,需要选择日期
        if str(orderes[1][0]) == "0":
            #选择集群
            casjc_log.logging.info(title + " 选择集群")
            hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[3].click()
            time.sleep(casjc_config.short_time)
            hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')[-2].click()
            time.sleep(casjc_config.short_time)
            #选择云硬盘类型
            casjc_log.logging.info(title + " 选择云硬盘类型")
            hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[4].click()
            time.sleep(casjc_config.short_time)
            try:
                hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')[-1].click()
            except:
                casjc_log.logging.info(title + " 没有找到云硬盘，退出操作")
                casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, "没有找到云硬盘"]
                aaa.Casjc_logout()
                return None
            #输入数量（TB）
            casjc_log.logging.info(title + " 输入数量(TB)")
            hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[5].clear()
            hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[5].send_keys("1")
            #输入数量（块）
            casjc_log.logging.info(title + " 输入数量(块)")
            hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[6].clear()
            hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[6].send_keys("1")
            #有效期开始时间
            hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[7].click()
            casjc_log.logging.info(title + " 选择有效期开始时间")
            time.sleep(casjc_config.short_time)
            hailong.find_elements_by_css_selector('td[class="available today"]')[0].click()
            time.sleep(casjc_config.short_time)
            #有效期结束时间
            casjc_log.logging.info(title + " 选择有效期结束时间")
            hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[8].click()
            time.sleep(casjc_config.short_time)
            try:
                hailong.find_elements_by_css_selector('td[class="available today"]')[0].click()
            except exceptions.ElementNotInteractableException:
                aa = hailong.find_elements_by_xpath('//div[@class="el-picker-panel__content"]/table[@class="el-date-table"]/tbody/tr[@class="el-date-table__row"]/td[@class="available"]')
                aa[-1].click()
    elif orderes[1][1] == "wg":
        #选择网络资源
        casjc_log.logging.info(title + " 选择产品服务-网络资源")
        hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')[-1].click()
        #点击计算资源下拉列表
        casjc_log.logging.info(title + " 点击计算资源下拉列表")
        hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[2].click()
        time.sleep(casjc_config.short_time)
        #选择公网IP
        casjc_log.logging.info(title + " 选择公网IP")
        hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')[-1].click()
        #点击规格下拉列表
        casjc_log.logging.info(title + " 点击规格下拉列表")
        hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[3].click()
        time.sleep(casjc_config.short_time)
        #选择规格
        casjc_log.logging.info(title + " 选择规格")
        hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')[-1].click()
        #如果是试用类型,需要选择日期
        if str(orderes[1][0]) == "0":
            #试用类型没有提前配置日期，需要配置资源时选择日期
            #有效期开始时间
            hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[4].click()
            casjc_log.logging.info(title + " 选择有效期开始时间")
            time.sleep(casjc_config.short_time)
            hailong.find_elements_by_css_selector('td[class="available today"]')[0].click()
            #有效期结束时间
            casjc_log.logging.info(title + " 选择有效期结束时间")
            hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[5].click()
            time.sleep(casjc_config.short_time)
            try:
                hailong.find_elements_by_css_selector('td[class="available today"]')[0].click()
            except exceptions.ElementNotInteractableException:
                aa = hailong.find_elements_by_xpath('//div[@class="el-picker-panel__content"]/table[@class="el-date-table"]/tbody/tr[@class="el-date-table__row"]/td[@class="available"]')
                aa[-1].click()
        #选择有效期开始日期
        #casjc_log.logging.info(title + " 选择有效期开始日期")
        #hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[4].click()
        #time.sleep(casjc_config.short_time)
        #hailong.find_elements_by_css_selector('td[class="available today"]')[0].click()
        #选择有效期结束日期
        #casjc_log.logging.info(title + " 选择有效期结束日期")
        #hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[5].click()
        #time.sleep(casjc_config.short_time)
        #hailong.find_elements_by_css_selector('td[class="available today"]')[0].click()
        #aa = hailong.find_elements_by_xpath('//tr[@class="el-date-table__row"]/td[@class="available"]/div/span')
        #print(aa[int(len(aa)/2)].text)
        #aa[int(len(aa)/2)].click()
        time.sleep(casjc_config.short_time)
    
    #进入申请信息tab，获取订单号
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="details"]')))
    time.sleep(casjc_config.short_time)
    ordernum2 = hailong.find_elements_by_tag_name('p')[1].text
    casjc_log.logging.info(title + " 当前操作订单号，" + ordernum)
    if ordernum != ordernum2[4:]:
        casjc_log.logging.info(title + " 预期配置资源的订单号与实际操作的订单号不同,终止配置资源")
        casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, "预期配置资源的订单号与实际操作的订单号不同,终止配置资源"]
        aaa.Casjc_logout()
        return None
    try:
        #点击确认配置
        casjc_log.logging.info(title + " 点击确认配置")
        hailong.find_element_by_css_selector('button[class="el-button el-button--primary"]').click()
    except:
        imagename = title + time.strftime("%m%d%H%M%S") + '.png'
        hailong.save_screenshot(r'C:\usr\Apache24\htdocs\image\\' + imagename)
        casjc_log.logging.info(title + " 点击确认参数按钮异常,查看截图 %s " %imagename)
        casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, " 订单号:" + ordernum + " 操作异常"]
        aaa.Casjc_logout()
        return None
    #判断是否弹出确认提示框,如果弹出点击确定按钮
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="el-message-box__message"]')))
    casjc_log.logging.info(title + " 点击弹出的确认提示框，确定按钮")
    hailong.find_elements_by_css_selector('button[class="el-button el-button--default el-button--small el-button--primary "]')[0].click()
    #获取提交请求返回信息
    aaa.admin_result(title,uname,ordernum)
    return None



#创建内部网络
def Casjc_vlan():
    title = "创建内部网络"
    #登录，点击资源管理菜单
    hailong = webdriver.Chrome()
    uname = myconfig['user1']
    upasswd = myconfig['passwd1']
    uurl = myconfig['adminUrl']
    aaa = casjc_page.Casjc_admin_page(hailong,uname,upasswd,uurl)
    casjc_log.logging.info(title + " 进入资源管理菜单")
    aaa.admin_resmanagement()
    #进入配置资源页面
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'i[class="el-icon- iconfont iconwangluoziyuan"]')))
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 进入内部网络页面")
    hailong.find_elements_by_css_selector('i[class="el-icon- iconfont iconwangluoziyuan"]')[0].click()
    time.sleep(casjc_config.short_time)
    hailong.find_elements_by_css_selector('li[data-index="/intranet"]')[0].click()
    #点击新建网络按钮
    casjc_log.logging.info(title + " 点击新建网络按钮")
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'button[class="el-button el-button--primary el-button--small"]')))
    hailong.find_elements_by_css_selector('button[class="el-button el-button--primary el-button--small"]')[0].click()
    time.sleep(casjc_config.short_time)
    #填写内部网络信息
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[0].send_keys("国科内部vlan1098")
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[1].send_keys("vlan1098")
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[2].send_keys("10.8.98.1")
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[3].send_keys("10.8.98.1/24")
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[4].send_keys("255.255.255.0")
    #点击保存按钮
    casjc_log.logging.info(title + " 点击保存按钮")
    hailong.find_elements_by_css_selector('button[class="el-button el-button--primary el-button--small"')[-2].click()
    #获取提交请求返回信息
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="el-message-box__message"]')))
    res = hailong.find_elements_by_css_selector('div[class="el-message-box__message"]')[0].text
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'button[class="el-button el-button--default el-button--small el-button--primary "]')))
    hailong.find_element_by_css_selector('button[class="el-button el-button--default el-button--small el-button--primary "]').click()
    aaa.admin_result(title,uname,res)
    return None


#修改网络名称
def Casjc_vlanname():
    title = "修改网络名称"
    #登录，点击资源管理菜单
    hailong = webdriver.Chrome()
    uname = myconfig['user1']
    upasswd = myconfig['passwd1']
    uurl = myconfig['adminUrl']
    aaa = casjc_page.Casjc_admin_page(hailong,uname,upasswd,uurl)
    casjc_log.logging.info(title + " 进入资源管理菜单")
    aaa.admin_resmanagement()
    #进入配置资源页面
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'i[class="el-icon- iconfont iconwangluoziyuan"]')))
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 进入内部网络页面")
    hailong.find_elements_by_css_selector('i[class="el-icon- iconfont iconwangluoziyuan"]')[0].click()
    time.sleep(casjc_config.short_time)
    hailong.find_elements_by_css_selector('li[data-index="/intranet"]')[0].click()
    time.sleep(casjc_config.show_time)
    #判断列表第一条是不是要修改的网络
    #for i in hailong.find_elements_by_css_selector('tr[class="el-table__row"]'):
    #    print(i.text)
    #for i in hailong.find_elements_by_xpath('//tr[@class="el-table__row"]/td[2]/div[@class="cell"]'):
    #    print(i.text)
    if hailong.find_elements_by_xpath('//tr[@class="el-table__row"]/td[2]/div[@class="cell"]')[0].text == "vlan1098":
    #if hailong.find_elements_by_css_selector('div[class="cell"]')[7].text == "vlan1098":
        #点击修改网络名称按钮
        casjc_log.logging.info(title + " 点击修改名称按钮")
        WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'button[class="el-button el-button--text el-button--mini"]')))
        hailong.find_elements_by_css_selector('button[class="el-button el-button--text el-button--mini"]')[0].click()
        time.sleep(casjc_config.short_time)
        #填写内部网络名称
        hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[-1].send_keys("国科内部vlan1098-1_1")
        #点击保存按钮
        casjc_log.logging.info(title + " 点击保存按钮")
        hailong.find_elements_by_css_selector('button[class="el-button el-button--primary"]')[-1].click()
        #获取提交请求返回信息
        aaa.admin_result(title,uname)
        return None
    #获取提交返回结果
    casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, " 操作异常,第一条不是要修改的网络"]
    hailong.quit()
    return None


#删除列表第一条内部网络
def Casjc_vlandel():
    title = "删除列表第一条内部网络"
    #登录，点击资源管理菜单
    hailong = webdriver.Chrome()
    uname = myconfig['user1']
    upasswd = myconfig['passwd1']
    uurl = myconfig['adminUrl']
    aaa = casjc_page.Casjc_admin_page(hailong,uname,upasswd,uurl)
    casjc_log.logging.info(title + " 进入资源管理菜单")
    aaa.admin_resmanagement()
    #进入配置资源页面
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'i[class="el-icon- iconfont iconwangluoziyuan"]')))
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 进入内部网络页面")
    hailong.find_elements_by_css_selector('i[class="el-icon- iconfont iconwangluoziyuan"]')[0].click()
    time.sleep(casjc_config.short_time)
    hailong.find_elements_by_css_selector('li[data-index="/intranet"]')[0].click()
    #点击删除按钮
    casjc_log.logging.info(title + " 点击删除按钮")
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'button[class="el-button el-button--text el-button--mini"]')))
    time.sleep(casjc_config.show_time)
    hailong.find_elements_by_css_selector('button[class="el-button el-button--text el-button--mini"]')[1].click()
    time.sleep(casjc_config.short_time)
    #判断是否弹出确认提示框,如果弹出点击确定按钮
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="el-message-box__message"]')))
    casjc_log.logging.info(title + " 点击弹出的确认提示框，确定按钮")
    hailong.find_elements_by_css_selector('button[class="el-button el-button--default el-button--small el-button--primary "]')[0].click()
    #获取提交请求返回信息
    aaa.admin_result(title,uname)
    return None



#创建公网网络
def Casjc_publicvlan():
    title = "创建公网网络"
    #登录，点击资源管理菜单
    hailong = webdriver.Chrome()
    uname = myconfig['user1']
    upasswd = myconfig['passwd1']
    uurl = myconfig['adminUrl']
    aaa = casjc_page.Casjc_admin_page(hailong,uname,upasswd,uurl)
    casjc_log.logging.info(title + " 进入资源管理菜单")
    aaa.admin_resmanagement()
    #进入配置资源页面
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'i[class="el-icon- iconfont iconwangluoziyuan"]')))
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 进入公网IP页面")
    hailong.find_elements_by_css_selector('i[class="el-icon- iconfont iconwangluoziyuan"]')[0].click()
    time.sleep(casjc_config.short_time)
    hailong.find_elements_by_css_selector('li[data-index="/Enetwork"]')[0].click()
    #点击新建网络按钮
    casjc_log.logging.info(title + " 点击新建公网IP按钮")
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'button[class="el-button el-button--primary el-button--small"]')))
    hailong.find_elements_by_css_selector('button[class="el-button el-button--primary el-button--small"]')[0].click()
    time.sleep(casjc_config.short_time)
    #填写公网网络信息
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[3].send_keys("127.0.0.5")
    time.sleep(casjc_config.short_time)
    #点击保存按钮
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'button[class="el-button el-button--primary"]')))
    casjc_log.logging.info(title + " 点击保存按钮")
    try:
        hailong.find_elements_by_css_selector('button[class="el-button el-button--primary"]')[-1].click()
        time.sleep(casjc_config.short_time)
        hailong.find_elements_by_css_selector('button[class="el-button el-button--primary"]')[-1].click()
        time.sleep(casjc_config.short_time)
        hailong.find_elements_by_css_selector('button[class="el-button el-button--primary"]')[-1].click()
    except:
        pass
    #获取提交请求返回信息
    aaa.admin_result(title,uname)
    return None


#删除公网网络
def Casjc_publicvlandel():
    title = "删除公网网络"
    #登录，点击资源管理菜单
    hailong = webdriver.Chrome()
    uname = myconfig['user1']
    upasswd = myconfig['passwd1']
    uurl = myconfig['adminUrl']
    aaa = casjc_page.Casjc_admin_page(hailong,uname,upasswd,uurl)
    casjc_log.logging.info(title + " 进入资源管理菜单")
    aaa.admin_resmanagement()
    #进入配置资源页面
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'i[class="el-icon- iconfont iconwangluoziyuan"]')))
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 进入公网IP页面")
    hailong.find_elements_by_css_selector('i[class="el-icon- iconfont iconwangluoziyuan"]')[0].click()
    time.sleep(casjc_config.short_time)
    hailong.find_elements_by_css_selector('li[data-index="/Enetwork"]')[0].click()
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="table-btn"]')))
    time.sleep(casjc_config.short_time)
    #点击删除网络按钮
    if hailong.find_elements_by_css_selector('div[class="cell el-tooltip"]')[0].text == "127.0.0.5":
        casjc_log.logging.info(title + " 点击删除公网IP按钮")
        hailong.find_elements_by_css_selector('div[class="table-btn"]')[0].click()
        time.sleep(casjc_config.short_time)
        #判断是否弹出确认提示框,如果弹出点击确定按钮
        WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="el-message-box__message"]')))
        casjc_log.logging.info(title + " 点击弹出的确认提示框，确定按钮")
        hailong.find_elements_by_css_selector('button[class="el-button el-button--default el-button--small el-button--primary "]')[0].click()
        #获取提交请求返回信息
        aaa.admin_result(title,uname)
        return None
    #获取提交返回结果
    casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, " 操作异常,第一条不是要删除的网络"]
    hailong.quit()
    return None


#申请合同作废
def Casjc_contract_void(contractnum):
    title = "申请合同作废"
    #登录，点击运营中心菜单
    uname = myconfig['user1']
    upasswd = myconfig['passwd1']
    uurl = myconfig['adminUrl']
    hailong = webdriver.Chrome()
    aaa = casjc_page.Casjc_admin_page(hailong,uname,upasswd,uurl)
    casjc_log.logging.info(title + " 进入运营中心菜单")
    aaa.admin_operationcenter()
    #进入全部合同菜单
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'i[class="el-icon- iconfont iconhetongguanli-"]')))
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 进入全部合同菜单")
    hailong.find_element_by_css_selector('i[class="el-icon- iconfont iconhetongguanli-"]').click()
    time.sleep(casjc_config.short_time)
    hailong.find_element_by_css_selector('li[data-index="/contractManagemen"]').click()
    #等待页面元素(全部合同列表)
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="el-card__body"]')))
    time.sleep(casjc_config.short_time)
    #搜索合同号
    hailong.find_elements_by_css_selector('i[class="el-icon-arrow-down el-icon--right"]')[0].click()
    time.sleep(casjc_config.short_time)
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[4].send_keys(contractnum)
    hailong.find_elements_by_css_selector('button[class="el-button el-button--primary el-button--small"]')[0].click()
    try:
        WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'tr[class="el-table__row"]')))
    except exceptions.TimeoutException:
        casjc_log.logging.info(title + " 没有找到预期的合同号," + contractnum)
        casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, " 没有找到预期的合同号," + contractnum]
        aaa.Casjc_logout()
        return None
    #点击更多按钮
    hailong.find_elements_by_xpath('//tr[@class="el-table__row"]/td/div[@class="cell"]/div/span/span')[0].click()
    time.sleep(casjc_config.short_time)
    #点击作废重签按钮
    hailong.find_elements_by_xpath('//ul[@class="more"]/li/span')[1].click()
    #等待页面元素(申请作废重签)
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="agreementTwo"]')))
    #点击上传按钮(作废协议)
    casjc_log.logging.info(title + " 点击上传文件按钮")
    hailong.find_elements_by_css_selector('button[class="el-button el-button--primary el-button--small"]')[0].click()
    time.sleep(casjc_config.short_time)
    #上传文件
    casjc_mode.Casjc_upload(casjc_config.uppath)
    time.sleep(casjc_config.short_time)
    #点击上传按钮(新合同)
    casjc_log.logging.info(title + " 点击上传文件按钮")
    hailong.find_elements_by_css_selector('button[class="el-button el-button--primary el-button--small"]')[1].click()
    time.sleep(casjc_config.short_time)
    #上传文件
    casjc_mode.Casjc_upload(casjc_config.uppath)
    time.sleep(casjc_config.short_time)
    #勾选合同确认信息复选框
    hailong.find_element_by_css_selector('span[class="el-checkbox__inner"]').click()
    #输入合同作废重签原因
    hailong.find_element_by_css_selector('textarea[class="el-textarea__inner"]').send_keys("合同作废重签提交")
    #点击确认按钮
    time.sleep(casjc_config.short_time)
    hailong.find_element_by_css_selector('button[class="el-button el-button--primary"]').click()
    #获取提交请求返回信息
    aaa.admin_result(title,uname,contractnum)
    return None


#合同作废审批
def Casjc_contract_tovoid(contractnum,username):
    title = "合同作废"
    #登录，点击运营中心菜单
    uname = username
    upasswd = myconfig['passwd2']
    uurl = myconfig['adminUrl']
    hailong = webdriver.Chrome()
    aaa = casjc_page.Casjc_admin_page(hailong,uname,upasswd,uurl)
    casjc_log.logging.info(title + " 进入运营中心菜单")
    aaa.admin_operationcenter()
    #进入全部合同菜单
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'i[class="el-icon- iconfont iconhetongguanli-"]')))
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 进入全部合同菜单")
    hailong.find_element_by_css_selector('i[class="el-icon- iconfont iconhetongguanli-"]').click()
    time.sleep(casjc_config.short_time)
    hailong.find_element_by_css_selector('li[data-index="/pendingContract"]').click()
    #等待页面元素(全部合同列表)
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="el-card__body"]')))
    time.sleep(casjc_config.short_time)
    #搜索合同号
    hailong.find_elements_by_css_selector('i[class="el-icon-arrow-down el-icon--right"]')[0].click()
    time.sleep(casjc_config.short_time)
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[4].send_keys(contractnum)
    hailong.find_elements_by_css_selector('button[class="el-button el-button--primary el-button--small"]')[0].click()
    try:
        WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'tr[class="el-table__row"]')))
    except exceptions.TimeoutException:
        casjc_log.logging.info(title + " 没有找到预期的合同号," + contractnum)
        casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, " 没有找到预期的合同号," + contractnum]
        aaa.Casjc_logout()
        return None
    #点击更多按钮
    hailong.find_elements_by_xpath('//tr[@class="el-table__row"]/td/div[@class="cell"]/div/span/span')[0].click()
    time.sleep(casjc_config.short_time)
    #点击作废审批按钮
    hailong.find_elements_by_xpath('//ul[@class="more"]/li/span')[0].click()
    #等待页面元素(作废重签审批)
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="el-radio-group"]')))
    #勾选合同确认信息复选框
    hailong.find_element_by_css_selector('span[class="el-checkbox__inner"]').click()
    #输入合同作废重签原因
    hailong.find_element_by_css_selector('textarea[class="el-textarea__inner"]').send_keys("合同作废重签审批，" + username)
    #查看合同信息
    hailong.find_elements_by_css_selector('span[class="el-radio-button__inner"]')[1].click()
    #等待页面元素(作废重签审批)
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="stepThree"]')))
    time.sleep(casjc_config.short_time)
    #获取当前合同号
    contractn = hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[3].get_attribute("title")
    casjc_log.logging.info(title + " 当前审批的合同号为：" + contractn)
    #点击确定按钮
    hailong.find_element_by_css_selector('button[class="el-button el-button--primary"]').click()
    #获取提交请求返回信息
    aaa.admin_result(title,uname,contractnum)
    return None
    


#新建企业单位
def Casjc_create_ent():
    title = "新增企业单位"
    #登录，点击运营中心菜单
    uname = myconfig['user1']
    upasswd = myconfig['passwd1']
    uurl = myconfig['adminUrl']
    hailong = webdriver.Chrome()
    aaa = casjc_page.Casjc_admin_page(hailong,uname,upasswd,uurl)
    casjc_log.logging.info(title + " 进入运营中心菜单")
    aaa.admin_operationcenter()
    #进入企业管理菜单
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'i[class="el-icon- iconfont iconicongl"]')))
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 进入企业管理菜单")
    hailong.find_element_by_css_selector('i[class="el-icon- iconfont iconicongl"]').click()
    time.sleep(casjc_config.short_time)
    #点击新增企业单位按钮
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="el-row"]')))
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 点击新增企业单位按钮")
    hailong.find_elements_by_css_selector('div[class="el-row"]')[0].click()
    time.sleep(casjc_config.short_time)
    #等待新增弹窗元素
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'span[class="el-radio-button__inner"]')))   
    #输入企业单位名称
    newuser = "ui_企业名称" + time.strftime("%m%d%H%M",time.localtime())
    casjc_log.logging.info(title + " 输入企业单位名称，" + newuser)
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[0].send_keys(newuser)
    #选择省
    #hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[5].send_keys(u"自动化管理用户")
    #选择市
    #hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[6].send_keys(str(random.randint(10000,99999)) + "@qq.com")
    #选择区
    #hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[7].send_keys("131" + time.strftime("%m%d%H%M",time.localtime()))
    #点击保存按钮
    casjc_log.logging.info(title + " 点击保存按钮")
    hailong.find_element_by_css_selector('button[class="el-button el-button--primary"]').click()
    #获取提交请求返回信息
    aaa.admin_result(title,uname,newuser)
    return None

#编辑企业单位
def Casjc_edit_ent():
    title = "编辑企业单位"
    #登录，点击运营中心菜单
    uname = myconfig['user1']
    upasswd = myconfig['passwd1']
    uurl = myconfig['adminUrl']
    hailong = webdriver.Chrome()
    aaa = casjc_page.Casjc_admin_page(hailong,uname,upasswd,uurl)
    casjc_log.logging.info(title + " 进入运营中心菜单")
    aaa.admin_operationcenter()
    #进入企业管理菜单
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'i[class="el-icon- iconfont iconicongl"]')))
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 进入企业管理菜单")
    hailong.find_element_by_css_selector('i[class="el-icon- iconfont iconicongl"]').click()
    time.sleep(casjc_config.short_time)
    #点击编辑企业单位按钮
    try:
        WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'button[class="el-button el-button--text el-button--mini"]')))
        time.sleep(casjc_config.short_time)
        casjc_log.logging.info(title + " 点击编辑企业单位按钮")
        hailong.find_elements_by_css_selector('button[class="el-button el-button--text el-button--mini"]')[1].click()
    except exceptions.TimeoutException:
        imagename = title + time.strftime("%m%d%H%M%S") + '.png'
        hailong.save_screenshot(r'C:\usr\Apache24\htdocs\image\\' + imagename)
        casjc_log.logging.info(title + " 点击编辑企业单位按钮异常,退出登录, 查看截图 %s" %imagename)
        casjc_config.casjc_result['编辑企业单位'] = [uname, "操作异常,没有找到编辑按钮"]
        aaa.Casjc_logout()
        return None
    #判断打开新增弹窗成功
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="el-card__body"]')))
    time.sleep(casjc_config.short_time)
    if hailong.find_element_by_css_selector('span[class="el-radio-button__inner"]').text == "基础信息":
        casjc_log.logging.info(title + " 编辑弹窗打开成功" )      
    #输入企业单位名称
    newuser = hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[0].get_attribute('value')
    #选择省
    #hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[5].send_keys(u"自动化管理用户")
    #选择市
    #hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[6].send_keys(str(random.randint(10000,99999)) + "@qq.com")
    #选择区
    #hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[7].send_keys("131" + time.strftime("%m%d%H%M",time.localtime()))
    #点击保存按钮
    casjc_log.logging.info(title + " 点击保存按钮")
    hailong.find_element_by_css_selector('button[class="el-button el-button--primary"]').click()
    #获取提交请求返回信息
    try:
        WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="el-row"]')))
        casjc_log.logging.info(title + " 编辑成功")
        casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, newuser + " 编辑成功"]
        aaa.Casjc_logout()
        return None
    except exceptions.TimeoutException:
        imagename = title + time.strftime("%m%d%H%M%S") + '.png'
        hailong.save_screenshot(r'C:\usr\Apache24\htdocs\image\\' + imagename)
        casjc_log.logging.info(title + " 页面元素未找到，编辑异常，退出登录, 查看截图 %s" %imagename)
        casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, "操作异常"]
        aaa.Casjc_logout()
        return None


#费用管理-新增计费
def Casjc_addCost(*res):
    '''
    srt = (6,-1)#高性能计算-共享
    srt = (6,-2)#高性能计算-标准
    srt = (8,-1)#数据存储-数据存储
    srt = (9,-1)#网络资源-网络资源
    '''
    title = "新增计费"
    if not res:
        casjc_log.logging.info(title + " 没有传递res参数,终止执行")
        casjc_config.casjc_result[title + time.strftime("%M%S")] = ["", "没有传递res参数，退出登录"]
        return None
    #登录，点击运营中心菜单
    uname = myconfig['user1']
    upasswd = myconfig['passwd1']
    uurl = myconfig['adminUrl']
    hailong = webdriver.Chrome()
    aaa = casjc_page.Casjc_admin_page(hailong,uname,upasswd,uurl)
    casjc_log.logging.info(title + " 进入运营中心菜单")
    aaa.admin_operationcenter()
    #进入费用管理菜单
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'li[data-index="/costList"]')))
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 进入费用管理菜单")
    hailong.find_element_by_css_selector('li[data-index="/costList"]').click()
    time.sleep(casjc_config.short_time)
    #点击新增计费按钮
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="list-header"]')))
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 点击新增计费按钮")
    hailong.find_elements_by_css_selector('button[class="el-button el-button--primary el-button--small"]')[0].click()
    #进入新增计费页面
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="el-card__body"]')))
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'input[class="el-input__inner"]')))
    time.sleep(casjc_config.short_time)
    #选择产品服务
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[0].click()
    time.sleep(casjc_config.short_time)
    if 1:
        #获取产品服务
        print(res[0][0])
        ss = hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')[res[0][0]].text
        casjc_log.logging.info(title + " 选择产品服务," + ss)
        hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')[res[0][0]].click()
        #选择资源类型,-1共享型
        hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[1].click()
        time.sleep(casjc_config.short_time)
        #获取资源类型
        tt = hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')[res[0][1]].text
        casjc_log.logging.info(title + " 选择资源类型," + tt)
        hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')[res[0][1]].click()
        #输入计算资源名称
        casjc_log.logging.info(title + " 输入计算资源名称")
        restitle = "资源名称" + time.strftime("%H%M%S")
        hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[2].send_keys(restitle)        
        casjc_log.logging.info(title + " 产品服务: " + ss + " -- 资源类型: " + tt + " 输入资源名称," + restitle)
        #输入技术规格
        if res[0][0] == 4 or res[0][0] == 6 or res[0][0] ==7:
            casjc_log.logging.info(title + " 输入技术规格")
            hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[3].send_keys("2*Rome 7742 64c 2.25GHz/512GB DDR4/960G SSD/100Gb EDR-规格参数")
        elif res[0][0] == 5:
            hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[3].click()
            time.sleep(casjc_config.short_time)
            casjc_log.logging.info(title + " 选择技术规格")
            hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')[-1].click()
        #选择服务区
        if res[0][0] != 7:    
            hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[4].click()
            time.sleep(casjc_config.short_time)
            casjc_log.logging.info(title + " 选择服务区," + hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')[-4].text)
            hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')[-4].click()
        #如果是高性能计算-标准型,输入节点范围
        if int(res[0][1]) == -2 or int(res[0][0]) == 8 or int(res[0][0]) == 9:
            casjc_log.logging.info(title + " 选择集群")
            hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[6].send_keys("test")
            hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[7].send_keys("100")
            hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[8].send_keys("120")
        #选择计价单位
        #hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[-1].click()
        #time.sleep(casjc_config.short_time)
        #casjc_log.logging.info(title + " 选择计价单位," + hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')[-1].text)
        #hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')[-1].click()
        #选择计价周期
        #hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[-2].click()
        #time.sleep(casjc_config.short_time)
        #casjc_log.logging.info(title + " 选择计价周期," + hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')[-1].text)
        #hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')[-1].click()
        #输入单价
        price = "100"
        casjc_log.logging.info(title + " 输入单价," + price)
        hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[-1].send_keys(price)
    hailong.find_element_by_css_selector('button[class="el-button el-button--primary el-button--small"]').click()
    #获取提交请求返回信息
    aaa.admin_result(title,uname," 产品服务: " + ss + " -- 资源类型: " + tt + " -- 资源名称: " + restitle)
    return restitle

#费用管理-编辑计费
def Casjc_editCost(cname=""):
    title = "编辑计费"
    if not cname:
        casjc_log.logging.info(title + " 没有传递cname参数,计费管理的资源名称")
        casjc_config.casjc_result[title + time.strftime("%M%S")] = ["", "没有给予资源名称，退出登录"]
        return None      
    #登录，点击运营中心菜单
    uname = myconfig['user1']
    upasswd = myconfig['passwd1']
    uurl = myconfig['adminUrl']
    hailong = webdriver.Chrome()
    aaa = casjc_page.Casjc_admin_page(hailong,uname,upasswd,uurl)
    casjc_log.logging.info(title + " 进入运营中心菜单")
    aaa.admin_operationcenter()
    #进入费用管理菜单
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'li[data-index="/costList"]')))
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 进入费用管理菜单")
    hailong.find_element_by_css_selector('li[data-index="/costList"]').click()
    time.sleep(casjc_config.short_time)
    #获取费用管理列表页有多少条数据
    try:
        WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'span[class="el-pagination__total"]')))
    except exceptions.TimeoutException:
        imagename = title + time.strftime("%m%d%H%M%S") + '.png'
        hailong.save_screenshot(r'C:\usr\Apache24\htdocs\image\\' + imagename)
        casjc_log.logging.info(title + " 页面元素未找到，或费用管理列表没有数据，退出登录, 查看截图 %s" %imagename)
        casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, "操作异常"]
        aaa.Casjc_logout()
        return None
    totalnum = hailong.find_element_by_css_selector('span[class="el-pagination__total"]').text
    casjc_log.logging.info(title + " 费用管理列表数据条数，" + totalnum)
    #进入费用管理列表最后一页
    casjc_log.logging.info(title + " 进入费用管理列表最后一页")
    hailong.find_elements_by_css_selector('li[class="number"]')[-1].click()
    time.sleep(casjc_config.short_time)
    #获取当前预编辑计费资源名称
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'tr[class="el-table__row"]')))
    newuser = hailong.find_elements_by_css_selector('div[class="cell el-tooltip"]')[-8].text
    if newuser != cname:
        casjc_log.logging.info(title + " 最后一条数据不是预期要编辑的计费")
        casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, "最后一条数据不是预期要编辑的计费，退出登录"]
        aaa.Casjc_logout()
        return None
    casjc_log.logging.info(title + " 当前准备要编辑的计费的资源名称为，" + newuser)
    #编辑最后一条费用管理记录
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'button[class="el-button el-button--text el-button--mini"]')))
    casjc_log.logging.info(title + " 编辑最后一条费用管理记录")
    hailong.find_elements_by_css_selector('button[class="el-button el-button--text el-button--mini"]')[-2].click()
    #进入编辑页面
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="el-card__body"]')))
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 进入编辑页面，点击确定按钮")
    #等待编辑页面确定按钮
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'button[class="el-button el-button--primary el-button--small"]')))
    time.sleep(casjc_config.short_time)
    #点击确定按钮
    hailong.find_element_by_css_selector('button[class="el-button el-button--primary el-button--small"]').click()
    #获取提交请求返回信息
    aaa.admin_result(title,uname,newuser)
    return None


#费用管理-删除计费
def Casjc_delCost(cname=""):
    title = "删除计费"
    if not cname:
        casjc_log.logging.info(title + " 没有传递cname参数,计费管理的资源名称")
        casjc_config.casjc_result[title + time.strftime("%M%S")] = ["", "没有给予资源名称，退出登录"]
        return None 
    #登录，点击运营中心菜单
    uname = myconfig['user1']
    upasswd = myconfig['passwd1']
    uurl = myconfig['adminUrl']
    hailong = webdriver.Chrome()
    aaa = casjc_page.Casjc_admin_page(hailong,uname,upasswd,uurl)
    casjc_log.logging.info(title + " 进入运营中心菜单")
    aaa.admin_operationcenter()
    #进入费用管理菜单
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'li[data-index="/costList"]')))
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 进入费用管理菜单")
    hailong.find_element_by_css_selector('li[data-index="/costList"]').click()
    time.sleep(casjc_config.short_time)
    #获取费用管理列表页有多少条数据
    try:
        WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'span[class="el-pagination__total"]')))
    except exceptions.TimeoutException:
        imagename = title + time.strftime("%m%d%H%M%S") + '.png'
        hailong.save_screenshot(r'C:\usr\Apache24\htdocs\image\\' + imagename)
        casjc_log.logging.info(title + " 页面元素未找到，或费用管理列表没有数据，退出登录, 查看截图 %s" %imagename)
        casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, "操作异常"]
        aaa.Casjc_logout()
        return None
    totalnum = hailong.find_element_by_css_selector('span[class="el-pagination__total"]').text
    casjc_log.logging.info(title + " 费用管理列表数据条数，" + totalnum)
    #进入费用管理列表最后一页
    casjc_log.logging.info(title + " 进入费用管理列表最后一页")
    hailong.find_elements_by_css_selector('li[class="number"]')[-1].click()
    time.sleep(casjc_config.short_time)
    #获取当前预删除计费资源名称
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'tr[class="el-table__row"]')))
    newuser = hailong.find_elements_by_css_selector('div[class="cell el-tooltip"]')[-8].text
    if newuser != cname:
        casjc_log.logging.info(title + " 最后一条数据不是预期要删除的计费")
        casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, "最后一条数据不是预期要删除的计费，退出登录"]
        aaa.Casjc_logout()
        return None
    casjc_log.logging.info(title + " 当前准备要删除的计费的资源名称为，" + newuser)
    #删除最后一条费用管理记录
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'button[class="el-button el-button--text el-button--mini"]')))
    casjc_log.logging.info(title + " 删除最后一条费用管理记录")
    hailong.find_elements_by_css_selector('button[class="el-button el-button--text el-button--mini"]')[-1].click()
    #弹出删除确认提示框，点击确定
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="el-message-box"]')))
    casjc_log.logging.info(title + " 弹出删除确认提示框，点击确定")
    hailong.find_element_by_css_selector('button[class="el-button el-button--default el-button--small el-button--primary "]').click()
    #获取提交请求返回信息
    aaa.admin_result(title,uname,newuser)
    return None


#新建企业管理用户
def Casjc_addsysent():
    title = "新增企业管理用户"
    #登录，点击用户系统菜单
    uname = myconfig['user1']
    upasswd = myconfig['passwd1']
    uurl = myconfig['adminUrl']
    hailong = webdriver.Chrome()
    aaa = casjc_page.Casjc_admin_page(hailong,uname,upasswd,uurl)
    casjc_log.logging.info(title + " 进入企业管理菜单")
    aaa.admin_usersystem()
    #进入用户管理菜单
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="el-submenu__title"]')))
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 进入用户管理菜单")
    hailong.find_elements_by_css_selector('div[class="el-submenu__title"]')[-1].click()
    #点击企业用户菜单
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'li[data-index="/enterprise"]')))
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 点击企业用户菜单")
    hailong.find_element_by_css_selector('li[data-index="/enterprise"]').click()
    #点击新增企业用户按钮
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="el-row"]')))
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 点击新增企业用户按钮")
    hailong.find_elements_by_css_selector('button[class="el-button el-button--primary el-button--small"]')[0].click()
    #判断打开新增弹窗成功
    if hailong.find_elements_by_css_selector('span[class="el-dialog__title"]')[-1].text == "新增企业用户":
        casjc_log.logging.info(title + " 新增弹窗打开成功" )      
    #输入企业用户账号
    newuser = "ui" + time.strftime("%m%d%H%M",time.localtime())
    casjc_log.logging.info(title + " 输入企业用账号" + newuser)
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[-7].send_keys(newuser)
    #输入企业用户姓名
    casjc_log.logging.info(title + " 输入企业用户姓名")
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[-6].send_keys(u"自动化管理用户")
    #获取邮箱,输入企业用户邮箱
    mm = casjc_mode.Casjc_mail()
    casjc_log.logging.info(title + " 输入企业用户邮箱:" + mm[0])
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[-5].send_keys(mm[0])
    #输入手机号
    casjc_log.logging.info(title + " 输入手机号")
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[-4].send_keys("131" + time.strftime("%m%d%H%M",time.localtime()))
    #输入固定电话
    mm = casjc_mode.Casjc_mail()
    dh = "010-88888888"
    casjc_log.logging.info(title + " 输入固定电话:" + dh)
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[-3].send_keys(dh)
    #选择企业单位
    try:
        casjc_log.logging.info(title + " 选择企业单位")
        hailong.find_elements_by_css_selector('input[placeholder="请选择企业单位"]')[1].click()
        time.sleep(casjc_config.show_time)
        hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')[-1].click()
    except:
        imagename = title + time.strftime("%m%d%H%M%S") + '.png'
        hailong.save_screenshot(r'C:\usr\Apache24\htdocs\image\\' + imagename)
        casjc_log.logging.info(title + " 选择企业单位异常，退出登录,查看截图 %s" %imagename)
        casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, "选择企业单位异常"]
        aaa.Casjc_logout(uname)
        return None
    #选择角色
    try:
        casjc_log.logging.info(title + " 选择角色")
        hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[-1].click()
        #hailong.find_elements_by_css_selector('input[placeholder="请选择角色"]')[1].click()
        time.sleep(casjc_config.short_time)
        hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')[-1].click()
    except:
        imagename = title + time.strftime("%m%d%H%M%S") + '.png'
        hailong.save_screenshot(r'C:\usr\Apache24\htdocs\image\\' + imagename)
        casjc_log.logging.info(title + " 选择角色异常，退出登录, 查看截图 %s" %imagename)
        casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, "选择角色异常"]
        aaa.Casjc_logout(uname)
        return None
    #点击保存按钮
    casjc_log.logging.info(title + " 点击保存按钮")
    hailong.find_elements_by_css_selector('button[class="el-button el-button--primary"]')[-1].click()
    #获取提交请求返回信息
    aaa.admin_result(title,uname,newuser)
    '''
    #新用户修改密码，修改为123456aA~
    passwd = casjc_mode.Casjc_mailpasswd(mm)
    if not passwd:
        casjc_log.logging.info(title + " 重置密码，邮箱没有收到")
        return None     
    casjc_log.logging.info(title + " 账号: " + newuser +" 密码: " + passwd)
    logindata = {"account":newuser,"password":passwd,"rememberMe":False,"origin":0}
    header = {}
    header['Content-Type'] = "application/json"
    #用户登录，获取session
    r = requests.post("http://11.2.77.3:30089/portal-test/user/login/account", headers=header, data=json.dumps(logindata))
    token = r.json()['data']
    header2 = {}
    header2["Authorization"] = token
    #获取用户id
    r2 = requests.get("http://11.2.77.3:30089/portal-test/user/person/get", headers=header2)
    userid = r2.json()["data"]["id"]
    pswddata = {"conPassword":"123456aA~","id":userid,"newPassword":"123456aA~","oldPassword":passwd}
    #修改密码
    r3 = requests.post("http://11.2.77.3:30089/portal-test/user/updatePassword", headers=header2, data=pswddata)
    if r3.status_code == 200:
        casjc_log.logging.info(title + " 修改密码成功,账号: " + newuser +"新密码: 123456aA~")
    else:
        casjc_log.logging.info(title + " 修改密码失败,账号: " + newuser +" 邮件收到密码: " + passwd)
    '''
    return None



#新建企业普通用户
def Casjc_addent():
    title = "新增企业普通用户"
    #登录，点击用户系统菜单
    uname = myconfig['user1']
    upasswd = myconfig['passwd1']
    uurl = myconfig['adminUrl']
    hailong = webdriver.Chrome()
    aaa = casjc_page.Casjc_admin_page(hailong,uname,upasswd,uurl)
    casjc_log.logging.info(title + " 进入用户系统菜单")
    aaa.admin_usersystem()
    #进入用户管理菜单
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="el-submenu__title"]')))
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 进入用户管理菜单")
    hailong.find_elements_by_css_selector('div[class="el-submenu__title"]')[-1].click()
    #点击企业用户菜单
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'li[data-index="/enterprise"]')))
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 点击企业用户菜单")
    hailong.find_element_by_css_selector('li[data-index="/enterprise"]').click()
    #点击新增企业用户按钮
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="el-row"]')))
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 点击新增企业用户按钮")
    hailong.find_elements_by_css_selector('button[class="el-button el-button--primary el-button--small"]')[0].click()
    #判断打开新增弹窗成功
    if hailong.find_elements_by_css_selector('span[class="el-dialog__title"]')[-1].text == "新增企业用户":
        casjc_log.logging.info(title + " 新增弹窗打开成功")
    #输入企业用户账号
    newuser = "ui" + time.strftime("%m%d%H%M%S",time.localtime())
    casjc_log.logging.info(title + " 输入企业用户账号" + newuser)
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[-7].send_keys(newuser)
    #输入企业用户姓名
    casjc_log.logging.info(title + " 输入企业用姓名")
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[-6].send_keys("自动化普通用户")
    #输入企业用户邮箱
    casjc_log.logging.info(title + " 输入企业用户邮箱")
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[-5].send_keys(str(random.randint(10000,99999)) + "@qq.com")
    #输入手机号
    casjc_log.logging.info(title + " 输入手机号")
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[-4].send_keys("177" + time.strftime("%m%d%H%M",time.localtime()))
    #输入电话号码
    casjc_log.logging.info(title + " 输入电话号码")
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[-3].send_keys("010-12345678")
    #选择企业单位
    try:
        casjc_log.logging.info(title + " 选择企业单位")
        hailong.find_elements_by_css_selector('input[placeholder="请选择企业单位"]')[1].click()
        time.sleep(casjc_config.show_time)
        hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')[-1].click()
    except:
        imagename = title + time.strftime("%m%d%H%M%S") + '.png'
        hailong.save_screenshot(r'C:\usr\Apache24\htdocs\image\\' + imagename)
        casjc_log.logging.info(title + " 选择企业单位异常，退出登录, 查看截图 %s" %imagename)
        casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, "选择企业单位异常"]
        aaa.Casjc_logout(uname)
        return None
    #选择角色
    try:
        casjc_log.logging.info(title + " 选择角色")
        hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[-1].click()
        #hailong.find_elements_by_css_selector('input[placeholder="请选择角色"]')[1].click()
        time.sleep(casjc_config.short_time)
        hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')[-2].click()
    except:
        imagename = title + time.strftime("%m%d%H%M%S") + '.png'
        hailong.save_screenshot(r'C:\usr\Apache24\htdocs\image\\' + imagename)
        casjc_log.logging.info(title + " 选择角色异常，退出登录, 查看截图 %s" %imagename)
        casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, "选择角色异常"]
        aaa.Casjc_logout(uname)
        return None
    #点击关联企业管理员
    try:
        casjc_log.logging.info(title + " 选择管理的企业管理员")
        hailong.find_elements_by_css_selector('input[placeholder="请选择管理员"]')[0].click()
        time.sleep(casjc_config.short_time)
        hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')[-1].click()
    except:
        imagename = title + time.strftime("%m%d%H%M%S") + '.png'
        hailong.save_screenshot(r'C:\usr\Apache24\htdocs\image\\' + imagename)
        casjc_log.logging.info(title + " 选择管理的企业管理员异常，退出登录, 查看截图 %s" % imagename)
        casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, "选择关联企业管理员异常"]
        aaa.Casjc_logout(uname)
        return None
    #点击保存按钮
    casjc_log.logging.info(title + " 点击保存按钮")
    hailong.find_elements_by_css_selector('button[class="el-button el-button--primary"]')[-1].click()
    #获取提交请求返回信息
    aaa.admin_result(title,uname,newuser)
    return None


#编辑企业用户
def Casjc_editent():
    title = "编辑企业用户"
    #登录，点击用户系统菜单
    uname = myconfig['user1']
    upasswd = myconfig['passwd1']
    uurl = myconfig['adminUrl']
    hailong = webdriver.Chrome()
    aaa = casjc_page.Casjc_admin_page(hailong,uname,upasswd,uurl)
    casjc_log.logging.info(title + " 进入用户系统菜单")
    aaa.admin_usersystem()
    #进入用户管理菜单
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="el-submenu__title"]')))
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 进入用户管理菜单")
    hailong.find_elements_by_css_selector('div[class="el-submenu__title"]')[-1].click()
    #点击企业用户菜单
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'li[data-index="/enterprise"]')))
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 点击企业用户菜单")
    hailong.find_element_by_css_selector('li[data-index="/enterprise"]').click()
    #点击用户列表更多按钮
    try:
        WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'button[class="el-button el-button--text el-button--mini el-popover__reference"]')))
        time.sleep(casjc_config.short_time)
        casjc_log.logging.info(title + " 点击列表页第一条数据的更多按钮")
        hailong.find_elements_by_css_selector('button[class="el-button el-button--text el-button--mini el-popover__reference"]')[0].click()
    except exceptions.TimeoutException:
        imagename = title + time.strftime("%m%d%H%M%S") + '.png'
        hailong.save_screenshot(r'C:\usr\Apache24\htdocs\image\\' + imagename)
        casjc_log.logging.info(title + " 点击列表页第一条数据的更多按钮异常，退出登录, 查看截图 %s" %imagename)
        casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, "操作异常,用户列表没有找到编辑按钮"]
        aaa.Casjc_logout(uname)
        return None
    #点击编辑按钮
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 点击编辑按钮")
    hailong.find_elements_by_css_selector('p[class="operator"]')[-6].click()
    #获取用户姓名
    newuser = hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[4].get_attribute('value')
    casjc_log.logging.info(title + " 当前编辑用户姓名" + newuser)
    #输入企业用户邮箱
    #hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[6].send_keys(str(random.randint(10000,99999)) + "@qq.com")
    #输入手机号
    #hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[7].send_keys("1310101" + str(random.randint(1000,9999)))
    #点击确定按钮
    casjc_log.logging.info(title + " 点击确定按钮")
    hailong.find_elements_by_css_selector('button[class="el-button el-button--primary"]')[-1].click()
    #获取提交请求返回信息
    aaa.admin_result(title,uname,newuser)
    return None


#企业用户重置密码
def Casjc_resset():
    title = "企业用户重置密码"
    #登录，点击用户系统菜单
    uname = myconfig['user1']
    upasswd = myconfig['passwd1']
    uurl = myconfig['adminUrl']
    hailong = webdriver.Chrome()
    aaa = casjc_page.Casjc_admin_page(hailong,uname,upasswd,uurl)
    casjc_log.logging.info(title + " 进入用户系统菜单")
    aaa.admin_usersystem()
    #进入用户管理菜单
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="el-submenu__title"]')))
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 进入用户管理菜单")
    hailong.find_elements_by_css_selector('div[class="el-submenu__title"]')[-1].click()
    #点击企业用户菜单
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'li[data-index="/enterprise"]')))
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 点击企业用户菜单")
    hailong.find_element_by_css_selector('li[data-index="/enterprise"]').click()
    #点击用户列表更多按钮
    try:
        WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'button[class="el-button el-button--text el-button--mini el-popover__reference"]')))
        time.sleep(casjc_config.short_time)
        casjc_log.logging.info(title + " 点击列表页第一条数据的更多按钮")
        hailong.find_elements_by_css_selector('button[class="el-button el-button--text el-button--mini el-popover__reference"]')[0].click()
    except exceptions.TimeoutException:
        imagename = title + time.strftime("%m%d%H%M%S") + '.png'
        hailong.save_screenshot(r'C:\usr\Apache24\htdocs\image\\' + imagename)
        casjc_log.logging.info(title + " 点击列表页第一条数据的更多按钮异常，退出登录, 查看截图 %s" %imagename)
        casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, "操作异常,用户列表没有找到编辑按钮"]
        aaa.Casjc_logout(uname)
        return None
    #获取用账号
    account = hailong.find_elements_by_css_selector('div[class="cell el-tooltip"]')[0].text
    casjc_log.logging.info(title + " 当前重置密码账号，" + account)
    #点击重置密码按钮
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 点击重置密码按钮")
    hailong.find_elements_by_css_selector('p[class="operator"]')[-5].click()
    #等待页面元素，弹出确认提示框
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="el-dialog__body"]')))
    #点击确认提示框的确认按钮
    casjc_log.logging.info(title + " 点击确认提示框的确认按钮")
    hailong.find_elements_by_css_selector('button[class="el-button el-button--primary el-button--small"]')[-2].click()
    #获取提交请求返回信息
    aaa.admin_result(title,uname,account)
    return None


#企业用户修改密码
def Casjc_updatepwd():
    title = "企业用户修改密码"
    #登录，点击用户系统菜单
    uname = myconfig['user1']
    upasswd = myconfig['passwd1']
    uurl = myconfig['adminUrl']
    hailong = webdriver.Chrome()
    aaa = casjc_page.Casjc_admin_page(hailong,uname,upasswd,uurl)
    casjc_log.logging.info(title + " 进入用户系统菜单")
    aaa.admin_usersystem()
    #进入用户管理菜单
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="el-submenu__title"]')))
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 进入用户管理菜单")
    hailong.find_elements_by_css_selector('div[class="el-submenu__title"]')[-1].click()
    #点击企业用户菜单
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'li[data-index="/enterprise"]')))
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 点击企业用户菜单")
    hailong.find_element_by_css_selector('li[data-index="/enterprise"]').click()
    #点击用户列表更多按钮
    try:
        WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'button[class="el-button el-button--text el-button--mini el-popover__reference"]')))
        time.sleep(casjc_config.short_time)
        casjc_log.logging.info(title + " 点击列表页第一条数据的更多按钮")
        hailong.find_elements_by_css_selector('button[class="el-button el-button--text el-button--mini el-popover__reference"]')[0].click()
    except exceptions.TimeoutException:
        imagename = title + time.strftime("%m%d%H%M%S") + '.png'
        hailong.save_screenshot(r'C:\usr\Apache24\htdocs\image\\' + imagename)
        casjc_log.logging.info(title + " 点击列表页第一条数据的更多按钮异常，退出登录, 查看截图 %s" %imagename)
        casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, "操作异常,用户列表没有找到更多按钮"]
        aaa.Casjc_logout(uname)
        return None
    #获取用账号
    account = hailong.find_elements_by_css_selector('div[class="cell el-tooltip"]')[0].text
    casjc_log.logging.info(title + " 当前修改密码账号，" + account)
    #点击修改密码按钮
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 点击修改密码按钮")
    hailong.find_elements_by_css_selector('p[class="operator"]')[-4].click()
    #等待页面元素，弹出修改密码输入框
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="el-dialog__body"]')))
    time.sleep(casjc_config.short_time)
    #输入新密码
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[-2].send_keys("123456aA~")
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[-1].send_keys("123456aA~")
    #点击确认提示框的确认按钮
    casjc_log.logging.info(title + " 点击确认提示框的确认按钮")
    hailong.find_elements_by_css_selector('button[class="el-button el-button--primary el-button--small"]')[-1].click()
    #获取提交请求返回信息
    aaa.admin_result(title,uname,account)
    return None

    


#新建系统用户
def Casjc_addsysuser():
    title = "新增系统用户"
    #登录，点击用户系统菜单
    uname = myconfig['user1']
    upasswd = myconfig['passwd1']
    uurl = myconfig['adminUrl']
    hailong = webdriver.Chrome()
    aaa = casjc_page.Casjc_admin_page(hailong,uname,upasswd,uurl)
    casjc_log.logging.info(title + " 进入用户系统菜单")
    aaa.admin_usersystem()
    #进入用户管理菜单
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="el-submenu__title"]')))
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 进入用户管理菜单")
    hailong.find_elements_by_css_selector('div[class="el-submenu__title"]')[-1].click()
    #点击系统用户菜单
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'li[data-index="/userManagement"]')))
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 点击系统用户菜单")
    hailong.find_element_by_css_selector('li[data-index="/userManagement"]').click()
    #点击新增用户按钮
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="el-row"]')))
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 点击新增用户按钮")
    hailong.find_elements_by_css_selector('button[class="el-button el-button--primary el-button--small"]')[0].click()
    #判断打开新增弹窗成功
    if hailong.find_elements_by_css_selector('span[class="el-dialog__title"]')[-1].text == "新增系统用户":
        casjc_log.logging.info(title + " 新增弹窗打开成功")
    #输入用户账号
    newuser = "ui" + time.strftime("%m%d%H%M%S",time.localtime())
    casjc_log.logging.info(title + " 输入用户账号," + newuser)
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[-7].send_keys(newuser)
    #输入用户姓名
    casjc_log.logging.info(title + " 输入用户姓名")
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[-6].send_keys("自动化系统用户")
    #输入用户邮箱
    casjc_log.logging.info(title + " 输入用户邮箱")
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[-5].send_keys(str(random.randint(10000,99999)) + "@qq.com")
    #输入手机号
    casjc_log.logging.info(title + " 输入手机号")
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[-4].send_keys("177" + time.strftime("%m%d%H%M",time.localtime()))
    #输入电话号码
    casjc_log.logging.info(title + " 输入电话号码")
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[-3].send_keys("010-88888888")
    #选择组织机构
    try:
        casjc_log.logging.info(title + " 选择组织机构")
        hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[-2].click()
        #hailong.find_element_by_css_selector('input[placeholder="请选择组织机构"]').click()
        time.sleep(casjc_config.short_time)
        hailong.find_elements_by_css_selector('i[class="el-icon-arrow-right el-cascader-node__postfix"]')[1].click()
        time.sleep(casjc_config.short_time)
        hailong.find_elements_by_css_selector('i[class="el-icon-arrow-right el-cascader-node__postfix"]')[3].click()
        time.sleep(casjc_config.short_time)
        hailong.find_elements_by_css_selector('i[class="el-icon-arrow-right el-cascader-node__postfix"]')[4].click()
        time.sleep(casjc_config.short_time)
        hailong.find_elements_by_css_selector('li[role="menuitem"]')[-1].click()
    except IndexError:
        imagename = title + time.strftime("%m%d%H%M%S") + '.png'
        hailong.save_screenshot(r'C:\usr\Apache24\htdocs\image\\' + imagename)
        casjc_log.logging.info(title + " 选择组织机构异常,退出登录, 查看截图 %s" %imagename)
        casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, "选择组织机构异常"]
        aaa.Casjc_logout(uname)
        return None
    #选择角色
    try :
        casjc_log.logging.info(title + " 选择角色")
        hailong.find_element_by_css_selector('input[class="el-select__input"]').click()
        time.sleep(casjc_config.short_time)
        hailong.find_elements_by_css_selector('li[class="el-select-dropdown__item"]')[-2].click()
        hailong.find_elements_by_css_selector('div[class="el-dialog__header"]')[-2].click()
        time.sleep(casjc_config.show_time)
    except:
        imagename = title + time.strftime("%m%d%H%M%S") + '.png'
        hailong.save_screenshot(r'C:\usr\Apache24\htdocs\image\\' + imagename)
        casjc_log.logging.info(title + " 选择角色异常，退出登录, 查看截图 %s" %imagename)
        casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, " 选择角色异常"]
        aaa.Casjc_logout(uname)
        return None
    #点击保存按钮
    casjc_log.logging.info(title + " 点击保存按钮")
    hailong.find_elements_by_css_selector('button[class="el-button el-button--primary"]')[-1].click()
    #获取提交请求返回信息
    aaa.admin_result(title,uname,newuser)
    return None


#编辑系统用户
def Casjc_editsysuser():
    title = "编辑系统用户"
    #登录，点击用户系统菜单
    uname = myconfig['user1']
    upasswd = myconfig['passwd1']
    uurl = myconfig['adminUrl']
    hailong = webdriver.Chrome()
    aaa = casjc_page.Casjc_admin_page(hailong,uname,upasswd,uurl)
    casjc_log.logging.info(title + " 进入用户系统菜单")
    aaa.admin_usersystem()
    #进入用户管理菜单
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="el-submenu__title"]')))
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 进入用户管理菜单")
    hailong.find_elements_by_css_selector('div[class="el-submenu__title"]')[-1].click()
    #点击系统用户菜单
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'li[data-index="/userManagement"]')))
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 点击系统用户菜单")
    hailong.find_element_by_css_selector('li[data-index="/userManagement"]').click()
    #点击用户列表更多按钮
    try:
        WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'button[class="el-button el-button--text el-button--mini el-popover__reference"]')))
        time.sleep(casjc_config.short_time)
        casjc_log.logging.info(title + " 点击用户列表第一条数据的更多按钮")
        hailong.find_elements_by_css_selector('button[class="el-button el-button--text el-button--mini el-popover__reference"]')[0].click()
    except exceptions.TimeoutException:
        imagename = title + time.strftime("%m%d%H%M%S") + '.png'
        hailong.save_screenshot(r'C:\usr\Apache24\htdocs\image\\' + imagename)
        casjc_log.logging.info(title + " 点击用户列表第一条数据的更多按钮异常，退出登录, 查看截图 %s" %imagename)
        casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, " 操作异常,用户列表没有找到编辑按钮"]
        aaa.Casjc_logout(uname)
        return None
    #点击编辑按钮
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 点击编辑按钮")
    for i in hailong.find_elements_by_tag_name('p'):
        print(i.text)
    hailong.find_elements_by_tag_name('p')[-5].click()
    #hailong.find_element_by_xpath("//div[@class='cell'][18]/span").click()
    #获取用户姓名
    newuser = hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[3].get_attribute('value')
    casjc_log.logging.info(title + " 当前编辑用户" + newuser)
    #输入企业用户邮箱
    #hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[5].send_keys(str(random.randint(10000,99999)) + "@qq.com")
    #输入手机号
    #hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[6].send_keys("1310101" + str(random.randint(1000,9999)))
    #点击确定按钮
    casjc_log.logging.info(title + " 点击确定按钮")
    hailong.find_elements_by_css_selector('button[class="el-button el-button--primary"]')[-1].click()
    #获取提交请求返回信息
    aaa.admin_result(title,uname,newuser)
    return None


#系统用户重置密码
def Casjc_sysresset():
    title = "系统用户重置密码"
    #登录，点击用户系统菜单
    uname = myconfig['user1']
    upasswd = myconfig['passwd1']
    uurl = myconfig['adminUrl']
    hailong = webdriver.Chrome()
    aaa = casjc_page.Casjc_admin_page(hailong,uname,upasswd,uurl)
    casjc_log.logging.info(title + " 进入用户系统菜单")
    aaa.admin_usersystem()
    #进入用户管理菜单
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="el-submenu__title"]')))
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 进入用户管理菜单")
    hailong.find_elements_by_css_selector('div[class="el-submenu__title"]')[-1].click()
    #点击系统用户菜单
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'li[data-index="/userManagement"]')))
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 点击系统用户菜单")
    hailong.find_element_by_css_selector('li[data-index="/userManagement"]').click()
    #点击用户列表更多按钮
    try:
        WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'button[class="el-button el-button--text el-button--mini el-popover__reference"]')))
        time.sleep(casjc_config.short_time)
        casjc_log.logging.info(title + " 点击用户列表第一条数据的更多按钮")
        hailong.find_elements_by_css_selector('button[class="el-button el-button--text el-button--mini el-popover__reference"]')[0].click()
    except exceptions.TimeoutException:
        imagename = title + time.strftime("%m%d%H%M%S") + '.png'
        hailong.save_screenshot(r'C:\usr\Apache24\htdocs\image\\' + imagename)
        casjc_log.logging.info(title + " 点击用户列表第一条数据的更多按钮异常，退出登录,查看截图 %s" %imagename)
        casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, " 操作异常,用户列表没有找到编辑按钮"]
        aaa.Casjc_logout(uname)
        return None
    #获取用账号
    account = hailong.find_elements_by_css_selector('div[class="cell el-tooltip"]')[0].text
    casjc_log.logging.info(title + " 当前重置密码账号，" + account)
    #点击重置密码按钮
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 点击重置密码按钮")
    hailong.find_elements_by_tag_name('p')[-4].click()
    #等待页面元素，弹出确认提示框
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="el-dialog__body"]')))
    #点击确认提示框的确认按钮
    casjc_log.logging.info(title + " 点击确认提示框的确认按钮")
    hailong.find_elements_by_css_selector('button[class="el-button el-button--primary el-button--small"]')[-2].click()
    #获取提交请求返回信息
    aaa.admin_result(title,uname,account)
    return None


#系统用户修改密码
def Casjc_sysupdatepwd():
    title = "系统用户修改密码"
    #登录，点击用户系统菜单
    uname = myconfig['user1']
    upasswd = myconfig['passwd1']
    uurl = myconfig['adminUrl']
    hailong = webdriver.Chrome()
    aaa = casjc_page.Casjc_admin_page(hailong,uname,upasswd,uurl)
    casjc_log.logging.info(title + " 进入用户系统菜单")
    aaa.admin_usersystem()
    #进入用户管理菜单
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="el-submenu__title"]')))
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 进入用户管理菜单")
    hailong.find_elements_by_css_selector('div[class="el-submenu__title"]')[-1].click()
    #点击系统用户菜单
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'li[data-index="/userManagement"]')))
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 点击系统用户菜单")
    hailong.find_element_by_css_selector('li[data-index="/userManagement"]').click()
    #点击用户列表更多按钮
    try:
        WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'button[class="el-button el-button--text el-button--mini el-popover__reference"]')))
        time.sleep(casjc_config.short_time)
        casjc_log.logging.info(title + " 点击用户列表第一条数据的更多按钮")
        hailong.find_elements_by_css_selector('button[class="el-button el-button--text el-button--mini el-popover__reference"]')[0].click()
    except exceptions.TimeoutException:
        imagename = title + time.strftime("%m%d%H%M%S") + '.png'
        hailong.save_screenshot(r'C:\usr\Apache24\htdocs\image\\' + imagename)
        casjc_log.logging.info(title + " 点击用户列表第一条数据的更多按钮异常，退出登录,查看截图 %s" %imagename)
        casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, " 操作异常,用户列表没有找到更多按钮"]
        aaa.Casjc_logout(uname)
        return None
    #获取用账号
    account = hailong.find_elements_by_css_selector('div[class="cell el-tooltip"]')[0].text
    casjc_log.logging.info(title + " 当前修改密码账号，" + account)
    #点击重置密码按钮
    time.sleep(casjc_config.short_time)
    casjc_log.logging.info(title + " 点击修改密码按钮")
    hailong.find_elements_by_tag_name('p')[-3].click()
    #等待页面元素，弹出确认提示框
    WebDriverWait(hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="el-dialog__body"]')))
    time.sleep(casjc_config.short_time)
    #输入新密码
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[-2].send_keys("123456aA~")
    hailong.find_elements_by_css_selector('input[class="el-input__inner"]')[-1].send_keys("123456aA~")
    #点击确认提示框的确认按钮
    casjc_log.logging.info(title + " 点击确认提示框的确认按钮")
    hailong.find_elements_by_css_selector('button[class="el-button el-button--primary el-button--small"]')[-1].click()
    #获取提交请求返回信息
    aaa.admin_result(title,uname,account)
    return None



if __name__ == "__main__":
    #srt = (6,-1)#高性能计算-共享
    #srt = (6,-2)#高性能计算-标准
    #srt = (8,-1)#数据存储-数据存储
    #srt = (9,-1)#网络资源-网络资源
    try:
        if sys.argv[1] == "dev":
            myconfig = casjc_config.devPerson['admin']
            env = "dev"
        else:
            myconfig = casjc_config.testPerson['admin']
            env = "test"
    except IndexError:
        myconfig = casjc_config.testPerson['admin']
        env = "test"
    casjc_log.logging.info(">" * 15 + " UI自动化脚本开始执行执行 " + "<" * 15)
    start_time = time.strftime("%m-%d %H:%M:%S",time.localtime())
    #计费管理中的服务和类型
    rstall = [(4,-1),(5,-1),(6,-1),(6,-2),(7,-1)]
    #申请资源中的配置方式与资源类型
    #appcon = [(0,"gg"),(0,"yy"),(0,"sw"),(0,"sy"),(0,"wg"),(1,"gg"),(1,"yy"),(1,"sw"),(1,"sy"),(1,"wg")]
    #appcon = [(0,"sy"),(0,"gg"),(0,"sw"),(1,"sy"),(1,"gg"),(1,"sw")]
    appcon = [(0,'sw'),(0,'gg'),(1,'sw'),(1,'gg')]
    
    #价格审批人员列表
    #试用
    order0 = [myconfig['user3'],myconfig['user6']]
    #新购
    order1 = [myconfig['user3'],myconfig['user7']]
    
    #非标准合同审批人员列表
    conuser = [myconfig['user3'],myconfig['user4'],myconfig['user5']]

    Casjc_addsysent()
    Casjc_updatepwd()
    
    '''
    Casjc_vlan()
    Casjc_vlanname()
    Casjc_vlandel()
    Casjc_publicvlan()
    Casjc_publicvlandel()
    '''
    '''
    for srt in rstall:
        res = Casjc_addCost(srt)
        Casjc_editCost(res)
        Casjc_delCost(res)
    '''
    '''
    Casjc_create_ent()
    Casjc_edit_ent()
    Casjc_addsysent()
    Casjc_addent()
    Casjc_editent()
    Casjc_resset()
    Casjc_updatepwd()
    Casjc_addsysuser()
    Casjc_editsysuser()
    Casjc_sysresset()
    Casjc_sysupdatepwd()
    
    '''
    #合同作废
    #作废合同号
    nnn = "GKJYHTXS202008012"
    #合同作废审批人员
    contractuser = ["kongshuishui","wangnan","tangdebing"]
    #Casjc_contract_void(nnn)
    #for i in contractuser:
    #   Casjc_contract_tovoid(nnn,i)
    
    
    for ac in appcon:
        #申请资源返回值为一个订单号和一个元组包含是否试用，资源类型，示例('20201026172520256', (0, 'gg'))
        xx = Casjc_res(ac)
        #xx = Casjc_res_area(ac)
        
        #审批特定订单
        #xx = ["20201027143557654",(1,'sy')]
        
        if not xx:
            continue
        if xx[1][0] == 0:
            for j in order0:
                Casjc_price(j,xx[0])
        if xx[1][0] == 1:
            for j in order1:
                Casjc_price(j,xx[0])
        #如果是新购，走合同审批和确认参数流程
        if ac[0] == 1:
            Casjc_contract(xx[0])
            for i in conuser:
                Casjc_contract_apply(i,xx[0])
        
            r = Casjc_change_config(xx)
            if r:
                print("进入配置")
                Casjc_config(xx)
        #如果是试用，直接配置
        elif ac[0] == 0:
            print("进入配置")
            Casjc_config(xx)
    
    #Casjc_config(["20201026162209362",'yy'])
    end_time = time.strftime("%m-%d %H:%M:%S",time.localtime())
    print ("开始时间： " + start_time)
    print ("结束时间： " + end_time)    
    print (json.dumps(casjc_config.casjc_result,ensure_ascii=False))
    casjc_mode.Run_result(("admin",start_time,end_time,json.dumps(casjc_config.casjc_result,ensure_ascii=False),env))
    casjc_log.logging.info( ">" * 15 + " 模块名: admin, 本次UI自动化脚本执行完成，通过页面模块筛选查看执行结果 " + "<" * 15)
