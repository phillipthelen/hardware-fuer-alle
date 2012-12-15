 # -*- coding: utf-8 -*-
from django import forms
from django.core import validators
from django.contrib.auth.models import User

def isValidUsername(field_data):
		try:
			User.objects.get(username=field_data)
		except User.DoesNotExist:
			return
		raise validators.ValidationError('Der Benutzername {} ist bereits vergeben.'.format(field_data))

class LocationForm(forms.Form):
	city = forms.CharField(max_length=200, required=False)
	street = forms.CharField(max_length=200, required=False)
	postcode = forms.CharField(max_length=5, required=False)
	displayLocation = forms.BooleanField(required=False)
	error_css_class = 'error'

class UserSettingsForm(forms.Form):
	displayname = forms.CharField(max_length=50, required=True)
	email = forms.EmailField(required=True)
	error_css_class = 'error'

	def clean_email(self):
		value = self.cleaned_data["email"]
		errors = {
			"different_account": "Diese Adresse ist bereits mit einem anderen Benutzer verknüpft.",
		}
		emails = User.objects.filter(email__iexact=value)
		if emails.exclude(username = self.user).exists():
			raise forms.ValidationError(errors["different_account"])
		return value

class EmailForm(forms.Form):
	email = forms.EmailField(required=True)
	error_css_class = 'error'

	def __init__(self, user=None, *args, **kwargs):
		self.user = user
		super(EmailForm, self).__init__(*args, **kwargs)
		
	def clean_email(self):
		value = self.cleaned_data["email"]
		errors = {
			"different_account": "Diese Adresse ist bereits mit einem anderen Benutzer verknüpft.",
		}
		emails = User.objects.filter(email__iexact=value)
		if emails.exclude(user=self.user).exists():
			raise forms.ValidationError(errors["different_account"])
		return value