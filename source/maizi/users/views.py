#coding:utf-8
from django.shortcuts import render,redirect,render_to_response
from django.views.decorators.csrf import csrf_exempt
from common.models import *
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponse
from django.core.serializers import serialize
from PIL import Image, ImageDraw, ImageFont
from maizi_website.settings import  BASE_DIR
import  datetime
import base64
import json
from django.core.mail import EmailMultiAlternatives
import cStringIO, string, os, random
# Create your views here.
# 首页
def index(request):
    return render(request, "common/index.html", locals())

def suindex(request):
    return render(request, "common/../../templates/users/success.html", locals())
# Create your views here.
#验证码
def captcha1(request):
    '''Captcha1'''
    try:
        image = Image.new('RGB', (147, 49), color = (255, 255, 255)) # model, size, background color
        font_file = os.path.join(settings.BASE_DIR, 'static/fonts/Arial.ttf') # choose a font file
        font = ImageFont.truetype(font_file, 47) # the font object
        draw = ImageDraw.Draw(image)
        rand_str = ''.join(random.sample(string.letters + string.digits, 4)) # The random string
        draw.text((7, 0), rand_str, fill=(0, 0, 0), font=font) # position, content, color, font
        del draw
        #request.session['captcha'] = rand_str.lower() # store the content in Django's session store
        request.session['captcha'] = rand_str         # store the content in Django's session store
        print (rand_str)
        buf = cStringIO.StringIO() # a memory buffer used to store the generated image
        image.save(buf, 'jpeg')
    except Exception as e:
        print(e)
    return HttpResponse(buf.getvalue(), 'image/jpeg') # return the image data stream as image/jpeg format, browser will treat it as an image

#登录
@csrf_exempt
def re_login(request):
    try:
       if request.method == 'POST':
            email=request.POST.get('email')
            password=request.POST.get('password')
            result={"code":"success","message":"登录成功"}
            user = authenticate(email=email, password=password)
            if user:
                    request.session['email'] = user.email
                    if user.is_active:
                        user.backend = 'users.auth.CustomBackend' # 指定自定义的登录验证方式
                        login(request, user)
                    else:
                        result['code']='notemail'
                        result['message']='邮箱未激活'
                        return HttpResponse(json.dumps(result), content_type="application/json")
            else:
                    result['code']='failure'
                    result['message']='账号密码不正确'
                    return HttpResponse(json.dumps(result), content_type="application/json")
    except Exception as e:
       print (e)
    print ('kkkk')
    return HttpResponse(json.dumps(result), content_type="application/json")

#注销
def re_logout(request):
  try:
    logout(request)
  except Exception as e:
      print (e)
  return redirect(request.META['HTTP_REFERER'])

#注册 注册信息写入到DB中 ，但未激活
@csrf_exempt
def reg(request):
    try:
         email=request.POST.get('email')
         capt=request.POST.get('capt')
         sessioncapt=request.session['captcha']
         username=email.split('@')[0]
         password=make_password(request.POST.get('password'))
         result={"code":"failure","message":"账号已注册"}
         us=UserProfile.objects.filter(email=email)
         if capt.lower()==sessioncapt.lower():
             if not us:
                 user=UserProfile.objects.create(email=email,username=username,password=password,is_active=False)
                 user.save()
                 request.session['email']=email
                 result['code']='success'
                 result['message']='账号可以注册'

                 return HttpResponse(json.dumps(result), content_type="application/json")
         else:
                 result['code']='failure'
                 result['message']='验证码不正确'
                 return HttpResponse(json.dumps(result), content_type="application/json")
    except Exception as e:
        print(e)
    return HttpResponse(json.dumps(result), content_type="application/json")

#注册激活用户
def regsetemail(request):
                try:
                    email=request.GET.get('baemail')
                    useremail=base64.b64decode(email)
                    user=UserProfile.objects.get(email=useremail)

                    if user:
                        user.is_active=True
                        user.save()
                        #激活页面
                       # baemail=base64.encodestring(useremail)
                       # EmailVerifyRecord.objects.filter(email=baemail).delete()

                        return render(request, "users/success.html", locals())
                except Exception as e:
                        print (e)
                        #   获取ip地址
        #       发送邮件成功了给管理员发送一个反馈
        #         mail_admins(u'用户注册反馈', u'当前XX用户注册了该网站', fail_silently=True)
                return render(request, "users/worng.html", locals())

