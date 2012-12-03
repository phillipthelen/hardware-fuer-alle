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
	email = forms.EmailField(required=False)
	error_css_class = 'error'

"""
	def __init__(self, user, *args, **kwargs):
		super(UserSettingsForm, self).__init__(*args, **kwargs)
		print user
		self.user = user

	def clean_email(self):
		email = self.cleaned_data.get('email')
		print form
		username = form.user.username
		if email and User.objects.filter(email=email).exclude(username=username).count():
			raise forms.ValidationError(u'Email addresses must be unique.')
		return email"""

class EmailForm(forms.Form):
	email = forms.EmailField(required=True)
	error_css_class = 'error'