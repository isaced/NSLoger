# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response,render,HttpResponseRedirect
from django.http import Http404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.urlresolvers import reverse

from models import Topic,Comment,Category,Node
from bbs.forms import ReplyForm, TopicForm, EditForm

from NSLoger.settings import NUM_TOPICS_PER_PAGE

def index(request):
    '''首页'''
    topic_list = Topic.objects.all().order_by('-updated_on')[:NUM_TOPICS_PER_PAGE]

    nodes = []
    categor_list = Category.objects.all()
    for category in categor_list:
        node = {}
        category_nodes = Node.objects.filter(category=category.id)
        node['category_name'] = category.name
        node['category_nodes'] = category_nodes
        nodes.append(node)

    return render(request,"bbs/index.html",{'topic_list':topic_list,'nodes':nodes})

def recent(request):
    topic_list = Topic.objects.all().order_by('-updated_on')
    paginator = Paginator(topic_list, NUM_TOPICS_PER_PAGE)
    page = request.GET.get('page')
    
    try:
        topic_list = paginator.page(page)
    except PageNotAnInteger:
        topic_list = paginator.page(1)
    except EmptyPage:
        topic_list = paginator.page(paginator.num_pages)

    return render_to_response("bbs/recent.html",{"topic_list":topic_list});

def topic(request,topic_id):
    '''主题详情'''

    try:
        topic = Topic.objects.get(id=topic_id)
    except Topic.DoesNotExist:
        raise Http404

    topic.num_views += 1
    topic.save()

    comment_list = Comment.objects.filter(topic=topic).order_by('created_on')

    form = ReplyForm()
    return render(request,"bbs/topic.html",{'topic':topic,'comment_list':comment_list,'form':form})

@login_required
def reply(request, topic_id):
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            try:
                topic = Topic.objects.get(id=topic_id)
            except Topic.DoesNotExist:
                raise Http404
            comment.topic = topic
            comment.save()
            
            topic.num_comments += 1
            topic.updated_on = timezone.now()
            # topic.last_reply = request.user
            topic.save()

    return HttpResponseRedirect(reverse("bbs:topic" ,args=(topic_id,)))

def node(request, node_slug):
    '''节点页'''

    try:
        node = Node.objects.get(slug=node_slug)
    except Node.DoesNotExist:
        raise Http404

    topic_list = Topic.objects.filter(node=node).order_by('-updated_on')
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
    
    if request.method == 'GET':
        form = TopicForm()
        context['node'] = node
        context['form'] = form
        return render(request,'bbs/new.html',context)
    
    form = TopicForm(request.POST)
    if form.is_valid():
        topic = form.save(commit=False)
        topic.node = node
        topic.author = request.user
        # topic.last_reply = request.user
        topic.updated_on = timezone.now()
        topic.save()
        # node.num_topics += 1
        node.save()
        
    return HttpResponseRedirect(reverse("bbs:node" ,args=(node_slug,)))