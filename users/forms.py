from django import forms


class LocationForm(forms.Form):
	city = forms.CharField(max_length=200, required=False)
	street = forms.CharField(max_length=200, required=False)
	postcode = forms.CharField(max_length=5, required=False)
	displayLocation = forms.BooleanField(required=False)

class UserSettingsForm(forms.Form):
	email = forms.EmailField(required=False)
	avatar = forms.ImageField(required=False)

class EmailForm(forms.Form):
	email = forms.EmailField(required=True)