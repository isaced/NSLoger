# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response

from models import Topic,Comment,Category,Node

def index(request):
    '''首页'''
    topic_list = Topic.objects.all()

    nodes = []
    categor_list = Category.objects.all()
    for category in categor_list:
        node = {}
        category_nodes = Node.objects.filter(category=category.id)
        node['category_name'] = category.name
        node['category_nodes'] = category_nodes
        nodes.append(node)

    return render_to_response("bbs/index.html",{'topic_list':topic_list,'nodes':nodes})

def topic(request,topic_id):
    '''主题详情'''
    topic = Topic.objects.get(id=topic_id)
    if topic:
        comment_list = Comment.objects.filter(topic=topic)
        return render_to_response("bbs/topic.html",{'topic':topic,'comment_list':comment_list})
    else:
        return render_to_response("404.html")

def node(request, node_slug):
    '''节点页'''
    print node_slug
    node = Node.objects.get(slug=node_slug)
    topic_list = Topic.objects.filter(node=node).order_by('-updated_on')

    return render_to_response("bbs/node.html",{"node":node, "topic_list":topic_list})