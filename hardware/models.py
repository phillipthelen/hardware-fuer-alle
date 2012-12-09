# coding: utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from main.models import Location
from django.template.defaultfilters import slugify
from hfa.util import get_hfile_name, get_cfile_name

class Condition(models.Model):
	"""Different conditions such as 'damaged', 'new', 'slightly used'"""
	name = models.CharField(_('name'), max_length=200)

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = _('condition')
		verbose_name_plural = _('condition')

class Category(models.Model):
	"""Categories such as 'smartphone', 'laptop', ..."""
	name = models.CharField(_('name'), max_length=200)
	icon = models.ImageField(upload_to=get_cfile_name)

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = _('category')
		verbose_name_plural = _('category')

class State(models.Model):
	"""Whether the owner wants to give the hardware away or lend it"""
	name = models.CharField(_('name'), max_length=200)
	temporary = models.BooleanField()

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = _('state')
		verbose_name_plural = _('state')

class Hardware(models.Model):
	"""The hardware itself"""
	name = models.CharField(_('name'), max_length=200)
	slug = models.SlugField(max_length=200)
	condition = models.ForeignKey(Condition, verbose_name = _('condition'), blank=False)
	category = models.ForeignKey(Category, verbose_name = _('category'), blank=False)
	description = models.TextField(_('description'))
	availability = models.BooleanField(_('availability'), default=True)
	state = models.ForeignKey(State, verbose_name = _('state'), blank=False)
	owner = models.ForeignKey(User, verbose_name = _('owner'), related_name='hardware_owner')
	lent_to = models.ForeignKey(User, verbose_name = _('lent to'), related_name='hardware_lent_to', blank=True, null=True)
	location = models.ForeignKey(Location, verbose_name = _('location'), null=True)
	lendlength = models.IntegerField(null=True, blank=True)

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = _('hardware')
		verbose_name_plural = _('hardware')

	def save(self):
		self.slug = slugify(self.name)
		super(Hardware, self).save()

class Image(models.Model):
	image = models.ImageField(upload_to=get_hfile_name)
	caption = models.TextField(max_length=400)
	hardware = models.ForeignKey(Hardware)

	@models.permalink
	def get_absolute_url(self):
		return ('upload-new', )

	def save(self, *args, **kwargs):
		self.slug = self.file.namer
		super(Image, self).save(*args, **kwargs)

	def delete(self, *args, **kwargs):
		self.image.delete(False)
		super(Image, self).delete(*args, **kwargs)