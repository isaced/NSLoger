# -*- coding: utf-8 -*-

from django.db import models
#from django.contrib.auth.models import User
from people.models import Member as User

# --- Model Define ---

class Comment(models.Model):
    content = models.TextField(max_length=200,verbose_name='内容')
    datetime = models.DateTimeField(auto_now_add=True,verbose_name='回复时间')
    user = models.ForeignKey(User,verbose_name='作者')
    def __unicode__(self):
        return "comment:" + self.user.username

class Subject(models.Model):
    title = models.CharField(max_length=50,verbose_name='标题')
    content = models.TextField(max_length=1000,verbose_name='内容')
    datetime = models.DateTimeField(auto_now_add=True,verbose_name='发表时间')
    comment = models.ManyToManyField(Comment,verbose_name='评论',blank=True)
    user = models.ForeignKey(User,verbose_name='作者')
    def __unicode__(self):
        return self.title
