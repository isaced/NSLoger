# -*- coding: utf-8 -*-
import re
from django.shortcuts import render_to_response,render,HttpResponseRedirect
from django.http import Http404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.core.cache import cache

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

    # 主题列表
    topic_list = Topic.objects.all().order_by('-updated_on')[:NUM_TOPICS_PER_PAGE]

    # 节点导航
    nodes = cache.get('index_nodes')  #取缓存
    if not nodes:
        nodes = []
        categor_list = Category.objects.all()
        print request.path
        for category in categor_list:
            node = {}
            category_nodes = Node.objects.filter(category=category.id)
            node['category_name'] = category.name
            node['category_nodes'] = category_nodes
            nodes.append(node)
        cache.set('index_nodes',nodes,600); #10分钟刷新

    
    # 今日热议
    hot_topics = cache.get('index_hot_topics')  #取缓存
    if not hot_topics:
        now = timezone.now()
        start = now - datetime.timedelta(hours=23, minutes=59, seconds=59)
        hot_comments = Comment.objects.filter(created_on__gt=start).values('topic').annotate(count=Count('topic')).order_by('-count')[:10]
        hot_topics = []
        for comment in hot_comments:
            topic = Topic.objects.get(id=comment['topic'])
            hot_topics.append(topic)
        cache.set('index_hot_topics',hot_topics,300); #5分钟刷新

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
        # comment ---
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
        # comment ---
    except Topic.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            last_comment = Comment.objects.filter(author=request.user).order_by('-created_on')[:1]
            last_comment = last_comment.first()
            if last_comment and last_comment.content == form.clean()['content'] and ((timezone.now()-last_comment.created_on).seconds < 10):
                messages.error(request,'你是否正在尝试连续提交两次相同的回复？');
            else:
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
                team_name_pattern = re.compile('(?<=@)([0-9a-zA-Z_.]+)', re.UNICODE)
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

    return render(request,"bbs/topic.html",{"node":node,"topic":topic,"form":form,"comment_list":comment_list,'paginator':paginator})


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
            last_topic = Topic.objects.filter(author=request.user).order_by('-created_on')[:1]
            last_topic = last_topic.first()
            if last_topic and last_topic.title == form.clean()['title'] and ((timezone.now()-last_topic.created_on).seconds < 10):
                messages.error(request,'你是否正在尝试连续提交两次相同的内容？');
                return HttpResponseRedirect(reverse("bbs:topic" ,args=(last_topic.id,)))
            else:
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
def edit(request,topic_id):

    try:
        topic = Topic.objects.get(id=topic_id)
        if topic.author != request.user:
            raise Http404
    except Node.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic.title = form.clean()['title']
            topic.content = form.clean()['content']
            topic.updated_on = timezone.now()
            topic.save()
            return HttpResponseRedirect(reverse("bbs:topic" ,args=(topic.id,)))
    else:
        form = TopicForm(instance=topic)
    
    return render(request,'bbs/edit.html',{'topic':topic,'form':form})

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
