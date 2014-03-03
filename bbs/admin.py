from django.contrib import admin
from bbs.models import Topic,Comment,Category,Node

class TopicAdmin(admin.ModelAdmin):
	list_display = ('title','created_on','node','author','num_comments','num_views')
	search_fields = ['title']
	list_filter = ('node__name',)

class CommentAdmin(admin.ModelAdmin):
	list_display = ('content', 'topic', 'author','created_on',)
	list_filter = ('topic__node__name',)

class NodeAdmin(admin.ModelAdmin):
	list_display = ('name', 'slug' , 'category' ,'created_on', 'updated_on', 'num_topics')

class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name',)


admin.site.register(Topic,TopicAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Node,NodeAdmin)
