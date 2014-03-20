# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from people.forms import ProfileForm, PasswordChangeForm
from people.models import Member
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse

import base64
import json

from django.conf import settings

SITE_URL = getattr(settings, "SITE_URL")

# ---Qiniu---
import qiniu.conf

qiniu.conf.ACCESS_KEY = ""
qiniu.conf.SECRET_KEY = ""

import qiniu.rs

bucket_name = 'nsloger'
# ---Qiniu---

__all__ = ['profile', 'password']


@csrf_protect
@login_required
def profile(request):
    user = request.user
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save(commit=True)
            messages.success(request, "设置已更新")
            return render(request, "people/settings.html", {"form": form})
    else:
        form = ProfileForm(instance=user)

    # Create Qiniu Upload Token
    key_name = 'avatar/' + user.username
    policy = qiniu.rs.PutPolicy(scope='%s:%s' % (bucket_name, key_name))
    policy.fsizeLimit = 1024 * 300
    policy.mimeLimit = "image/jpeg;image/png"
    policy.returnBody = '{"hash": $(etag), "key": $(key)}'
    policy.returnUrl = SITE_URL + reverse("user:upload_headimage")
    uptoken = policy.token()

    return render(request, "people/settings.html", {
        "form": form,
        "user": user,
        "uptoken":uptoken
        })


@csrf_protect
@login_required
def password(request):
    user = request.user

    if request.method == "POST":
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            data = form.clean()
            if user.check_password(data["old_password"]):
                user.set_password(data["password"])
                user.save()
                messages.success(request, "新密码设置成功！请重新登录")
                auth_logout(request)
                return HttpResponseRedirect(reverse("user:login"))
            else:
                messages.error(request,'当前密码输入错误')
                return render(request, "people/password.html", {"form": form})
    else:
        form = PasswordChangeForm()

    return render(request, "people/password.html", {
        "form": form,
        })

# 头像上传
@csrf_protect
@login_required
def upload_headimage(request):
    user = request.user
    
    if request.method == "GET":
        try:
            retstr = request.GET.get('upload_ret')
            retstr = retstr.encode("utf-8")
            dec = base64.urlsafe_b64decode(retstr)
            ret = json.loads(dec)
            if ret and ret['key']:
                request.user.avatar = ret['key']
                request.user.save()
            else:
                raise
            messages.success(request, '头像上传成功！')
        except:
            messages.error(request, '头像上传失败！')

    return HttpResponseRedirect(reverse("user:settings"))

# 头像删除
@csrf_protect
@login_required
def delete_headimage(request):
    user = request.user

    if user.avatar == None or user.avatar == '':
        messages.error(request, '亲，你还没上传头像呢！')
    else:
        ret, err = qiniu.rs.Client().delete(bucket_name, user.avatar)
        if err is not None:
            messages.error(request, '头像删除失败')
        else:
            user.avatar = ''
            user.save()
            messages.success(request, '头像删除成功')
    return HttpResponseRedirect(reverse("user:settings"))