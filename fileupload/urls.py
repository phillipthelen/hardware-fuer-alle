from django.conf.urls.defaults import *
from fileupload.views import PictureCreateView, multiuploader, delete_image

urlpatterns = patterns('',
    (r'^delete/(?P<pk>\d+)$', delete_image),
    (r'^upload/$', multiuploader),
)

