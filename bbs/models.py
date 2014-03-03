# -*- coding: utf-8 -*-

from django.db import models
#from django.contrib.auth.models import User
from people.models import Member as User

# --- Model Define ---

class Category(models.Model):
    name = models.CharField(max_length=100,verbose_name='类别名称')

    def __unicode__(self):
        return self.name

class Node(models.Model):
    name = models.CharField(max_length=100,verbose_name='节点名称')
    slug = models.SlugField(max_length=100,verbose_name='url标识符')
    created_on = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    updated_on = models.DateTimeField(blank=True, null=True,auto_now=True,verbose_name='更新时间')
    num_topics = models.IntegerField(default=0,verbose_name='主题数')
    category = models.ForeignKey(Category,verbose_name='所属类别')

    def __unicode__(self):
        return self.name

class Topic(models.Model):
    title = models.CharField(max_length=100,verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    node = models.ForeignKey(Node,verbose_name='所属节点')
    author = models.ForeignKey(User,verbose_name='作者')
    num_views = models.IntegerField(default=0,verbose_name='浏览量')
    num_comments = models.IntegerField(default=0,verbose_name='评论数')
    last_reply = models.ForeignKey(User,related_name='+',verbose_name='最后回复者')
    datetime = models.DateTimeField(auto_now_add=True,verbose_name='发表时间')
    created_on = models.DateTimeField(auto_now_add=True,verbose_name='更新时间')
    updated_on = models.DateTimeField(auto_now=True,blank=True, null=True)

    def __unicode__(self):
        return self.title

class Comment(models.Model):
    content = models.TextField(verbose_name='内容')
    author = models.ForeignKey(User,verbose_name='作者')
    topic = models.ForeignKey(Topic,verbose_name='所属主题')
    created_on = models.DateTimeField(auto_now_add=True,verbose_name='评论时间')

    def __unicode__(self):
        return self.content
