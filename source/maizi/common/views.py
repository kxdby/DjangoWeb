#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2015/11/3
@author: yopoing
Common模块View业务处理。
"""

from django.shortcuts import render,HttpResponse
from common.models import *
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
import math
import json

# 首页
def index(request):
    ad=Ad.objects.all()
    media_url=settings.MEDIA_URL
    teacher_list=UserProfile.objects.filter(groups__name='老师')
    return render(request, "common/index.html", locals())

#获取搜索关键字
def get_rk(request):
    try:
          data=[]
          keword=RecommendKeywords.objects.all()
          for i in keword:
              data.append({'name':i.name})
    except Exception as e:
        print (e)
    print (data)
    return HttpResponse(json.dumps(data), content_type="application/json")

#查询课程
@csrf_exempt
def gc_kp(request):
    data = dict()
    keyword = request.POST.get("keyword", "")
    if keyword:
        career_course = CareerCourse.objects.filter(name__icontains=keyword).order_by("index")
        course = Course.objects.filter(name__icontains=keyword).order_by("index")
    else:
        career_course = CareerCourse.objects.all().order_by("index")
        course = Course.objects.all().order_by("index")
    data["career_course"] = []

    for i in career_course:
        data["career_course"].append({'name': i.name, 'course_color': i.course_color, 'id': i.id})
    data["course"] = []
    for i in course:
        data["course"].append({'name': i.name, 'course_color': i.course_color, 'id': i.id})
    data['code']='success'
    print (data)
    return HttpResponse(json.dumps(data), content_type="application/json")

# 分页代码
def get_page_start_and_end(page, pagesize):
    start = (page - 1) * pagesize
    end = page * pagesize
    return start, end

#获取
@csrf_exempt
def get_co(request):
    try:
        pagesize=8
        data = {'course':[],'code':'failure',"message":'','total_pages:':1,'page':1}
        container=request.POST.get('course_by')
        try:
          page = int(request.GET.get("page", 1))
          if page<=0:
              page=1
        except Exception as e:
             page = 1

        if(container=='hot'):
            total_count =Course.objects.filter(is_homeshow=1).count()
            total_pages = math.ceil(float(total_count) / pagesize)
            if page > total_pages:
                page = total_pages
            start, end = get_page_start_and_end(page, pagesize)
            course = Course.objects.filter(is_homeshow=1).order_by("-favorite_count", "index")[start:end]
            for i in course:
               data["course"].append({'name': i.name, 'img': str(i.image), 'count': i.student_count, 'id': i.id})
            data["message"]='查询成功'
            data['code']='success'
            data["total_pages"] = int(total_pages)
            data["current_page"] = page
        elif (container=='new'):

            total_count = Course.objects.filter(is_homeshow=1).count()
            total_pages = math.ceil(float(total_count) / pagesize)
            if page > total_pages:
                page = total_pages
            start, end = get_page_start_and_end(page, pagesize)
            course = Course.objects.filter(is_homeshow=1).order_by("-date_publish", "index")[start:end]

            for i in course:
                data["course"].append({'name':i.name,'img':str(i.image),'count':i.student_count,'id':i.id})
            data["total_pages"] = int(total_pages)
            data["current_page"] = page
            data["message"]='查询成功'
            data['code']='success'
        elif(container=='most'):
            total_count = Lesson.objects.all().values("course").annotate(total_play_count=Sum('play_count')).count()
            total_pages = math.ceil(float(total_count) / pagesize)
            if page > total_pages:
                page = total_pages
            start, end = get_page_start_and_end(page, pagesize)
            course = Lesson.objects.all().values("course__name", "course__student_count", "course__image",
              "course__id").annotate(total_play_count=Sum('play_count')).order_by( '-total_play_count')[start:end]

            for i in course:
               data["course"].append({'name':i['course__name'],'img':str(i['course__image']),'count':i['course__student_count'],'id':i['course__id']})
            data["total_pages"] = int(total_pages)
            data["current_page"] = page
            data["message"]='查询成功'
            data['code']='success'

        else:
            data["message"] = "ddd"
            data["course"]=[]
    except Exception as e:
       print (e)


    return HttpResponse(json.dumps(data), content_type="application/json")
#获取教师名单
@csrf_exempt
def get_teach(request,tea_id):
    try:
        media_url=settings.MEDIA_URL
        teacher=UserProfile.objects.get(pk=tea_id)
        co=Course.objects.filter(teacher=teacher)
        print (co)
    except Exception as e:
        print (e)
    return render(request, "common/teacher_course.html", locals())
