# -*- coding: utf-8 -*-
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100,verbose_name='类别名称')

    def __unicode__(self):
        return self.name

class CoolSite(models.Model):
    name = models.CharField(max_length=100,verbose_name='站点名称')
    url = models.URLField(verbose_name='站点地址')
    description = models.TextField(blank=True,verbose_name='站点介绍')
    category = models.ForeignKey(Category,verbose_name='所属类别')
    created_on = models.DateTimeField(auto_now_add=True,verbose_name='添加时间')

    def __unicode__(self):
        return self.name