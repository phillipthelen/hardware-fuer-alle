from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from main.models import Location

class UserProfile(models.Model):
	# This field is required.
	user = models.OneToOneField(User)

	location = models.ForeignKey(Location, null=True)

	displayLocation = models.BooleanField(_('display location'), default=False)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)