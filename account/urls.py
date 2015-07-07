from django.conf.urls import patterns, url

from account import views
urlpatterns = patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'account/login.html'}, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    )