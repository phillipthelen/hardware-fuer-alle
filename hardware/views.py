from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext, loader, Context
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.contrib.messages.api import get_messages
from django.contrib.auth.models import User
from hardware.models import Hardware, Category, Condition, State
from django.core.paginator import Paginator, InvalidPage, EmptyPage
import hfa.util
from django import forms
from django.core.urlresolvers import reverse

class HardwareForm(forms.Form):
	condition_choices = [(c.id, c.name) for c in Condition.objects.all()]
	category_choices = [(c.id, c.name) for c in Category.objects.all()]
	state_choices = [(c.id, c.name) for c in State.objects.all()]
	name = forms.CharField(max_length=200)
	description = forms.CharField(widget=forms.Textarea)
	condition = forms.ModelChoiceField(queryset=Condition.objects.all())
	category = forms.ModelChoiceField(queryset=Category.objects.all())
	state = forms.ModelChoiceField(queryset=State.objects.all())
	

def displayHardware(request, id, name):
	"""Display a hardware"""
	hardware = get_object_or_404(Hardware, id=id)
	context = {'hardware':hardware}
	return render_to_response('hardware/hardwareview.html', context, RequestContext(request))

def listAll(request, page=None):
	"""list all available hardware"""
	try:
		page = int(hfa.util.stripSlash(page))
	except:
		page = 1
	hardware = Hardware.objects.all()
	paginator = Paginator(hardware, 15)
	try:
		hardware = paginator.page(page)
	except (EmptyPage, InvalidPage):
		return redirect(reverse(listAll))
	
	
	context = {'hardware':hardware, }
	return render_to_response('hardware/hardwarelist.html', context, RequestContext(request))

@login_required
def hardwareEdit(request, id=None):
	
	if id==None:
		if request.method == 'POST': # If the form has been submitted...
			form = HardwareForm(request.POST) # A form bound to the POST data
			if form.is_valid(): # All validation rules pass
				h = Hardware()
				h.name = form.cleaned_data['name']
				h.description = form.cleaned_data['description']
				h.condition = form.cleaned_data['condition']
				h.category = form.cleaned_data['category']
				h.state = form.cleaned_data['state']
				h.owner = request.user
				h.save()

				return HttpResponseRedirect(reverse(displayHardware, args=[h.id, h.name])) # Redirect after POST
		else:
			form = HardwareForm()
		
		context = {'form':form, 'edit':False}
		return render_to_response('hardware/hardwareform.html', context, RequestContext(request))
	else:
		hardware = get_object_or_404(Hardware, id=id)
		if request.user == hardware.owner:
			if request.method == 'POST':
				form = HardwareForm(request.POST) # A form bound to the POST data
				if form.is_valid(): 
					hardware.name = form.cleaned_data['name']
					hardware.description = form.cleaned_data['description']
					hardware.condition = form.cleaned_data['condition']
					hardware.category = form.cleaned_data['category']
					hardware.state = form.cleaned_data['state']
					hardware.owner = request.user
					hardware.save()
					print hardware.id
					return HttpResponseRedirect(reverse(displayHardware, args=[hardware.id, hardware.name])) # Redirect after POST
			else:
				form = HardwareForm()
				
				form.initial["name"] = hardware.name
				form.initial["description"] = hardware.description
				form.initial["condition"] = hardware.condition
				form.initial["category"] = hardware.category
				form.initial["state"] = hardware.state

				context = {'form':form, 'hardware':hardware, 'edit':True}
				return render_to_response('hardware/hardwareform.html', context, RequestContext(request))
		else:
			return HttpResponseForbidden(loader.get_template("403.html").render(RequestContext({})))
