__author__ = 'jeffrey.dambly'

from django.conf.urls import patterns, url
from vips import views

urlpatterns = patterns('',
                       url(
                           regex=r'^$',
                           view=views.IndexView.as_view(),
                           name='index'
                       ),
                       url(
                           regex=r'^devices/$',
                           view=views.DeviceList.as_view(),
                           name='devices'
                       ),
                       url(
                           regex=r'^device/create/$',
                           view=views.CreateDevice.as_view(),
                           name='createdevice'
                       ),
                       url(
                           regex=r'device/(?P<pk>\d+)>/delete',
                           view=views.DeleteDevice.as_view(),
                           name='deletedevice'
                       ),
                       url(
                           regex=r'device/admin/$',
                           view=views.AdminView.as_view(),
                           name='deviceadmin'
                       ),
                       url(
                           regex=r'vip/(?P<pk>\d+)/members',
                           view=views.MemberView.as_view(),
                           name='members'
                       ),
)
