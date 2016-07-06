#!/usr/bin/env python
# -*- coding: utf-8 -*-



from django.conf.urls import patterns, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('common.views',
    url(r'^$', 'index', name='index'),
    url(r'^get_rk/$', 'get_rk', name='get_rk'),
    url(r'^gc_kp/$', 'gc_kp', name='gc_kp'),
    url(r'^get_teach/(?P<tea_id>\d+)$', 'get_teach', name='get_teach'),
    url(r'^get_co/$', 'get_co', name='get_co'),
      )+static("/media/", document_root=settings.MEDIA_ROOT)

