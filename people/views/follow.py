# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from people.models import Member, Follower
from django.views.decorators.csrf import csrf_protect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError


@csrf_protect
@login_required
def follow(request, uid):
    if request.method == "GET":
        return HttpResponseRedirect(reverse("bbs:index"))

    user_a = request.user
    try:
        user_b = Member.objects.get(pk=uid)
    except (Member.DoesNotExist, Follower.DoesNotExist):
        messages.error(request, "用户不存在")
        return HttpResponseRedirect(reverse("bbs:index"))

    if user_a.id == uid:
        messages.error(request, "不能关注自己")
        return HttpResponseRedirect(reverse("bbs:index"))


    try:
        follower = Follower.objects.create(user_a=user_a, user_b=user_b)
        follower.save()
        messages.success(request, u"关注用户 %s 成功" % user_b.username)
        return HttpResponseRedirect(reverse("user:user",args=(user_b.id,)))
    except IntegrityError:
        messages.error(request, u"你已经关注了用户 %s，不能重复关注" % user_b.username)
        return HttpResponseRedirect(reverse("user:user",args=(user_b.id,)))


@csrf_protect
@login_required
def un_follow(request, uid):
    if request.method == "GET":
        return HttpResponseRedirect(reverse("bbs:index"))

    user_a = request.user
    try:
        user_b = Member.objects.get(pk=uid)
        follower = Follower.objects.filter(user_a=user_a, user_b=user_b).first()
    except (Member.DoesNotExist, Follower.DoesNotExist):
        messages.error(request, u"用户不存在")
        return HttpResponseRedirect(reverse("bbs:index"))
    else:
        follower.delete()
        messages.success(request, u"取消关注用户 %s 成功" % user_b.username)
        return HttpResponseRedirect(reverse("user:user",args=(user_b.id,)))


@login_required
def following(request):
    following_list = Follower.objects.filter(user_a=request.user).all()
    print following_list
    print "test"
    return render(request, "people/following.html", locals())
