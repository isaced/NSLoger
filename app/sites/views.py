# -*- coding: utf-8 -*-
from django.shortcuts import render
from sites.models import Category,CoolSite

def index(request):
	category_list = Category.objects.all();
	categorys = []
	for category in category_list:
		sites = {
			'category_name':category.name,
			'category_sites':CoolSite.objects.filter(category=category)
			}
		categorys.append(sites)
		
	return render(request,'sites/index.html',{"categorys":categorys})