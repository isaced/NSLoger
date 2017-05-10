# -*- coding: utf-8 -*-
from django.conf.urls import url
from page import views


urlpatterns = [
        url(r'^(?P<page_slug>[\w-]+)/$',views.page,name="page"),
]
