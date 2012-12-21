from django import forms
from hardware.models import Condition, Category, State
from django.utils.html import conditional_escape, escape
from django.utils.encoding import force_unicode

class ReportForm(forms.Form):
	description = forms.CharField(required=True, widget=forms.Textarea(attrs={"class":"span6"}))
	error_css_class = 'error'

class HardwareReportForm(ReportForm):
	object = forms.IntegerField()