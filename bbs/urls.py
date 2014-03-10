# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from bbs import views


urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^recent/?$',views.recent, name='recent'),
        url(r'^t/(?P<topic_id>\d+)/$', views.topic, name="topic"),
        url(r'^t/(\d+)/reply/?$',views.reply,name='reply'),
        url(r'^node/([\w-]+)/new/?$',views.new,name='new'),
        url(r'^node/(?P<node_slug>[\w-]+)/$',views.node,name="node"),
		url(r'^notice/?$',views.notice,name='notice'),
		url(r'^notice/(\d+)/delete/?$',views.notice_delete,name='notice_delete'),
        )
