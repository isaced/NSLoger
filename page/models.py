# -*- coding: utf-8 -*-
from django.db import models

class Page(models.Model):
    title = models.CharField(max_length=100,verbose_name='标题')
    slug = models.SlugField(max_length=100,verbose_name='url标识符')
    content = models.TextField(verbose_name='内容')
    num_views = models.IntegerField(default=0,verbose_name='浏览量')
    created_on = models.DateTimeField(auto_now_add=True,verbose_name='发表时间')
    updated_on = models.DateTimeField(blank=True, null=True,verbose_name='更新时间')

    def __unicode__(self):
        return self.title