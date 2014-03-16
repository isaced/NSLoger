# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from page import views


urlpatterns = patterns('',
        url(r'^(?P<page_slug>[\w-]+)/$',views.page,name="page"),
        )
