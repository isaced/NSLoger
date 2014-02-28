# -*- coding: utf-8 -*-

from django.http import HttpResponse


def login(request):
    return HttpResponse("login")
