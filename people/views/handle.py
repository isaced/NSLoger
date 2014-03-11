# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from people.forms import RegisterForm, LoginForm
from people.models import Member, Follower
from bbs.models import Topic, Comment
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import logout as auth_logout, authenticate, login as auth_login
from django.core.urlresolvers import reverse
from django.contrib import messages

from bbs.models import Topic
from NSLoger.settings import NUM_TOPICS_PER_PAGE,NUM_COMMENT_PER_PAGE

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

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

            #注册成功后自动登陆
            user = authenticate(email=data["email"], password=data["password"])
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
    return HttpResponseRedirect(reverse('bbs:index'))


def user(request, uid):
    user_from_id = Member.objects.get(pk=uid)
    user_a = request.user
    if user_a.is_authenticated():
        try:
            follower = Follower.objects.filter(user_a=user_a, user_b=user_from_id).first()
        except (Member.DoesNotExist, Follower.DoesNotExist):
            follower = None

    topic_list = Topic.objects.order_by("-created_on").filter(author=user_from_id.id)[:10]
    comment_list = Comment.objects.order_by("-created_on").filter(author=user_from_id)[:10]
    return render(request, "people/user.html", locals())

# 用户榜
def au_top(request):
    au_list = Member.objects.order_by('-au')[:20]
    user_count = Member.objects.all().count()
    return render(request, "people/au_top.html", locals())

# 用户个人页面 - 所有主题
def user_topics(request, uid):
    this_user = Member.objects.get(pk=uid)
    topic_list = Topic.objects.order_by("-created_on").filter(author=uid)
    paginator = Paginator(topic_list, NUM_TOPICS_PER_PAGE)
    page = request.GET.get('page')
    try:
        topic_list = paginator.page(page)
    except PageNotAnInteger:
        topic_list = paginator.page(1)
    except EmptyPage:
        topic_list = paginator.page(paginator.num_pages)

    return render(request, "people/user_topics.html", locals())

# 用户个人页面 - 所有回复
def user_comments(request, uid):
    this_user = Member.objects.get(pk=uid)
    comment_list = Comment.objects.order_by("-created_on").filter(author=uid)
    paginator = Paginator(comment_list, NUM_COMMENT_PER_PAGE)
    page = request.GET.get('page')
    try:
        comment_list = paginator.page(page)
    except PageNotAnInteger:
        comment_list = paginator.page(1)
    except EmptyPage:
        comment_list = paginator.page(paginator.num_pages)

    return render(request, "people/user_comments.html", locals())
