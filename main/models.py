from django.db import models
from django.utils.translation import ugettext_lazy as _

class Location(models.Model):
	latitude = models.DecimalField(max_digits=9, decimal_places=7,null=True)
	longitude = models.DecimalField(max_digits=9, decimal_places=7,null=True)
	city = models.CharField(_('city'), max_length=200, null=True)
	street = models.CharField(_('street'), max_length=200, null=True)
	postcode = models.CharField(_('postcode'), max_length=5, null=True)