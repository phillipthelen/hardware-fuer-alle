# coding: utf-8 f
from django.conf.urls import patterns, include, url
from main.views import home
from users.views import error, login, profile, settings
from django.contrib import admin
from hardware.views import displayHardware, listAll, hardwareEdit, deleteHardware

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hfa.views.home', name='home'),
    # url(r'^hfa/', include('hfa.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^$', home, name='home'),
    url(r'^users/(?P<id>.*)/(?P<username>.*)$', profile, name='profile'),
    url(r'^settings/$', settings, name='settings'),
    url(r'^hardware/view/(?P<id>.*)/(?P<name>.*)$', displayHardware, name="display hardware"),
    url(r'^hardware/new/$', hardwareEdit),
    url(r'^hardware/edit/(?P<id>.*)$', hardwareEdit),
    url(r'^hardware/delete/(?P<id>.*)$', deleteHardware),
    url(r'^hardware/$', listAll),
    url(r'^hardware/(?P<page>\d*)$', listAll),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    
)
