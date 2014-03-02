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

    return render(request, "people/settings.html", {
        "form": form,
        "user": user,
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