#找回密码
@csrf_exempt
def forgetpass(request):
    try:
                try:
                    email=request.POST.get('email')
                    result={'code':'success'}
                    user=UserProfile.objects.get(email=email)
                    if user:
                      request.session['email'] = user.email
                    if user.is_active==False:
                        result['code']='notemail'
                        result['message']='邮箱未激活'
                        return HttpResponse(json.dumps(result), content_type="application/json")

                except UserProfile.DoesNotExist as e:
                        result={'code':'failure'}
                        return HttpResponse(json.dumps(result), content_type="application/json")
                        #   获取ip地址
        #       发送邮件成功了给管理员发送一个反馈
        #         mail_admins(u'用户注册反馈', u'当前XX用户注册了该网站', fail_silently=True)
    except Exception as e:
        print(e)
    return HttpResponse(json.dumps(result), content_type="application/json")

#重置密码
@csrf_exempt
def newpassword(request):
    try:
        email=request.POST.get('email')
        password1= request.POST.get('password')
        password = make_password(password1)
        UserProfile.objects.filter(email=email).update(password=password)
        baemail=base64.encodestring(email)
        #EmailVerifyRecord.objects.filter(email=baemail).delete()
        result={'code':'success'}
        return HttpResponse(json.dumps(result), content_type="application/json")
    except Exception as e:
        result={'code':'failure'}
        return HttpResponse(json.dumps(result), content_type="application/json")
    return HttpResponse(json.dumps(result), content_type="application/json")

#重置密码成功
def passwordsuccess(request):
  return render(request, "users/success.html", locals())

#重置密码失败
def passwordfail(request):
  return render(request, "users/resfail.html", locals())

#跳转到提示激活邮件
def acuser(request):
      if request.META.has_key('HTTP_X_FORWARDED_FOR'):
                   ip =  request.META['HTTP_X_FORWARDED_FOR']
      else:
                   ip = request.META['REMOTE_ADDR']
      email=request.session['email']
      type=0
      request.session['type']=0
      setEmail(ip,email,type)
    #  return render(request, "common/../../templates/users/emailvaildate.html", locals())
      return render(request, "users/emailvaildate.html", locals())

# 发送找回密码邮件
def setacemail(request):
    try:
        if request.META.has_key('HTTP_X_FORWARDED_FOR'):
                       ip =  request.META['HTTP_X_FORWARDED_FOR']
        else:
                       ip = request.META['REMOTE_ADDR']
        email=request.session['email']
        type=1
        request.session['type']=1
        setEmail(ip,email,type)
    except Exception as e:
        pass
    return render(request, "users/emailvaildate.html", locals())

#发邮件
def setEmail(ip,email,type):
    try :
        baemail=base64.encodestring(email)
        uemail=EmailVerifyRecord.objects.create(ip=ip,email=baemail,type=type)
        uemail.save()
        if type==1:
             email_url="http://127.0.0.1:8000/users/resetpassword?baemail="+baemail
             subject='找回密码'
             html_content = u'<b>请点击链接重置密码：</b><p> '+email_url+ \
                               u'<p><b>(该链接在24小时内有效)</b> <p>' \
                               u'<b>如果上面不是链接形式，请将地址复制到您的浏览器(例如IE)的地址栏再访问。</b>'
        else:
            email_url="http://127.0.0.1:8000/users/regsetemail?baemail="+baemail
            subject='账号激活'
            html_content = u'<b>请点击链接激活：</b><p> '+email_url+ \
                               u'<p><b>(该链接在24小时内有效)</b> <p>' \
                               u'<b>如果上面不是链接形式，请将地址复制到您的浏览器(例如IE)的地址栏再访问。</b>'
        form_email,to = '1014332782@qq.com',email
        text_content = 'This is an important message'
        msg = EmailMultiAlternatives(subject,text_content,form_email,[to])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
    except Exception as e:
        print (e)

#获取邮件链接提取邮箱 验证链接是否过期
def go_resetpassword_html(request):
    try:
        email=request.GET.get('baemail')
        useremail=base64.b64decode(email)
        baemail=base64.encodestring(useremail)
        uemail=EmailVerifyRecord.objects.filter(email=baemail).order_by('-created')[0]
        print (uemail)
        datetime1=datetime.datetime.now()
        datetime2=uemail.created
        if(strtime2second(datetime1,datetime2)):
            return render(request, "users/resetpassword.html", locals())
        else:
             return render(request, "users/resetpasswordfail.html", locals())
    except Exception as e:
        print (e)
    return render(request, "users/resetpasswordfail.html", {'useremail':useremail})

