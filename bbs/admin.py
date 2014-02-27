from django import forms
from django.contrib import admin
from bbs.models import Subject,Comment

admin.site.register(Subject)
admin.site.register(Comment)
