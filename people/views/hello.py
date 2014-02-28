# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
__all__ = ['hello']

def hello(request):
    return HttpResponse("Hello")
