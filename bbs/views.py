# -*- coding: utf-8 -*-
import re
from django.shortcuts import render_to_response,render,HttpResponseRedirect
from django.http import Http404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.urlresolvers import reverse

from models import Topic,Comment,Category,Node,Notice, FavoritedTopic
from people.models import Member as User
from bbs.forms import ReplyForm, TopicForm, EditForm
from django.db import IntegrityError

from django.contrib import messages
from NSLoger.settings import NUM_TOPICS_PER_PAGE,NUM_COMMENT_PER_PAGE

import datetime
from django.db.models import Count 

def index(request):
    '''首页'''
    topic_list = Topic.objects.all().order_by('-created_on')[:NUM_TOPICS_PER_PAGE]

    nodes = []
    categor_list = Category.objects.all()
    print request.path
    for category in categor_list:
        node = {}
        category_nodes = Node.objects.filter(category=category.id)
        node['category_name'] = category.name
        node['category_nodes'] = category_nodes
        nodes.append(node)
    
    # 今日热议
    now = timezone.now()
    start = now - datetime.timedelta(hours=23, minutes=59, seconds=59)
    hot_comments = Comment.objects.filter(created_on__gt=start).values('topic').annotate(count=Count('topic')).order_by('-count')[:10]
    hot_topics = []
    for comment in hot_comments:
        topic = Topic.objects.get(id=comment['topic'])
        hot_topics.append(topic)

    return render(request,"bbs/index.html",{
        'topic_list':topic_list,
        'nodes':nodes,
        'hot_topics':hot_topics
        })

def recent(request):
    topic_list = Topic.objects.all().order_by('-created_on')
    paginator = Paginator(topic_list, NUM_TOPICS_PER_PAGE)
    page = request.GET.get('page')

    try:
        topic_list = paginator.page(page)
    except PageNotAnInteger:
        topic_list = paginator.page(1)
    except EmptyPage:
        topic_list = paginator.page(paginator.num_pages)

    return render(request,"bbs/recent.html",{"topic_list":topic_list});

def topic(request,topic_id):
    '''主题详情'''

    try:
        topic = Topic.objects.get(id=topic_id)
    except Topic.DoesNotExist:
        raise Http404

    topic.num_views += 1
    topic.save()

    faved_num = FavoritedTopic.objects.filter(topic=topic).count()

    if request.user.is_authenticated():
        try:
            faved_topic = FavoritedTopic.objects.filter(user=request.user, topic=topic).first()
        except (User.DoesNotExist, FavoritedTopic.DoesNotExist):
            faved_topic = None

    # Comment
    comment_list = Comment.objects.filter(topic=topic).order_by('created_on')
    paginator = Paginator(comment_list, NUM_COMMENT_PER_PAGE)
    page = request.GET.get('page')
    if page == None:
        page = paginator.num_pages

    try:
        comment_list = paginator.page(page)
    except PageNotAnInteger:
        comment_list = paginator.page(1)
    except EmptyPage:
        comment_list = paginator.page(paginator.num_pages)

    form = ReplyForm()
    return render(request,"bbs/topic.html", locals())

@login_required
def reply(request, topic_id):

    try:
        topic = Topic.objects.get(id=topic_id)
        comment_list = Comment.objects.filter(topic=topic).order_by('created_on')
    except Topic.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            request.user.comment_num += 1
            request.user.calculate_au()
            request.user.save()
            comment.author = request.user

            try:
                topic = Topic.objects.get(id=topic_id)
            except Topic.DoesNotExist:
                raise Http404

            comment.topic = topic
            comment.save()

            # --- 解析@ ---

            #team_name_pattern = re.compile('(?<=@)(\w+)', re.UNICODE)
            team_name_pattern = re.compile('(?<=@)([0-9a-zA-Z.]+)', re.UNICODE)
            at_name_list = set(re.findall(team_name_pattern, comment.content))
            if at_name_list:
                for at_name in at_name_list:
                    if at_name != comment.author.username and at_name != comment.topic.author.username:
                        try:
                            at_user = User.objects.get(username=at_name)
                            if at_user:
                                notice = Notice(from_user=comment.author,to_user=at_user    ,topic=comment.topic,content=comment.content)
                                notice.save()
                        except:
                            pass

            # --- 解析@ ---

            topic.num_comments += 1
            topic.updated_on = timezone.now()
            topic.last_reply = request.user
            topic.save()
            return HttpResponseRedirect(reverse("bbs:topic" ,args=(topic_id,)))
    else:
        form = ReplyForm()

    return render(request,"bbs/topic.html",{"node":node,"topic":topic,"form":form,"comment_list":comment_list})


