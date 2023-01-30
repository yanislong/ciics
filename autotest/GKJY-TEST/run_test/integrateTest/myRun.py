#!/usr/bin/env python


import userRegist, userLogin, findPasswd

#实例化注册模块
a = userRegist.userregist()
#合法账号手机号注册
a.phoneregist()
#非法账号手机号注册
a.illegrateAccountRegist()

#实例化用户登录模块
b = userLogin.userlogin()
#正确账号密码登录
b.accountLogin()
#正确账号错误密码登录
b.wpasslogin()
