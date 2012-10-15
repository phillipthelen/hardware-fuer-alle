from django import forms
from hardware.models import Condition, Category, State

class HardwareForm(forms.Form):
	condition_choices = [(c.id, c.name) for c in Condition.objects.all()]
	category_choices = [(c.id, c.name) for c in Category.objects.all()]
	state_choices = [(c.id, c.name) for c in State.objects.all()]
	name = forms.CharField(max_length=200)
	description = forms.CharField(widget=forms.Textarea)
	condition = forms.ModelChoiceField(queryset=Condition.objects.all())
	category = forms.ModelChoiceField(queryset=Category.objects.all())
	state = forms.ModelChoiceField(queryset=State.objects.all())
	ownlocation = forms.BooleanField(required=False)
	city = forms.CharField(max_length=200, required=False)
	postcode = forms.CharField(max_length=5, required=False)
	street = forms.CharField(max_length=200, required=False)

class SendmailForm(forms.Form):
	text = forms.CharField(widget=forms.Textarea)