#计算时间差不超过24h
def strtime2second(datetime1,datetime2):
    try:
        #datetime 转换 str
        dts1=datetime1.strftime("%Y-%m-%d %H:%I:%S")
        dts2=datetime2.strftime("%Y-%m-%d %H:%I:%S")

        import re;
        dt1= re.sub("[^\d]", "",dts1 )
        dt2= re.sub("[^\d]", "",dts2 )

        dint1=int(dt1[0:8])
        dint2=int(dt2[0:8])

        if(dint1-dint2>1):
            return False
        else:
            s=datetime.datetime.strptime(dts1,"%Y-%m-%d %H:%I:%S")
            s1=datetime.datetime.strptime(dts2,"%Y-%m-%d %H:%I:%S")
            if((s-s1).seconds>86400):
                return False
            else:
                return True
    except Exception as e:
        print(e)
        return False

def su(request):
     return render(request, "users/resetpassword.html", locals())

def convert_to_dicts(objs):
  '''把对象列表转换为字典列表'''
  obj_arr = []
  for o in objs:
    #把Object对象转换成Dict对象
    dict = {}
    dict.update(o.__dict__)
    obj_arr.append(dict)
  return obj_arr

def class_to_dict(obj):
  '''把对象(支持单个对象、list、set)转换成字典'''
  is_list = obj.__class__ == [].__class__
  is_set = obj.__class__ == set().__class__
  if is_list or is_set:
    obj_arr = []
    for o in obj:
      #把Object对象转换成Dict对象
      dict = {}
      dict.update(o.__dict__)
      obj_arr.append(dict)
    return obj_arr
  else:
    dict = {}
    dict.update(obj.__dict__)
    return dict

def a(request):

    user=UserProfile.objects.get(pk=1)
    us= class_to_dict(user)
    #json.dumps(us)
    #print( json.dumps(us))
   # json_object = simplejson.dumps( us )
    print(us)
    return render(request, "common/base.html", locals())



def setemail(request):
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
                   ip =  request.META['HTTP_X_FORWARDED_FOR']
    else:
                   ip = request.META['REMOTE_ADDR']
    email=request.session['email']
    ip=request.GET.get('type')
    setEmail(ip,email,type)

'''

@csrf_exempt
def login(request ):
 try:
    email=request.POST.get('email')
    password=request.POST.get('password')
    result={"code":"success","message":"登录成功"}
    try:
            user=UserProfile.objects.get(email=email)

    except UserProfile.DoesNotExist:
             result['code']='failure'
             result['message']='用户不存在'
             return HttpResponse(json.dumps(result), content_type="application/json")
    if(not  user.check_password(password)):
             print (user.check_password(password))
             result['code']='failure'
             result['message']='密码不正确'
             return HttpResponse(json.dumps(result), content_type="application/json")
    request.session['user']=user.username
    request.session['uuid']=user.id
    request.session['email']=user.email
 except Exception :
       pass
 return HttpResponse(json.dumps(result), content_type="application/json")
 '''

'''
@csrf_exempt
def login(request ):
    try:
           # email=request.POST.get('email')
            #password=request.POST.get('password')
            #result={"code":"success","message":"登录成功"}
            sd='dailinchuan@qq.com'
            ps='0206shuai'
            user=authenticate(username=sd, password=ps)
            print (user)
           # if user.code:
            if user is not None:
              #  result['code']=user.code
                print(user)
                user.backend = 'users.auth.CustomBackend'
                print(user)
                login(request, user)
                print(user)
               # user.backend = 'django.contrib.auth.backends.ModelBackend' # 指定自定义的登录验证方式
                #print (user.code)
               # print (user.username)
                #print(user.email)
                #print (user.password)
pp.auth.CustomBackend' # 指定自定义的登录验证方式
              #  print (result['message'])
              #  login(request, user)
               # request.session['email'] = user.email
                #snemail = request.session['email']

                #return render(request, 'commbn/base.html', locals())

    except Exception as e:
        pass
    print ('ssss')
    return render(request, 'common/index.html', locals())
'''
