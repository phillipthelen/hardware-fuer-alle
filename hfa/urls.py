# coding: utf-8 f
from django.conf.urls import patterns, include, url
from main.views import home, hardwareAbuse
from users.views import error, login, profile, settings, confirmEmail, newEmail, disconnect
from django.contrib import admin
from hardware.views import displayHardware, listHardware, listComponents, hardwareEdit, deleteHardware, sendMail, searchHardware, giveaway, takeback, new_images
from hfa.settings import DEBUG, MEDIA_ROOT
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()
admin.autodiscover()

urlpatterns = patterns('',
 url(r'^upload/', include('fileupload.urls')),
    url(r'^$', home, name='home'),
    url(r'^users/(?P<userid>.*)$', profile, name='profile'),
    url(r'^settings/$', settings, name='settings'),
    url(r'^hardware/view/(?P<id>.*)/(?P<name>.*)$', displayHardware, name="display hardware"),
    url(r'^hardware/giveaway/$', giveaway),
    url(r'^hardware/takeback/(?P<hardwareid>.*)', takeback),
    url(r'^hardware/new/$', hardwareEdit),
    url(r'^hardware/newimages/(?P<hardwareid>.*)$', new_images),
    url(r'^hardware/edit/(?P<id>.*)$', hardwareEdit),
    url(r'^hardware/delete/(?P<id>.*)$', deleteHardware),
    url(r'^hardware/contact/(?P<hardwareid>.*)$', sendMail),
    url(r'^hardware/search/$', searchHardware),
    url(r'^hardware/search/(?P<page>.*)$', searchHardware),
    url(r'^hardware/list/$', listHardware),
    url(r'^hardware/list/components/$', listComponents),
    url(r'^hardware/list/components/(?P<page>\d*)$', listComponents),
    url(r'^hardware/list/(?P<page>\d*)$', listHardware),
    url(r'^hardware/abuse/$', hardwareAbuse),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/confirm/(?P<confirmation_key>.*)$', confirmEmail),
    url(r'^accounts/newmail$', newEmail),
    url(r'^accounts/disconnect/(?P<socialacc>.*)$', disconnect),
    url(r'^accounts/', include('allauth.urls')),

    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
)

if DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^images/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': MEDIA_ROOT}))
