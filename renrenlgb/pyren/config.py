# -*- coding: utf-8 -*-

LOGINURL = r'http://www.renren.com/PLogin.do'
ICODEURL = r'http://icode.renren.com/getcode.do?t=login&rnd=Math.random()'

#EMAIL = r'您的邮箱'
#PASSWORD = r'您的密码'
#EMAIL = r'wwdd.23@163.com'
EMAIL = r'13613112728'
PASSWORD = r'075100'

WALLURL = r'http://w.renren.com/wall/'

# FailCode via "login-v6.js"
FAILCODE = {
            '-1': '登录成功',
            '0': '登录系统错误，请稍后尝试',
            '1': '您的用户名和密码不匹配',
            '2': '您的用户名和密码不匹配',
            '4': '您的用户名和密码不匹配',
            '8': '请输入帐号，密码',
            '16': '您的账号已停止使用',
            '32': '帐号未激活，请激活帐号',
            '64': '您的帐号需要解锁才能登录',
            '128': '您的用户名和密码不匹配',
            '512': '请您输入验证码',
            '4096': '登录系统错误，稍后尝试',
}
