# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from people.forms import RegisterForm, LoginForm
from people.models import Member
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import logout as auth_logout, authenticate, login as auth_login
from django.core.urlresolvers import reverse
from django.contrib import messages

__all__ = ['register', 'login', 'logout']

@csrf_protect
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.clean()
            new_user = Member.objects.create_user(username=data["username"],
                                                  email=data["email"],
                                                  password=data["password"])

            # Email 验证
            # TODO
            new_user.save()
            return HttpResponseRedirect(reverse("user:login"))

    else:
        form = RegisterForm()
    return render(request, 'people/register.html', {
        'form': form,
        })


@csrf_protect
def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.clean()
            # 邮箱
            username = data["username"]
            if '@' in username:
                email = username
            else:
                user = Member.objects.get(username=username)
                email = user.email

            user = authenticate(email=email, password=data["password"])
            if user is not None:
                auth_login(request, user)
                go = reverse("bbs:index")
                if request.session.get("next"):
                    go = request.session.pop("next")

                is_auto_login = request.POST.get('auto')
                if not is_auto_login:
                    request.session.set_expiry(0)
                return HttpResponseRedirect(go)
            else:
                messages.error(request, '密码不正确！')
                return render(request,'people/login.html',locals())
    else:
        form = LoginForm()

    if request.GET.get("next"):
        request.session["next"] = request.GET["next"]

    return render(request, 'people/login.html', {
        'form': form
        })


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('user:login'))


def user(request, uid):
    user = Member.objects.get(pd=uid)
    return render(request, "people/user.html", locals())
