from django.db import models
import random
from hardware.models import Hardware
storage = 'hardware/'

class MultiuploaderImage(models.Model):
	"""Model for storing uploaded photos"""
	filename = models.CharField(max_length=60, blank=True, null=True)
	image = models.FileField(upload_to=storage)
	key_data = models.CharField(max_length=90, unique=True, blank=True, null=True)
	upload_date = models.DateTimeField(auto_now_add=True)
	caption = models.CharField(max_length=200,blank=True, null=True)
	hardware = models.ForeignKey(Hardware)

	@property
	def key_generate(self):
		"""returns a string based unique key with length 80 chars"""
		while 1:
			key = str(random.getrandbits(256))
			try:
				MultiuploaderImage.objects.get(key=key)
			except:
				return key

	def __unicode__(self):
		return self.image.name

	def delete(self, *args, **kwargs):
		# You have to prepare what you need before delete the model
		stor, path = self.image.storage, self.image.path
		# Delete the model before the file
		super(MultiuploaderImage, self).delete(*args, **kwargs)
		# Delete the file after the model
		stor.delete(path)