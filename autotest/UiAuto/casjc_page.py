import time, sys, json, random

from selenium import webdriver
from selenium.webdriver.common.action_chains import *
from selenium.common import exceptions
from selenium.webdriver.support.wait import WebDriverWait  
from selenium.webdriver.support import expected_conditions as EC  
from selenium.webdriver.common.by import By

import casjc_config
import casjc_mode
import casjc_log


#driver = webdriver.PhantomJS(executable_path='')


def isElementExist():
    psss    

class Casjc_admin_page():

    def __init__(self,hailong,luser,lpasswd,lurl):
        self.hailong = hailong
        self.uname = luser        
        self.upasswd = lpasswd
        self.lurl = lurl
        self.Casjc_login()



    #登陆后台系统
    def Casjc_login(self):
        self.hailong.get(self.lurl)
        self.hailong.maximize_window()
        try:
            WebDriverWait(self.hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "input[type='text']")))
        except exceptions.TimeoutException:
            pass
        self.hailong.find_element_by_css_selector("input[type='text']").send_keys(self.uname)
        casjc_log.logging.info("管理后台登录-输入用户名:" + self.uname)
        self.hailong.find_element_by_css_selector('input[type="password"]').send_keys(self.upasswd)
        casjc_log.logging.info("管理后台登录-输入密码:" + self.upasswd)
        self.hailong.find_element_by_tag_name('button').click()
        #等待casjc_config.wait_time全局设置时间，判断是否登录成功进入首页
        try:
            WebDriverWait(self.hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'a[class="router-link-active"]')))
            if self.hailong.find_elements_by_css_selector('a[class="router-link-active"]')[0].text == "首页":
                time.sleep(casjc_config.show_time)
                #casjc_config.casjc_result['管理后台用户登录'+ time.strftime("%M%S",time.localtime())] = "当前用户: %s  登录成功" %self.uname
                return None
            else:
                casjc_config.casjc_result['管理后台用户登录'+ time.strftime("%M%S",time.localtime())] = [ self.uname, "登录失败,测试终止"]
                self.hailong.quit()
                casjc_log.logging.info("登录失败或点击页面菜单异常，终止程序")
                casjc_mode.Run_result(("admin","","",json.dumps(casjc_config.casjc_result,ensure_ascii=False),""))
                sys.exit()
                return None
        except exceptions.TimeoutException:
            imagename = "后台登录" + time.strftime("%m%d%H%M%S") + '.png'
            self.hailong.save_screenshot(r'C:\usr\Apache24\htdocs\image\\' + imagename)
            casjc_config.casjc_result['管理后台用户登录'+ time.strftime("%M%S",time.localtime())] = [ self.uname, "登录失败,测试终止,查看截图 %s" %imagename]
            self.hailong.quit()
            casjc_mode.Run_result(("admin","","",json.dumps(casjc_config.casjc_result,ensure_ascii=False),""))
            sys.exit()
            return None


    #退出后台系统
    def Casjc_logout(self,uname=""):
        title = "退出登录"
        aname = uname
        impl = self.hailong.find_element_by_css_selector('span[class="el-avatar el-avatar--medium el-avatar--circle el-popover__reference"]')
        chain = ActionChains(self.hailong)
        chain.move_to_element(impl).perform()
        try:
            #点击退出登录
            self.hailong.find_elements_by_tag_name('a')[-1].click()
            #弹出确认提示框，点击确定
            self.hailong.find_elements_by_css_selector('button[class="el-button el-button--default el-button--small el-button--primary "]')[0].click()
            casjc_log.logging.info("退出登录成功")
            time.sleep(casjc_config.show_time)
            self.hailong.quit()
            return None
        except:
            imagename = "后台退出" + time.strftime("%m%d%H%M%S") + '.png'
            self.hailong.save_screenshot(r'C:\usr\Apache24\htdocs\image\\' + imagename)
            casjc_config.casjc_result[title + time.strftime("%M%S")] = [aname, "退出登录异常,后台退出 %s" %imagename]
            self.hailong.quit()
            return None
        
        

    def admin_home(self):
        try:
            WebDriverWait(self.hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.LINK_TEXT, '首页')))
            self.hailong.find_element_by_link_text('首页').click()
            time.sleep(casjc_config.short_time)
        except:
            imagename = time.strftime("%m%d%H%M%S") + '.png'
            self.hailong.save_screenshot(r'C:\usr\Apache24\htdocs\image\\' + imagename)
            start_time = time.strftime("%m-%d %H:%M:%S",time.localtime())
            end_time = time.strftime("%m-%d %H:%M:%S",time.localtime())   
            casjc_config.casjc_result['打开首页菜单'+ time.strftime("%M%S",time.localtime())] = [self.uname, "页面异常,测试终止"]
            casjc_mode.Run_result(("admin",start_time,end_time,json.dumps(casjc_config.casjc_result,ensure_ascii=False)))
            self.hailong.quit()
            casjc_log.logging.info("登录失败或点击页面菜单异常，终止程序, 查看截图 %s" %imagename)
            sys.exit()
            return None

    def admin_resmanagement(self):
        try:
            WebDriverWait(self.hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.LINK_TEXT, '资源管理')))
            self.hailong.find_element_by_link_text('资源管理').click()
            time.sleep(casjc_config.short_time)
        except:
            imagename = time.strftime("%m%d%H%M%S") + '.png'
            self.hailong.save_screenshot(r'C:\usr\Apache24\htdocs\image\\' + imagename)
            start_time = time.strftime("%m-%d %H:%M:%S",time.localtime())
            end_time = time.strftime("%m-%d %H:%M:%S",time.localtime())   
            casjc_config.casjc_result['打开资源管理菜单'+ time.strftime("%M%S",time.localtime())] = [self.uname, "页面异常,测试终止"]
            casjc_mode.Run_result(("admin",start_time,end_time,json.dumps(casjc_config.casjc_result,ensure_ascii=False)))
            self.hailong.quit()
            casjc_log.logging.info("登录失败或点击页面菜单异常，终止程序,查看截图 %s" %imagename)
            sys.exit()
            return None

    def admin_operationcenter(self):
        try:
            WebDriverWait(self.hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.LINK_TEXT, '运营中心')))
            self.hailong.find_element_by_link_text('运营中心').click()
            time.sleep(casjc_config.short_time)
        except:
            imagename = time.strftime("%m%d%H%M%S") + '.png'
            self.hailong.save_screenshot(r'C:\usr\Apache24\htdocs\image\\' + imagename)
            start_time = time.strftime("%m-%d %H:%M:%S",time.localtime())
            end_time = time.strftime("%m-%d %H:%M:%S",time.localtime())   
            casjc_config.casjc_result['打开运营中心菜单'+ time.strftime("%M%S",time.localtime())] = [self.uname, "页面异常,测试终止"]
            casjc_mode.Run_result(("admin",start_time,end_time,json.dumps(casjc_config.casjc_result,ensure_ascii=False)))
            self.hailong.quit()
            casjc_log.logging.info("登录失败或点击页面菜单异常，终止程序,查看截图 %s" %imagename)
            sys.exit()
            return None
        
    def admin_appcenter(self):
        try:
            WebDriverWait(self.hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.LINK_TEXT, '应用中心')))
            self.hailong.find_element_by_link_text('应用中心').click()
            time.sleep(casjc_config.short_time)
        except:
            imagename = time.strftime("%m%d%H%M%S") + '.png'
            self.hailong.save_screenshot(r'C:\usr\Apache24\htdocs\image\\' + imagename)
            start_time = time.strftime("%m-%d %H:%M:%S",time.localtime())
            end_time = time.strftime("%m-%d %H:%M:%S",time.localtime())   
            casjc_config.casjc_result['打开应用中心菜单'+ time.strftime("%M%S",time.localtime())] = [self.uname, "页面异常,测试终止"]
            casjc_mode.Run_result(("admin",start_time,end_time,json.dumps(casjc_config.casjc_result,ensure_ascii=False)))
            self.hailong.quit()
            casjc_log.logging.info("登录失败或点击页面菜单异常，终止程序,查看截图 %s" %imagename)
            sys.exit()
            return None

    def admin_usersystem(self):
        try:
            WebDriverWait(self.hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.LINK_TEXT, '系统管理')))
            self.hailong.find_element_by_link_text('系统管理').click()
            time.sleep(casjc_config.short_time)
        except:
            imagename = time.strftime("%m%d%H%M%S") + '.png'
            self.hailong.save_screenshot(r'C:\usr\Apache24\htdocs\image\\' + imagename)
            start_time = time.strftime("%m-%d %H:%M:%S",time.localtime())
            end_time = time.strftime("%m-%d %H:%M:%S",time.localtime())   
            casjc_config.casjc_result['打开用户系统菜单'+ time.strftime("%M%S",time.localtime())] = [self.uname, "页面异常,测试终止"]
            casjc_mode.Run_result(("admin",start_time,end_time,json.dumps(casjc_config.casjc_result,ensure_ascii=False)))
            self.hailong.quit()
            casjc_log.logging.info("登录失败或点击页面菜单异常，终止程序,查看截图 %s" %imagename)
            sys.exit()
            return None

    def admin_result(self, title, aname="", anumber=""):
        try:
            WebDriverWait(self.hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'p[class="el-message__content"]')))
            if len(self.hailong.find_element_by_css_selector('p[class="el-message__content"]').text) == 0:
                casjc_log.logging.info("获取请求响应消息为空")
                casjc_config.casjc_result[title + time.strftime("%M%S")] = [aname, "操作数据:账号/单号 " + anumber + " 操作异常"]
                self.Casjc_logout()
                return None
            casjc_config.casjc_result[title + time.strftime("%M%S")] = [aname, "操作数据:账号/单号 " + anumber + self.hailong.find_element_by_css_selector('p[class="el-message__content"]').text]
            self.Casjc_logout()
            return None
        except exceptions.TimeoutException:
            imagename = time.strftime("%m%d%H%M%S") + '.png'
            self.hailong.save_screenshot(r'C:\usr\Apache24\htdocs\image\\' + imagename)
            casjc_log.logging.info("没有获取到响应消息,查看截图 %s" %imagename)
            casjc_config.casjc_result[title + time.strftime("%M%S")] = [aname, "操作数据:账号/单号 " + anumber + " 操作异常"]
            self.Casjc_logout()
            return None

    def admin_appwait(self, title, uname, ordernum):
        try:
            #等待加载待审批列表页面元素
            WebDriverWait(self.hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'thead[class="has-gutter"]')))
            time.sleep(casjc_config.short_time)
            WebDriverWait(self.hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'tr[class="el-table__row"]')))
            time.sleep(casjc_config.short_time)
            #获取第一页列表数据条数
            listnum = self.hailong.find_elements_by_css_selector('tr[class="el-table__row"]')
            casjc_log.logging.info(title + " 列表当前页数据条数为:%d 条数据"%len(listnum))
            #如果条数0，退出
            if len(listnum) == 0:
                casjc_log.logging.info("没有待生成合同或待审批订单")
                casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, "没有待生成合同或待审批订单"]
                return None
            mytmp = 0
            #循环遍历第一页列表是否有符合的订单号，如果有点击生成合同，没有退出
            for i in range(len(listnum)):
                if self.hailong.find_element_by_xpath('//tr[@class="el-table__row"][' + str(i+1) + ']/td/div[@class="cell el-tooltip"][1]').text == ordernum:
                    casjc_log.logging.info(title + " %s找到预期单号，点击生成或审批按钮" %str(ordernum))
                    self.hailong.find_elements_by_css_selector('button[class="el-button el-button--text el-button--mini"]')[i].click()
                    time.sleep(casjc_config.short_time)
                    mytmp = 1
                    break
            if mytmp == 0:
                casjc_log.logging.info("列表第一页没有找到符合的订单号")
                casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, "待审批列表第一页没有找到符合的订单号"]
                return None            
        except exceptions.TimeoutException:
            imagename = time.strftime("%m%d%H%M%S") + '.png'
            self.hailong.save_screenshot(r'C:\usr\Apache24\htdocs\image\\' + imagename)
            casjc_log.logging.info("没有待生成合同或待审批订单,查看截图 %s" %imagename)
            casjc_config.casjc_result[title + time.strftime("%M%S")] = [uname, "没有待生成合同或待审批订单"]
            return None

