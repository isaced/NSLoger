from django.contrib import admin
from bbs.models import Topic,Comment,Category,Node

admin.site.register(Topic)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Node)
