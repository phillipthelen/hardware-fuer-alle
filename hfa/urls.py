# coding: utf-8 f
from django.conf.urls import patterns, include, url
from main.views import home
from users.views import error, login, profile, settings, confirmEmail, newEmail
from django.contrib import admin
from hardware.views import displayHardware, listAll, hardwareEdit, deleteHardware
from hfa.settings import DEBUG, MEDIA_ROOT

admin.autodiscover()

urlpatterns = patterns('',
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
    url(r'^accounts/confirm/(?P<confirmation_key>.*)$', confirmEmail),
    url(r'^accounts/newmail$', newEmail),
    url(r'^accounts/', include('allauth.urls')),
    
)

if DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^images/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': MEDIA_ROOT}))
