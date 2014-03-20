# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from people import views
import bbs

urlpatterns = patterns('',
        url(r'^register/$', views.register, name="register"),
        url(r'^login/$', views.login, name="login"),
        url(r'^logout/$', views.logout, name="logout"),
        url(r'^settings/$', views.profile, name="settings"),
        url(r'^settings/upload_headimage/$', views.upload_headimage, name="upload_headimage"),
        url(r'^settings/delete_headimage/$', views.delete_headimage, name="delete_headimage"),
        url(r'^password/$', views.password, name="password"),
        url(r'^user/(?P<uid>\d+)/$', views.user, name="user"),
        url(r'^user/(?P<uid>\d+)/topics/$', views.user_topics, name="user_topics"),
        url(r'^user/(?P<uid>\d+)/comments/$', views.user_comments, name="user_comments"),
        url(r'^users/$', views.au_top, name="au_top"),
        url(r'^follow/(?P<uid>\d+)/$', views.follow, name="follow"),
        url(r'^unfollow/(?P<uid>\d+)/$', views.un_follow, name="unfollow"),
        url(r'^my/following/$', views.following, name="following"),
        url(r'^my/fav/$', bbs.views.fav_topic_list, name="faved_topic_list"),
        url(r'^send_verified_email/$', views.send_verified_email, name="send_verified_email"),
        url(r'^email_verified/(?P<uid>\d+)/(?P<token>\w+)/$', views.email_verified, name="email_verified"),
        url(r'^find_password/$', views.find_password, name="find_pass"),
        url(r'^reset_password/(?P<uid>\d+)/(?P<token>\w+)/$', views.first_reset_password, name="first_reset_password"),
        url(r'^reset_password/$', views.reset_password, name="reset_password"),
        )
