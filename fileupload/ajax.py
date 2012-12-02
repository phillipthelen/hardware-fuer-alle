from dajax.core import Dajax
from fileupload.models import MultiuploaderImage
from dajaxice.decorators import dajaxice_register
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from sorl.thumbnail import get_thumbnail
from django.utils import simplejson

@dajaxice_register
def get_images(request, hardwareid):
	images = MultiuploaderImage.objects.filter(hardware=hardwareid)
	result = []
	for image in images:
		file_size = image.image.size
		#getting thumbnail url using sorl-thumbnail
		im = get_thumbnail(image.image, "80x80", quality=50)
		thumb_url = im.url

		#settings imports
		file_delete_url = '/upload/delete/'
		file_url = '/images/'+str(image.image)
		result.append({"name":image.filename,
					"caption":image.caption,
					   "size":file_size,
					   "url":file_url,
					   "thumbnail_url":thumb_url,
					   "delete_url":file_delete_url+str(image.pk),
					   "delete_type":"POST",})
	return simplejson.dumps(result)