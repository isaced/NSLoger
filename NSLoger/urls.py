from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from bbs import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'NSLoger.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.index),
    url(r'^subject/(?P<subject_id>\d)/$', views.subject),
    url(r'^login/', views.login),
    url(r'^register/', views.register),
    url(r'^logout/', views.logout),
    url(r'^admin/', include(admin.site.urls)),
)