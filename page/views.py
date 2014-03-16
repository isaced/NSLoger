# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import Http404
from page.models import Page

def page(request, page_slug):
    try:
        page = Page.objects.get(slug=page_slug)
    except Page.DoesNotExist:
        raise Http404

    return render(request,"page/page.html",{"page":page})