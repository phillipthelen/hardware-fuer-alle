from django import forms
from hardware.models import Condition, Category, State

class HardwareForm(forms.Form):
	condition_choices = [(c.id, c.name) for c in Condition.objects.all()]
	category_choices = [(c.id, c.name) for c in Category.objects.all()]
	state_choices = [(c.id, c.name) for c in State.objects.all()]
	name = forms.CharField(max_length=200)
	description = forms.CharField(widget=forms.Textarea)
	condition = forms.ModelChoiceField(queryset=Condition.objects.all(), empty_label=None)
	category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label=None)
	state = forms.ModelChoiceField(queryset=State.objects.all(), empty_label=None)
	ownlocation = forms.BooleanField(required=False)
	city = forms.CharField(max_length=200, required=False)
	postcode = forms.CharField(max_length=5, required=False)
	street = forms.CharField(max_length=200, required=False)
	image1 = forms.ImageField(max_length=2000, required=False)
	caption1 = forms.CharField(max_length=400, required=False)

	image2 = forms.ImageField(max_length=2000, required=False)
	caption2 = forms.CharField(max_length=400, required=False)

	image3 = forms.ImageField(max_length=2000, required=False)
	caption3 = forms.CharField(max_length=400, required=False)

class SendmailForm(forms.Form):
	text = forms.CharField(widget=forms.Textarea)
