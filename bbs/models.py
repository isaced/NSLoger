# -*- coding: utf-8 -*- 

from django.db import models
from django.contrib.auth.models import User

# --- Model Define ---

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

class Node(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(blank=True, null=True)
    category = models.ForeignKey(Category)

    def __unicode__(self):
        return self.name
    
class Topic(models.Model):
    title = models.CharField(max_length=100,verbose_name='标题')     
    content = models.TextField(verbose_name='内容')
    node = models.ForeignKey(Node,verbose_name='所属节点')
    author = models.ForeignKey(User,verbose_name='作者')
    num_views = models.IntegerField(default=0,verbose_name='浏览量')
    num_comments = models.IntegerField(default=0,verbose_name='评论数')
    datetime = models.DateTimeField(auto_now_add=True,verbose_name='发表时间')
    created_on = models.DateTimeField(auto_now_add=True,verbose_name='更新时间')
    updated_on = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return self.title

class Comment(models.Model):
    content = models.TextField(verbose_name='内容')
    author = models.ForeignKey(User,verbose_name='作者')
    topic = models.ForeignKey(Topic)
    created_on = models.DateTimeField(auto_now_add=True,verbose_name='评论时间')

    def __unicode__(self):
        return self.content