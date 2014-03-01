# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import Http404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from models import Topic,Comment,Category,Node

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

    return render_to_response("bbs/index.html",{'topic_list':topic_list,'nodes':nodes})

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

    return render_to_response("bbs/topic.html",{'topic':topic,'comment_list':comment_list})


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

    return render_to_response("bbs/node.html",{"node":node, "topic_list":topic_list})