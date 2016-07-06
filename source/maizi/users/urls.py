#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2015/11/3
@author: yopoing
users模块的url配置。
"""

from django.conf.urls import patterns,url
from users.views import *

urlpatterns = patterns('users.views',
    url(r'^re_login/$',re_login,name='re_login'),
    url(r'^captcha1/$', 'captcha1',name='captcha1'),
    url(r'^re_logout/$','re_logout',name='re_logout'),
    url(r'^reg/$','reg',name='reg'),
    url(r'^resetpassword/$','go_resetpassword_html',name='resetpassword'),
    url(r'^forgetpass/$',forgetpass,name='forgetpass'),
    url(r'^acuser/$','acuser',name='acuser'),
    url(r'^setacemail/$','setacemail',name='setacemail'),
    url(r'^regsetemail/$','regsetemail',name='regsetemail'),
    url(r'^newpassword/$','newpassword',name='newpassword'),
    url(r'^suindex/$','suindex',name='suindex'),
    url(r'^passwordsuccess/$','passwordsuccess',name='passwordsuccess'),
    url(r'^passwordfail/$','passwordfail',name='passwordfail'),



)
