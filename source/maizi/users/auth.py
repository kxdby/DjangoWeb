# -*- coding:utf-8 -*-
from django.contrib.auth.backends import ModelBackend
from common.models import *

class CustomBackend(ModelBackend):#重写认证，继承ModelBackend

    def authenticate(self, email=None, password=None, **kwargs):
        try:
            #user = UserProfile.objects.get(phone=username)#电话验证，通过电话的查询对象
            user = UserProfile.objects.get(email=email)#如邮箱验证，改这里即可！！！！！！！！
            if user.check_password(password):#检查密码
                return user
        except UserProfile.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            pass
        return None
