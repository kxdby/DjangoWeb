#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Django settings for maizi_website project.

Generated by 'django-admin startproject' using Django 1.8.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


MEDIA_ROOT =os.path.join(BASE_DIR, 'media')
MEDIA_URL ='/media/'
# app path settings
sys.path.insert(0, os.path.join(BASE_DIR, 'maizi'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 't*lquojw@0f)zn*8d*yzr*5c%51jbpik#xt78k!s!tv@)n%xg@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'common',
    'course',
    'users',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'maizi_website.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'maizi_website.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'maizidb',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

 #自定义的登录认证方式
AUTHENTICATION_BACKENDS = (
    'users.auth.CustomBackend',
   'django.contrib.auth.backends.ModelBackend',
)

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR,  'static'),
)




TEMPLATE_DIRS = (
    os.path.join(BASE_DIR,  'templates'),
)

# define
AUTH_USER_MODEL = "common.UserProfile"




#邮件配置
EMAIL_HOST = 'smtp.qq.com'                   #SMTP地
EMAIL_PORT =587                                  #SMTP端口
EMAIL_HOST_USER = '1014332782@qq.com'       #我自己的邮箱
EMAIL_HOST_PASSWORD = 'lfoxjezgyveobchf'                  #我的邮箱密码
#EMAIL_HOST_PASSWORD ='daowohao@2b'
EMAIL_SUBJECT_PREFIX = u'[CoorCar网]'            #为邮件Subject-line前缀,默认是'[django]'
EMAIL_USE_TLS = True                             #与SMTP服务器通信时，是否启动TLS链接(安全链接)。默认是false
#管理员站点
SERVER_EMAIL = 'daixueyu@139.com'