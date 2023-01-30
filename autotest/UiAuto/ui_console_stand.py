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


import casjc_config
import casjc_mode
import casjc_page
import casjc_log
 

#申请资源
def stand_open():
    title = "价格审批"
    casjc_log.logging.info(title + " 本次要审批的订单号")
    #登录，点击资源管理菜单
    hailong = webdriver.Chrome()
    uname = myconfig["username"]
    upasswd = myconfig['passwd']
    uurl = myconfig['consoleUrl']
    aaa = casjc_page.Casjc_admin_page(hailong,uname,upasswd,uurl)
    casjc_log.logging.info(title + " 进入资源管理菜单")
    aaa.admin_resmanagement()


if __name__ == "__main__":
    myconfig = casjc_config.stdPerson['console']
    env = "std"
    casjc_log.logging.info(">" * 15 + " UI自动化脚本开始执行执行 " + "<" * 15)
    start_time = time.strftime("%m-%d %H:%M:%S",time.localtime())
    
    stand_open()
    end_time = time.strftime("%m-%d %H:%M:%S",time.localtime())
    print ("开始时间： " + start_time)
    print ("结束时间： " + end_time)    
    print (json.dumps(casjc_config.casjc_result,ensure_ascii=False))
    casjc_mode.Run_result(("admin",start_time,end_time,json.dumps(casjc_config.casjc_result,ensure_ascii=False),env))
    casjc_log.logging.info( ">" * 15 + " 模块名: admin, 本次UI自动化脚本执行完成，通过页面模块筛选查看执行结果 " + "<" * 15)
