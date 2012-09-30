from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

class UserProfile(models.Model):
	# This field is required.
	user = models.OneToOneField(User)
	
	latitude = models.DecimalField(max_digits=9, decimal_places=7,null=True)
	longitude = models.DecimalField(max_digits=9, decimal_places=7,null=True)
	city = models.CharField(_('city'), max_length=200, null=True)
	street = models.CharField(_('street'), max_length=200, null=True)
	postcode = models.CharField(_('postcode'), max_length=5, null=True)

	displayLocation = models.BooleanField(_('display location'), default=False)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)