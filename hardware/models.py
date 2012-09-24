# coding: utf-8 
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

class Condition(models.Model):
	name = models.CharField(_('name'), max_length=200)

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = _('condition')
		verbose_name_plural = _('condition')

class Category(models.Model):
	name = models.CharField(_('name'), max_length=200)

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = _('category')
		verbose_name_plural = _('category')

class State(models.Model):
	name = models.CharField(_('name'), max_length=200)

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = _('state')
		verbose_name_plural = _('state')

class Hardware(models.Model):
	name = models.CharField(_('name'), max_length=200)
	condition = models.ForeignKey(Condition, verbose_name = _('condition'), blank=False)
	category = models.ForeignKey(Category, verbose_name = _('category'), blank=False)
	description = models.TextField(_('description'))
	availability = models.BooleanField(_('availability'))
	state = models.ForeignKey(State, verbose_name = _('state'), blank=False)
	owner = models.ForeignKey(User, verbose_name = _('owner'), related_name='hardware_owner')
	lent_to = models.ForeignKey(User, verbose_name = _('lent to'), related_name='hardware_lent_to', blank=True, null=True)

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = _('hardware')
		verbose_name_plural = _('hardware')