class Casjc_console_page():

    def __init__(self, hailong, uname, passwd, lurl):
        self.hailong = hailong
        self.uname = uname
        self.upasswd = passwd
        self.lurl = lurl
        self.console_login()


    #登陆控制台系统
    def console_login(self):
        self.hailong.get(self.lurl)
        self.hailong.maximize_window()
        try:
            WebDriverWait(self.hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'a[href="/login"]')))
            WebDriverWait(self.hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'input[type="text"]')))
            WebDriverWait(self.hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'input[type="password"]')))
        except exceptions.TimeoutException:
            casjc_log.logging.info("找不到登录按钮")
        self.hailong.find_elements_by_css_selector('a[href="/login"]')[0].click()
        time.sleep(casjc_config.show_time)
        self.hailong.find_element_by_css_selector("input[type='text']").send_keys(self.uname)
        casjc_log.logging.info("官网登录-输入用户名:" + self.uname)
        self.hailong.find_element_by_css_selector('input[type="password"]').send_keys(self.upasswd)
        casjc_log.logging.info("官网登录-输入密码:" + self.upasswd)
        self.hailong.find_element_by_tag_name('button').click()
        #等待casjc_config.wait_time全局设置时间，判断是否登录成功进入首页
        try:
            WebDriverWait(self.hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="console"]')))
            if self.hailong.find_elements_by_css_selector('div[class="console"]')[0].text == "控制台":
                time.sleep(casjc_config.show_time)
                #casjc_config.casjc_result['控制台用户登录'+ time.strftime("%M%S",time.localtime())] = [self.uname, "登录成功"]
                return None
            else:
                casjc_log.logging.info("控制台登录异常")
                casjc_config.casjc_result['控制台用户登录'+ time.strftime("%M%S",time.localtime())] = [self.uname, "登录失败,测试终止"]
                self.hailong.quit()
                sys.exit()
                return None
        except exceptions.TimeoutException:
            imagename = time.strftime("%m%d%H%M%S") + '.png'
            self.hailong.save_screenshot(r'C:\usr\Apache24\htdocs\image\\' + imagename)
            casjc_log.logging.info("控制台登录异常,查看截图 %s" %imagename)
            casjc_config.casjc_result['控制台用户登录'+ time.strftime("%M%S",time.localtime())] = [self.uname, "登录失败,测试终止"]
            self.hailong.quit()
            sys.exit()
            return None

    #退出控制台系统
    def console_logout(self, uname=""):
        title = "控制台退出登录"
        aname = uname
        WebDriverWait(self.hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="userinfo el-popover__reference"]')))
        impl = self.hailong.find_element_by_css_selector('div[class="userinfo el-popover__reference"]')
        chain = ActionChains(self.hailong)
        chain.move_to_element(impl).perform()
        time.sleep(casjc_config.short_time)
        try:
            #点击退出登录
            a = self.hailong.find_elements_by_css_selector('button[class="el-button btnText el-button--text"]')[-1].click()
            time.sleep(casjc_config.short_time)
            #弹出确认提示框，点击确定
            self.hailong.find_elements_by_css_selector('button[class="el-button el-button--default el-button--small el-button--primary "]')[0].click()
            casjc_log.logging.info(aname + " 退出登录成功")
            time.sleep(casjc_config.show_time)
            self.hailong.quit()
            return None
        except:
            imagename = time.strftime("%m%d%H%M%S") + '.png'
            self.hailong.save_screenshot(r'C:\usr\Apache24\htdocs\image\\' + imagename)
            casjc_log.logging.info(aname + " 退出登录异常,查看截图 %s" %imagename)
            casjc_config.casjc_result[title + time.strftime("%M%S")] = [aname, "退出登录异常"]
            self.hailong.quit()
            return None

    
    def console(self):
        try:
            WebDriverWait(self.hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="headerBarRight"]')))
            WebDriverWait(self.hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="console"]')))
            time.sleep(casjc_config.short_time)
            self.hailong.find_elements_by_css_selector('div[class="console"]')[0].click()
            time.sleep(casjc_config.show_time)
            return None
        except:
            imagename = time.strftime("%m%d%H%M%S") + '.png'
            self.hailong.save_screenshot(r'C:\usr\Apache24\htdocs\image\\' + imagename)
            start_time = time.strftime("%m-%d %H:%M:%S",time.localtime())
            end_time = time.strftime("%m-%d %H:%M:%S",time.localtime())   
            casjc_config.casjc_result['打开控制台'+ time.strftime("%M%S",time.localtime())] = [self.uname, "页面异常,测试终止"]
            casjc_mode.Run_result(("console",start_time,end_time,json.dumps(casjc_config.casjc_result,ensure_ascii=False)))
            self.hailong.quit()
            casjc_log.logging.info("登录失败或点击页面菜单异常，终止程序,查看截图 %s" %imagename)
            sys.exit()
            return None

    def console_result(self, title, aname="", anumber=""):
        try:
            WebDriverWait(self.hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'p[class="el-message__content"]')))
            resultmessage = self.hailong.find_element_by_css_selector('p[class="el-message__content"]').text
            if len(resultmessage) == 0:
                casjc_log.logging.info("获取请求响应消息为空")
                casjc_config.casjc_result[title + time.strftime("%M%S")] = [aname, "操作数据:账号/单号 " + anumber + " 操作异常"]
                self.console_logout()
                return None
            casjc_config.casjc_result[title + time.strftime("%M%S")] = [aname, "操作数据:账号/单号 " + anumber + resultmessage]
            self.console_logout()
            return None
        except exceptions.TimeoutException:
            imagename = time.strftime("%m%d%H%M%S") + '.png'
            self.hailong.save_screenshot(r'C:\usr\Apache24\htdocs\image\\' + imagename)
            casjc_log.logging.info("没有获取到请求响应消息,查看截图 %s" %imagename)
            casjc_config.casjc_result[title + time.strftime("%M%S")] = [aname, "操作数据:账号/单号 " + anumber + " 操作异常"]
            self.hailong.quit()
            return None


