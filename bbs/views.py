# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger

from models import Subject,Comment
from django.contrib.auth.models import User

def index(request):
    '''首页'''
    subject_list = Subject.objects.all()
    return render_to_response("index.html",{'subject_list':subject_list})

def subject(request,subject_id):
    '''主题详情'''
    subject = Subject.objects.get(id=subject_id)
    if subject:
        reply_list = Comment.objects.filter(subject=subject)
        return render_to_response("subject.html",{'subject':subject,'reply_list':reply_list})
    else:
        return render_to_response("404.html")

def user(request,user_id):
    ''''用户信息'''
    user = User.objects.get(id=user_id)
    if user:
        sbject_list = Subject.objects.all()
        comment_list = Comment.objects.filter(user=user)
    return render_to_response("user.html",{"user":user,"subject_list":sbject_list,"comment_list":comment_list})

def login(request):
    '''登陆'''
    return HttpResponse("login")

def register(request):
    '''用户注册'''
    return HttpResponse("register")

def logout(request):
    '''注销'''
    return HttpResponse("logout")