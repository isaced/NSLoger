# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response

from models import Subject,Comment

def index(request):
    '''首页'''
    subject_list = Subject.objects.all()
    return render_to_response("bbs/index.html",{'subject_list':subject_list})

def subject(request,subject_id):
    '''主题详情'''
    subject = Subject.objects.get(id=subject_id)
    if subject:
        reply_list = Comment.objects.filter(subject=subject)
        return render_to_response("bbs/subject.html",{'subject':subject,'reply_list':reply_list})
    else:
        return render_to_response("404.html")
