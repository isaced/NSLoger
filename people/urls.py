# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from people import views

urlpatterns = patterns('',
        url(r'^$', views.hello, name="index"),
        url(r'^register/$', views.register, name="register"),
        url(r'^login/$', views.login, name="login"),
        url(r'^logout/$', views.logout, name="logout"),
        url(r'^settings/$', views.profile, name="settings"),
        url(r'^password/$', views.password, name="password"),
        url(r'^(?P<uid>\d+)/$', views.user, name="user"),
        )