def node(request, node_slug):
    '''节点页'''

    try:
        node = Node.objects.get(slug=node_slug)
    except Node.DoesNotExist:
        raise Http404

    topic_list = Topic.objects.filter(node=node).order_by('-created_on')
    paginator = Paginator(topic_list, NUM_TOPICS_PER_PAGE)
    page = request.GET.get('page')

    try:
        topic_list = paginator.page(page)
    except PageNotAnInteger:
        topic_list = paginator.page(1)
    except EmptyPage:
        topic_list = paginator.page(paginator.num_pages)

    return render(request,"bbs/node.html",{"node":node, "topic_list":topic_list})

@login_required
def new(request, node_slug):
    context = {}
    try:
        node = Node.objects.get(slug=node_slug)
    except Node.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.node = node
            request.user.topic_num += 1
            request.user.calculate_au()
            request.user.save()
            topic.author = request.user
            topic.last_reply = request.user
            topic.updated_on = timezone.now()
            topic.save()
            node.num_topics += 1
            node.save()

            # --- 解析@ ---

            team_name_pattern = re.compile('(?<=@)(\w+)', re.UNICODE)
            at_name_list = set(re.findall(team_name_pattern, topic.content))
            if at_name_list:
                for at_name in at_name_list:
                    if at_name != topic.author.username:
                        try:
                            at_user = User.objects.get(username=at_name)
                            if at_user:
                                notice = Notice(from_user=topic.author,to_user=at_user,topic=topic,content='')
                                notice.save()
                        except:
                            pass

            # --- 解析@ ---

            return HttpResponseRedirect(reverse("bbs:topic" ,args=(topic.id,)))
    else:
        form = TopicForm()

    return render(request,'bbs/new.html',{'node':node,'form':form})


@login_required
def notice(request):
    context = {}
    if request.method == 'GET':
        notices = Notice.objects.filter(to_user=request.user,is_deleted=False).order_by('-time')
        context['notices'] = notices

        return render(request,'bbs/notice.html',context)

@login_required
def notice_delete(request, notice_id):
    if request.method == 'GET':
        try:
            notice = Notice.objects.get(id=notice_id)
        except Notice.DoesNotExist:
            raise Http404
        notice.is_deleted = True
        notice.save()

    return HttpResponseRedirect(reverse("bbs:notice"))

def about(request):
    return render(request,'bbs/about.html')


@login_required
def fav_topic_list(request):
    faved_topic = FavoritedTopic.objects.filter(user=request.user).all()
    return render(request, 'bbs/fav_topic.html', locals())


@login_required
def fav_topic(request, topic_id):
    if request.method == "GET":
        return HttpResponseRedirect(reverse("bbs:index"))

    try:
        topic = Topic.objects.get(pk=topic_id)
        if FavoritedTopic.objects.filter(user=request.user, topic=topic).first():
            messages.error(request, u"主题已经关注了")
            return HttpResponseRedirect(reverse("bbs:index"))

        fav_topic_new = FavoritedTopic.objects.create(user=request.user, topic=topic)
        fav_topic_new.save()
    except Topic.DoesNotExist:
        messages.error(request, u"主题不存在")
        return HttpResponseRedirect(reverse("bbs:index"))

    #except IntegrityError:
        #messages.error(request, u"主题已经关注了")
        #return HttpResponseRedirect(reverse("bbs:index"))

    return HttpResponseRedirect(reverse("bbs:topic" ,args=(topic_id,)))


@login_required
def unfav_topic(request, topic_id):
    if request.method == "GET":
        return HttpResponseRedirect(reverse("bbs:index"))
    try:
        topic = Topic.objects.get(pk=topic_id)
        faved_topic = FavoritedTopic.objects.filter(user=request.user, topic=topic)
        faved_topic.delete()
    except Topic.DoesNotExist:
        messages.error(request, u"主题不存在")
        return HttpResponseRedirect(reverse("bbs:index"))

    return HttpResponseRedirect(reverse("bbs:topic", args=(topic_id,)))
