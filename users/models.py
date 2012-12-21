from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from main.models import Location
from sorl.thumbnail import ImageField
from hfa.util import get_afile_name

class UserProfile(models.Model):
	# This field is required.
	user = models.OneToOneField(User)

	location = models.ForeignKey(Location, null=True)
	displayLocation = models.BooleanField(_('display location'), default=False)

	displayname = models.CharField(max_length=50, blank=False)

	avatar = ImageField(upload_to=get_afile_name, null=True, blank=True)

	confirmation_key = models.CharField(max_length=40, blank=True, null=True)
	key_expires = models.DateTimeField(blank=True, null=True)
	mail_confirmed = models.BooleanField(default=False)

	def delete(self, *args, **kwargs):
		# You have to prepare what you need before delete the model
		storage, path = self.avatar.storage, self.avatar.path
		# Delete the model before the file
		super(UserProfile, self).delete(*args, **kwargs)
		# Delete the file after the model
		storage.delete(path)

def create_user_profile(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.create(user=instance, displayname=instance.username)

post_save.connect(create_user_profile, sender=User)
