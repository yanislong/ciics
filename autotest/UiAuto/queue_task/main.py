#!/usr/bin/env python3

from websocket import create_connection
import time, json, random

import casjc_login
import casjc_config
import casjc_mode_task
import casjc_log_task
import casjc_resource
import casjc_user


def submitJob():

    title = "[已有资源用户,提交作业_" + str(random.randint(1000,9999)) + "] "
    global res
    userinfo = casjc_login.login(casjc_config.username, casjc_config.passwd, 0)
    url = "ws://10.8.14.194:11014/webshell?uid=" + str(userinfo[1]) + "&id=42&queueName=" + casjc_config.queuename + "&token=" + userinfo[0] + "&cols=132&rows=15&width=1870&height=510"
    jobname = str(time.strftime('%d%H%M',time.localtime()))
    try:
        ws = create_connection(url,timeout=60)
        print(ws.recv())
        sjob1 = 'nohup srun -p low -J casjc-' + jobname + ' sleep 180&\n'
        casjc_log_task.logging.info('执行slurm命令:' + sjob1)
        ws.send(sjob1)
        print(ws.recv())
        print(json.loads(ws.recv())['data'])
        ws.send('\n')
        print(ws.recv())
        time.sleep(5)
        sjob2 = 'squeue\n'
        casjc_log_task.logging.info('执行slurm命令:' + sjob2)
        ws.send(sjob2)
        print(ws.recv())
        squeue = ws.recv()
        print(squeue)
        res[title + sjob1] = [casjc_config.username, squeue]
        return True
    except Exception as e:
        print('error', e)
        return False

def newSubmitJob():

    """[新用户初次配置资源，提交作业]"""
    title = "[新用户初次配置资源，提交作业]"

    global res
    #新增企业用户
    newuser = casjc_user.auser()
    luser = newuser.addControlUser()
    #登录企业用户
    userinfo = casjc_login.login(luser[0], casjc_config.cpasswd, 0)
    #申请审批配置资源
    rescoure = casjc_resource.resource(luser[0], luser[1], luser[2])
    rescoure.testNew("half")
    #等待610秒,等高性能配置生效
    time.sleep(610)
    url = "ws://10.8.14.181:11014/webshell?uid=" + str(userinfo[1]) + "&id=42&queueName=" + casjc_config.queuename + "&token=" + userinfo[0] + "&cols=132&rows=15&width=1870&height=510"
    casjc_log_task.logging.info(newSubmitJob.__doc__ + " 登录webshell: " + url)
    jobname = str(time.strftime('%d%H%M',time.localtime()))
    try:
        ws = create_connection(url,timeout=60)
        print(ws.recv())
        sjob1 = 'nohup srun -p low -J casjc-' + jobname + ' sleep 180&\n'
        casjc_log_task.logging.info(newSubmitJob.__doc__ +'执行slurm命令:' + sjob1)
        print(ws.recv())
        print(json.loads(ws.recv())['data'])
        print(ws.recv())
        print(ws.recv())
        print(ws.recv())
        ws.send(sjob1)
        ws.send('\n')
        time.sleep(1)
        print(ws.recv())
        print(ws.recv())
        sjob2 = 'squeue\n'
        casjc_log_task.logging.info(newSubmitJob.__doc__ + '执行slurm命令:' + sjob2)
        ws.send(sjob2)
        print(ws.recv())
        time.sleep(2)
        squeue = ws.recv()
        print(squeue)
        res[title + sjob1] = [luser[0], squeue]
        return True
    except Exception as e:
        print('error', e)
        res[title] = [luser[0], "webServer timeout"]
        return False

def renewSubmitJob():

    """[新用户初次配置资源后续期资源，提交作业]"""
    title = "[新用户初次配置资源后续期资源，提交作业]"

    global res
    #新增企业用户
    newuser = casjc_user.auser()
    luser = newuser.addControlUser()
    #登录企业用户
    userinfo = casjc_login.login(luser[0], casjc_config.cpasswd, 0)
    #申请审批配置资源
    rescoure = casjc_resource.resource(luser[0], luser[1], luser[2])
    rescoure.testRenew()
    #等待610秒,等高性能配置生效
    time.sleep(610)
    url = "ws://10.8.14.181:11014/webshell?uid=" + str(userinfo[1]) + "&id=42&queueName=" + casjc_config.queuename + "&token=" + userinfo[0] + "&cols=132&rows=15&width=1870&height=510"
    casjc_log_task.logging.info(newSubmitJob.__doc__ + " 登录webshell: " + url)
    jobname = str(time.strftime('%d%H%M',time.localtime()))
    try:
        ws = create_connection(url,timeout=60)
        print(ws.recv())
        sjob1 = 'nohup srun -p low -J casjc-' + jobname + ' sleep 180&\n'
        casjc_log_task.logging.info(newSubmitJob.__doc__ +'执行slurm命令:' + sjob1)
        print(ws.recv())
        print(json.loads(ws.recv())['data'])
        print(ws.recv())
        print(ws.recv())
        print(ws.recv())
        ws.send(sjob1)
        ws.send('\n')
        time.sleep(1)
        print(ws.recv())
        print(ws.recv())
        sjob2 = 'squeue\n'
        casjc_log_task.logging.info(newSubmitJob.__doc__ + '执行slurm命令:' + sjob2)
        ws.send(sjob2)
        print(ws.recv())
        time.sleep(2)
        squeue = ws.recv()
        print(squeue)
        res[title + sjob1] = [luser[0], squeue]
        return True
    except Exception as e:
        print('error', e)
        res[title] = [luser[0], "webServer timeout"]
        return False

