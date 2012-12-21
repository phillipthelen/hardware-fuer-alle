 # -*- coding: utf-8 -*-
from django import forms
from hardware.models import Condition, Category, State
from django.utils.html import conditional_escape, escape
from django.utils.encoding import force_unicode

class SelectWithTitles(forms.Select):
	def __init__(self, *args, **kwargs):
		super(SelectWithTitles, self).__init__(*args, **kwargs)
		
		self.titles = {}

	def render_option(self, selected_choices, option_value, option_label):
		title_html = (option_label in self.titles) and \
			u' title="%s" ' % escape(force_unicode(self.titles[option_label])) or ''
		option_value = force_unicode(option_value)
		selected_html = (option_value in selected_choices) and u' selected="selected"' or ''
		return u'<option value="%s"%s%s>%s</option>' % (
			escape(option_value), title_html, selected_html,
			conditional_escape(force_unicode(option_label)))
pty_label=None
class ChoiceFieldWithTitles(forms.ChoiceField):
	widget = SelectWithTitles(attrs={"class":"span2", 'title':"Brauchst du das Gerät irgendwann wieder oder hast du selbst gar keine Verwendung mehr dafür?"})

	def __init__(self, choices=(), *args, **kwargs):
		choice_pairs = [(c[0], c[1]) for c in choices]
		super(ChoiceFieldWithTitles, self).__init__(choices=choice_pairs, *args, **kwargs)
		self.widget.titles = dict([(c[1], c[2]) for c in choices])

class HardwareForm(forms.Form):
	lendlengthtypes = (
		('1', 'Tag(e)'),
		('7', 'Woche(n)'),
		('30', 'Monat(e)'),
		('356', 'Jahr(e)')
	)
	error_css_class = 'error'
	namewidget=forms.TextInput(attrs={"class":"span3", 'title':"Gib den Namen deiner Hardware ein, am Besten einfach die Produktbezeichnung."})
	name = forms.CharField(max_length=200, widget=namewidget)
	descriptionwidget=forms.Textarea(attrs={"class":"span5", 'title':"Beschreibe deine Hardware: welche Macken und Eigenheiten erwarten einen neuen Besitzer eventuell? Was für Besonderheiten hat deine Hardware?"})
	description = forms.CharField(widget=descriptionwidget)
	conditionwidget=forms.Select(attrs={"class":"span2", 'title':"Wähle den Zustand ehrlich aus; du musst nichts besser ausgeben als es ist."})
	condition = forms.ModelChoiceField(queryset=Condition.objects.all(), empty_label=None, widget=conditionwidget)
	categorywidget=forms.Select(attrs={"class":"span2", 'title':"Wähle aus um was für ein Gerät es sich handelt."})
	category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label=None, widget=categorywidget)
	state = ChoiceFieldWithTitles()
	lendlengthwidget=forms.TextInput(attrs={"class":"span1", 'title':"Schätze ab, wann du das Gerät spätestens selbst wieder benötigen wirst."})
	lendlength = forms.IntegerField(required=False, widget=lendlengthwidget)
	lendlengthtypewidget = forms.Select(attrs={"class":"span2"})
	lendlengthtype = forms.ChoiceField(choices=lendlengthtypes, required=False, widget=lendlengthtypewidget)
	locationwidget=forms.CheckboxInput(attrs={'title':"Wo kann das Gerät abgeholt werden? Wenn du keinen Haken setzt wird einfach der Ort verwendet, den du in deinem Profil angegeben hast."})
	ownlocation = forms.BooleanField(required=False, widget=locationwidget)
	city = forms.CharField(max_length=200, required=False)
	postcode = forms.CharField(max_length=5, required=False)
	street = forms.CharField(max_length=200, required=False)


	def __init__(self, *args, **kwargs):
		super(HardwareForm, self).__init__(*args, **kwargs)

		choices = []
		for c in State.objects.all():
			choices.append((c.id, c.name, c.temporary))
		self.fields['state'] = ChoiceFieldWithTitles(choices = choices)


class SendmailForm(forms.Form):
	text = forms.CharField(widget=forms.Textarea)

class SimpleSearchForm(forms.Form):
	searchquery = forms.CharField(required=False)

class SearchForm(SimpleSearchForm):
	SORT_BY_CHOICES = (
		("", "Sortiere nach"),
		("name", "Name"),
		("owner", "Besitzer"),
		("condition", "Zustand"),
		("category", "Kategorie"),
		("state", "Art"),
		("distance", "Entfernung")
	)
	error_css_class = 'error'

	condition = forms.ModelChoiceField(queryset=Condition.objects.all(), empty_label="Zustand", required=False, widget=forms.Select(attrs={"class":"input-medium",}))
	category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Kategorie", required=False, widget=forms.Select(attrs={"class":"input-medium",}))
	state = forms.ModelChoiceField(queryset=State.objects.all(), empty_label="Art", required=False, widget=forms.Select(attrs={"class":"input-medium",}))
	sortby = forms.ChoiceField(choices=SORT_BY_CHOICES, required=False, widget=forms.Select(attrs={"class":"input-medium",}))

class LendForm(forms.Form):
	username = forms.CharField()