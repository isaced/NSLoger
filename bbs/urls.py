# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from bbs import views


urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^recent/?$',views.recent, name='recent'),
        url(r't/(\w+)/?$', views.topic, name="topic"),
        url(r'^node/(\w+)/?$',views.node,name="node"),
        )