def entNewSubmitJob():

    """[新普通用户初次配置资源，提交作业]"""
    title = "[新普通用户初次配置资源，提交作业]"

    global res
    #新增企业用户
    newuser = casjc_user.auser()
    tmpuser = newuser.addControlUser()
    #申请审批配置资源
    rescoure = casjc_resource.resource(tmpuser[0], tmpuser[1], tmpuser[2])
    rescoure.testNew("half")
    #新增企业普通用户
    newuser2 = casjc_user.cuser(tmpuser[0])
    luser = newuser2.addQueueStoreUser()
    #登录企业普通用户
    userinfo = casjc_login.login(luser, casjc_config.cpasswd, 0)
    #等待610秒,等高性能配置生效
    time.sleep(610)
    url = "ws://10.8.14.181:11014/webshell?uid=" + str(userinfo[1]) + "&id=42&queueName=" + casjc_config.queuename + "&token=" + userinfo[0] + "&cols=132&rows=15&width=1870&height=510"
    casjc_log_task.logging.info(newSubmitJob.__doc__ + " 登录webshell: " + url)
    jobname = str(time.strftime('%d%H%M',time.localtime()))
    try:
        ws = create_connection(url,timeout=60)
        print(ws.recv())
        sjob1 = 'nohup srun -p low -J casjc-' + jobname + ' sleep 180&\n'
        casjc_log_task.logging.info(newSubmitJob.__doc__ +'执行slurm命令:' + sjob1)
        print(ws.recv())
        print(json.loads(ws.recv())['data'])
        print(ws.recv())
        print(ws.recv())
        print(ws.recv())
        ws.send(sjob1)
        ws.send('\n')
        time.sleep(1)
        print(ws.recv())
        print(ws.recv())
        sjob2 = 'squeue\n'
        casjc_log_task.logging.info(newSubmitJob.__doc__ + '执行slurm命令:' + sjob2)
        ws.send(sjob2)
        print(ws.recv())
        time.sleep(2)
        squeue = ws.recv()
        print(squeue)
        res[title + sjob1] = [luser[0], squeue]
        return True
    except Exception as e:
        print('error', e)
        res[title] = [luser[0], "webServer timeout"]
        return False

def entRenewSubmitJob():

    """[新普通用户初次配置资源后进行续期，提交作业]"""
    title = "[新普通用户初次配置资源后进行续期，提交作业]"

    global res
    #新增企业用户
    newuser = casjc_user.auser()
    tmpuser = newuser.addControlUser()
    #申请审批配置资源并续期
    rescoure = casjc_resource.resource(tmpuser[0], tmpuser[1], tmpuser[2])
    rescoure.testRenew()
    #新增企业普通用户
    newuser2 = casjc_user.cuser(tmpuser[0])
    luser = newuser2.addQueueStoreUser()
    #登录企业普通用户
    userinfo = casjc_login.login(luser, casjc_config.cpasswd, 0)
    #等待610秒,等高性能配置生效
    time.sleep(610)
    url = "ws://10.8.14.181:11014/webshell?uid=" + str(userinfo[1]) + "&id=42&queueName=" + casjc_config.queuename + "&token=" + userinfo[0] + "&cols=132&rows=15&width=1870&height=510"
    casjc_log_task.logging.info(newSubmitJob.__doc__ + " 登录webshell: " + url)
    jobname = str(time.strftime('%d%H%M',time.localtime()))
    try:
        ws = create_connection(url,timeout=60)
        print(ws.recv())
        sjob1 = 'nohup srun -p low -J casjc-' + jobname + ' sleep 180&\n'
        casjc_log_task.logging.info(newSubmitJob.__doc__ +'执行slurm命令:' + sjob1)
        print(ws.recv())
        print(json.loads(ws.recv())['data'])
        print(ws.recv())
        print(ws.recv())
        print(ws.recv())
        ws.send(sjob1)
        ws.send('\n')
        time.sleep(1)
        print(ws.recv())
        print(ws.recv())
        sjob2 = 'squeue\n'
        casjc_log_task.logging.info(newSubmitJob.__doc__ + '执行slurm命令:' + sjob2)
        ws.send(sjob2)
        print(ws.recv())
        time.sleep(2)
        squeue = ws.recv()
        print(squeue)
        res[title + sjob1] = [luser[0], squeue]
        return True
    except Exception as e:
        print('error', e)
        res[title] = [luser[0], "webServer timeout"]
        return False

if __name__ == "__main__":
    env = "test"
    res = {}
    start_time = time.strftime("%m-%d %H:%M:%S",time.localtime())
    submitJob()
    #newSubmitJob()
    #renewSubmitJob()
    #entNewSubmitJob()
    #entRenewSubmitJob()
    end_time = time.strftime("%m-%d %H:%M:%S",time.localtime())
    casjc_mode_task.Run_result(("task",start_time,end_time,json.dumps(res,ensure_ascii=False),env))
