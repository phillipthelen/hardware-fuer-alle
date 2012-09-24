# coding: utf-8 f
from django.conf.urls import patterns, include, url
from main.views import home
from users.views import done, logout, error, login, profile
from django.contrib import admin
from hardware.views import displayHardware, listAll

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hfa.views.home', name='home'),
    # url(r'^hfa/', include('hfa.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^$', home, name='home'),
    url(r'^login/$', login, name="login"),
    url(r'^accounts/done/$', done, name='done'),
    url(r'^accounts/error/$', error, name='error'),
    url(r'^accounts/logout/$', logout, name='logout'),
    url(r'^users/(?P<username>.*)$', profile, name='profile'),
    url(r'^hardware/view/(?P<id>.*)$', displayHardware, name="display hardware"),
    url(r'^hardware/$', listAll),
    url(r'^hardware/(?P<page>\d*)$', listAll),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('social_auth.urls')),
    
)