class Casjc_std_admin():

    def __init__(self,hailong,luser,lpasswd,lurl):
        self.hailong = hailong
        self.uname = luser        
        self.upasswd = lpasswd
        self.lurl = lurl
        self.Casjc_login()



    #登陆标准版后台系统
    def Casjc_login(self):
        self.hailong.get(self.lurl)
        self.hailong.maximize_window()
        try:
            WebDriverWait(self.hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "input[type='text']")))
        except exceptions.TimeoutException:
            pass
        self.hailong.find_element_by_css_selector("input[type='text']").send_keys(self.uname)
        casjc_log.logging.info("管理后台登录-输入用户名:" + self.uname)
        self.hailong.find_element_by_css_selector('input[type="password"]').send_keys(self.upasswd)
        casjc_log.logging.info("管理后台登录-输入密码:" + self.upasswd)
        self.hailong.find_element_by_tag_name('button').click()
        #等待casjc_config.wait_time全局设置时间，判断是否登录成功进入首页
        try:
            #WebDriverWait(self.hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class="subnav-header"]')))
            WebDriverWait(self.hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'img[src="/static/image/photo.png"]')))
        except exceptions.TimeoutException:
            imagename = "标准版后台登录" + time.strftime("%m%d%H%M%S") + '.png'
            self.hailong.save_screenshot(r'C:\usr\Apache24\htdocs\image\\' + imagename)
            casjc_config.casjc_result['标准版管理后台用户登录'+ time.strftime("%M%S",time.localtime())] = [ self.uname, "登录失败,测试终止,查看截图 %s" %imagename]
            self.hailong.quit()
            sys.exit()
            return None


    #退出标准版后台系统
    def Casjc_logout(self,uname=""):
        title = "退出登录"
        aname = uname
        impl = self.hailong.find_element_by_css_selector('span[class="el-avatar el-avatar--medium el-avatar--circle el-popover__reference"]')
        chain = ActionChains(self.hailong)
        chain.move_to_element(impl).perform()
        try:
            #点击退出登录
            self.hailong.find_elements_by_tag_name('a')[-1].click()
            #弹出确认提示框，点击确定
            self.hailong.find_elements_by_css_selector('button[class="el-button el-button--default el-button--small el-button--primary "]')[0].click()
            casjc_log.logging.info("退出登录成功")
            time.sleep(casjc_config.show_time)
            self.hailong.quit()
            return None
        except:
            imagename = "后台退出" + time.strftime("%m%d%H%M%S") + '.png'
            self.hailong.save_screenshot(r'C:\usr\Apache24\htdocs\image\\' + imagename)
            casjc_config.casjc_result[title + time.strftime("%M%S")] = [aname, "退出登录异常,后台退出 %s" %imagename]
            self.hailong.quit()
            return None

    def admin_result(self, title, aname="", anumber=""):
        try:
            WebDriverWait(self.hailong,casjc_config.wait_time,0.5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'p[class="el-message__content"]')))
            if len(self.hailong.find_element_by_css_selector('p[class="el-message__content"]').text) == 0:
                casjc_log.logging.info("获取请求响应消息为空")
                casjc_config.casjc_result[title + time.strftime("%M%S")] = [aname, "操作数据:账号/单号 " + anumber + " 操作异常"]
                self.Casjc_logout()
                return None
            casjc_config.casjc_result[title + time.strftime("%M%S")] = [aname, "操作数据:账号/单号 " + anumber + self.hailong.find_element_by_css_selector('p[class="el-message__content"]').text]
            self.Casjc_logout()
            return None
        except exceptions.TimeoutException:
            imagename = time.strftime("%m%d%H%M%S") + '.png'
            self.hailong.save_screenshot(r'C:\usr\Apache24\htdocs\image\\' + imagename)
            casjc_log.logging.info("没有获取到响应消息,查看截图 %s" %imagename)
            casjc_config.casjc_result[title + time.strftime("%M%S")] = [aname, "操作数据:账号/单号 " + anumber + " 操作异常"]
            self.Casjc_logout()
            return None

    
if __name__ == "__main__":
    hailong = webdriver.Chrome()
    a = Casjc_admin_page(hailong,"duliadmin","Test1234!")
    a.admin_home()
    a.admin_resmanagement()
    a.admin_operationcenter()
    a.admin_appcenter()
    a.admin_usersystem()
   
