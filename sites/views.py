# -*- coding: utf-8 -*-
from django.shortcuts import render
from sites.models import Category,CoolSite
from django.core.cache import cache

def index(request):

	categorys = cache.get('sites_categorys')  #取缓存
	if not categorys:
		category_list = Category.objects.all();
		categorys = []
		for category in category_list:
			sites = {
				'category_name':category.name,
				'category_sites':CoolSite.objects.filter(category=category)
				}
			categorys.append(sites)
		cache.set('sites_categorys',categorys,600)  #写缓存
		
	return render(request,'sites/index.html',{"categorys":categorys})