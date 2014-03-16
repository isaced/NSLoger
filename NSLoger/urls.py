from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'NSLoger.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^$', views.index),
    #url(r'^subject/(?P<subject_id>\d)/$', views.subject, name='subject'),
    #url(r'^user/(?P<user_id>\d)/$', views.user, name="user"),
    #url(r'^login/', views.login),
    #url(r'^register/', views.register),
    #url(r'^logout/', views.logout),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('bbs.urls', namespace='bbs')),
    url(r'^sites/', include('sites.urls', namespace='sites')),
    url(r'^', include('people.urls', namespace='user')),
    url(r'^', include('page.urls', namespace='page')),
)
