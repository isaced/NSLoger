# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from people import views
import bbs

urlpatterns = patterns('',
        url(r'^register/$', views.register, name="register"),
        url(r'^login/$', views.login, name="login"),
        url(r'^logout/$', views.logout, name="logout"),
        url(r'^settings/$', views.profile, name="settings"),
        url(r'^password/$', views.password, name="password"),
        url(r'^(?P<uid>\d+)/$', views.user, name="user"),
        url(r'^au_top/$', views.au_top, name="au_top"),
        url(r'^follow/(?P<uid>\d+)/$', views.follow, name="follow"),
        url(r'^unfollow/(?P<uid>\d+)/$', views.un_follow, name="unfollow"),
        url(r'^following/$', views.following, name="following"),
        url(r'^topic/fav/$', bbs.views.fav_topic_list, name="faved_topic_list"),
        url(r'^topic/fav/(?P<topic_id>\d+)/$', bbs.views.fav_topic, name="fav_topic"),
        url(r'^topic/unfav/(?P<topic_id>\d+)/$', bbs.views.unfav_topic, name="unfav_topic"),
        )
