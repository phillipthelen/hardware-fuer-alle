from fileupload.models import MultiuploaderImage
from django.views.generic import CreateView, DeleteView
from hardware.models import Hardware
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import UploadedFile

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

import logging
log = logging
from django.shortcuts import get_object_or_404, render_to_response

#importing json parser to generate jQuery plugin friendly json response
from django.utils import simplejson

#for generating thumbnails
#sorl-thumbnails must be installed and properly configured
from sorl.thumbnail import get_thumbnail


from django.views.decorators.csrf import csrf_exempt

import logging
log = logging

def response_mimetype(request):
    if "application/json" in request.META['HTTP_ACCEPT']:
        return "application/json"
    else:
        return "text/plain"

class PictureCreateView(CreateView):
    model = MultiuploaderImage

    def form_valid(self, form):
        self.object = form.save()
        f = self.request.FILES.get('file')
        data = [{'name': f.name, 'url': settings.MEDIA_URL + "pictures/" + f.name.replace(" ", "_"), 'thumbnail_url': settings.MEDIA_URL + "pictures/" + f.name.replace(" ", "_"), 'delete_url': reverse('upload-delete', args=[self.object.id]), 'delete_type': "DELETE"}]
        response = JSONResponse(data, {}, response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response


class PictureDeleteView(DeleteView):
    model = MultiuploaderImage

    def delete(self, request, *args, **kwargs):
        """
        This does not actually delete the file, only the database record.  But
        that is easy to implement.
        """
        self.object = self.get_object()
        self.object.delete()
        if request.is_ajax():
            response = JSONResponse(True, {}, response_mimetype(self.request))
            response['Content-Disposition'] = 'inline; filename=files.json'
            return response
        else:
            return HttpResponseRedirect('/upload/new')

class JSONResponse(HttpResponse):
    """JSON response class."""
    def __init__(self,obj='',json_opts={},mimetype="application/json",*args,**kwargs):
        content = simplejson.dumps(obj,**json_opts)
        super(JSONResponse,self).__init__(content,mimetype,*args,**kwargs)

@csrf_exempt
def multiuploader(request):
    """
Main Multiuploader module.
Parses data from jQuery plugin and makes database changes.
"""
    if request.method == 'POST':
        print request.POST
        print request.FILES
        log.info('received POST to main multiuploader view')
        if request.FILES == None:
            return HttpResponseBadRequest('Must have files attached!')
        #getting file data for farther manipulations
        file = request.FILES['file']
        wrapped_file = UploadedFile(file)
        filename = wrapped_file.name
        file_size = wrapped_file.file.size
        log.info ('Got file: "%s"' % str(filename))
        log.info('Content type: "$s" % file.content_type')

        #writing file manually into model
        #because we don't need form of any type.
        image = MultiuploaderImage()
        image.filename=str(filename)
        image.caption = request.POST["caption[]"]
        hardware = get_object_or_404(Hardware, id=request.POST["hardwareid"])
        if hardware.owner != request.user:
            return HttpResponse('fak u')
        image.hardware = hardware
        image.image=file
        image.key_data = image.key_generate
        image.save()
        log.info('File saving done')

        #getting thumbnail url using sorl-thumbnail
        if 'image' in file.content_type.lower():
            im = get_thumbnail(image, "80x80", quality=50)
            thumb_url = im.url
        else:
            thumb_url = ''

        #settings imports
        try:
            file_delete_url = settings.MULTI_FILE_DELETE_URL+'/'
            file_url = settings.MULTI_IMAGE_URL+'/'+image.key_data+'/'
        except AttributeError:
            file_delete_url = 'multi_delete/'
            file_url = 'multi_image/'+image.key_data+'/'

        #generating json response array
        result = []
        result.append({"name":filename,
                    "caption":image.caption,
                       "size":file_size,
                       "url":file_url,
                       "thumbnail_url":thumb_url,
                       "delete_url":file_delete_url+str(image.pk)+'/',
                       "delete_type":"POST",})
        response_data = simplejson.dumps(result)
        
        #checking for json data type
        #big thanks to Guy Shapiro
        if "application/json" in request.META['HTTP_ACCEPT_ENCODING']:
            mimetype = 'application/json'
        else:
            mimetype = 'text/plain'
        return HttpResponse(response_data, mimetype=mimetype)
    else: #GET
        return HttpResponse('Only POST accepted')