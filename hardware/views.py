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
from django.core.urlresolvers import reverse
from main.views import home
from main.models import Location
from geopy import geocoders
import urllib
from hardware.forms import SendmailForm, HardwareForm, SimpleSearchForm
from django.core.mail import EmailMessage

def create_pagelist(pagenumber, maxitem):
	pagelist = []
	
	if maxitem < 5:
		for i in range(1, maxitem+1):
			pagelist.append(i)
		return pagelist

	if pagenumber <= 4: 
		for i in range(1, pagenumber):
			pagelist.append(i)
	else:
		pagelist.append(1)
		for i in range(pagenumber-3, pagenumber):
			pagelist.append(i)
	if (maxitem - pagenumber) <= 4: 
		for i in range(pagenumber, maxitem+1):
			pagelist.append(i)
	else:
		for i in range(pagenumber, pagenumber+4):
			pagelist.append(i)
		pagelist.append(maxitem)
	return pagelist

def displayHardware(request, id, name):
	"""Display a hardware"""
	hardware = get_object_or_404(Hardware, id=id)
	context = {'hardware':hardware}
	if request.user.is_authenticated():
		if hardware.owner != request.user and hardware.owner.get_profile().location != None and request.user.get_profile().location != None:
			ownerlocation = hardware.owner.get_profile().location
			userlocation = request.user.get_profile().location
			context["distance"] = hfa.util.get_distance_string(ownerlocation, userlocation)
	map, showmap = hfa.util.create_map(hardware.location)
	context["map"] = map
	context["showmap"] = showmap
	return render_to_response('hardware/hardwareview.html', context, RequestContext(request))

from django.core.paginator import Paginator, InvalidPage, EmptyPage

def get_list_page(page=1):
	hardware = Hardware.objects.all()
	paginator = Paginator(hardware, 20)
	try:
		hardware = paginator.page(page)
	except (EmptyPage, InvalidPage):
		hardware = paginator.page(1)
	if page != None:
		pagelist = create_pagelist(hardware.number, paginator.num_pages)
	else:
		pagelist = create_pagelist(1, paginator.num_pages)
	return hardware, pagelist, paginator.count

def listAll(request, page=1):
	"""list all available hardware"""
	hardware, pagelist, itemcount = get_list_page(page)
	context = {'hardware':hardware, 'pagelist':pagelist, 'itemcount':itemcount}
	return render_to_response('hardware/hardwarelist.html', context, RequestContext(request))

@login_required
def deleteHardware(request, id):
	hardware = get_object_or_404(Hardware, id=id)
	if hardware.owner == request.user:
		hardware.delete()
		return HttpResponseRedirect(reverse(home))
	else:
		return HttpResponseForbidden(loader.get_template("403.html").render(RequestContext({})))

@login_required
def hardwareEdit(request, id=None):
	user = request.user
	profile = user.get_profile()
	if user.email != "" and profile.mail_confirmed:
		if id==None:
			if request.method == 'POST': # If the form has been submitted...
				form = HardwareForm(request.POST) # A form bound to the POST data
				if form.is_valid(): # All validation rules pass
					h = Hardware()
					h.name = form.cleaned_data['name']
					h.description = form.cleaned_data['description']
					h.condition = form.cleaned_data['condition']
					h.category = form.cleaned_data['category']
					h.state = get_object_or_404(State, id=form.cleaned_data['state'])
					h.owner = user
					if form.cleaned_data['ownlocation']:
						location = Location()
						location.city = form.cleaned_data['city']
						location.street = form.cleaned_data['street']
						location.postcode = form.cleaned_data['postcode']
						g = geocoders.Google()
						if location.city!= "" or location.street!="" or location.street!="":
							searchstring = location.street + ", " + location.postcode + " " + form.cleaned_data['city']
							places = g.geocode(urllib.quote(searchstring), exactly_one=False)
							location.latitude = places[0][1][0]
							location.longitude = places[0][1][1]
						else:
							location.latitude = None
							location.longitude = None
						location.save()
						h.location = location
					else:
						h.location = profile.location
					if h.state.temporary:
						h.lendlength = form.cleaned_data['lendlength'] * form.cleaned_data['lendlengthtype']
					h.save()

					return HttpResponseRedirect(reverse(displayHardware, args=[h.id, h.name])) # Redirect after POST
			else:
				form = HardwareForm()

			context = {'form':form, 'edit':False}
			return render_to_response('hardware/hardwareform.html', context, RequestContext(request))
		else:
			hardware = get_object_or_404(Hardware, id=id)
			if user == hardware.owner:
				if request.method == 'POST':
					form = HardwareForm(request.POST) # A form bound to the POST data
					if form.is_valid():
						hardware.name = form.cleaned_data['name']
						hardware.description = form.cleaned_data['description']
						hardware.condition = form.cleaned_data['condition']
						hardware.category = form.cleaned_data['category']
						hardware.state = form.cleaned_data['state']
						hardware.owner = user
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
	else:
		return render_to_response('hardware/hardwareform.html', {"invalidmail":True} , RequestContext(request))

@login_required
def sendMail(request, hardwareid):
	hardware = get_object_or_404(Hardware, id=hardwareid)
	user = request.user
	profile = user.get_profile()
	if hardware.owner != user:
		if user.email != "" and profile.mail_confirmed:
			if request.method == "POST":
				form = SendmailForm(request.POST)
				if form.is_valid():
					headers = {'Reply-To':user.email}  # From-header
					from_email = 'noreply@hardware-fuer-alle.de'          # Return-Path header
					subject = "Somebody is interested in your hardware!"
					body = """The user {0} is interested in your hardware.
He/She wrote the following text:
{1}""".format(user.username, form.cleaned_data["text"])
					EmailMessage(subject, body, from_email, [hardware.owner.email],
									   headers=headers).send()
			else:
				form = SendmailForm()
			context = {"form":form, "hardware":hardware}
			return render_to_response('hardware/sendmail.html',context , RequestContext(request))
		else:
			return render_to_response('hardware/sendmail.html', {"invalidmail":True} , RequestContext(request))

	else:
		return render_to_response('hardware/sendmail.html', {"ownhardware":True} , RequestContext(request))

def get_search_page(page=1, searchquery=""):
	hardware = Hardware.objects.filter(name__icontains=searchquery)
	paginator = Paginator(hardware, 20)
	try:
		hardware = paginator.page(page)
	except (EmptyPage, InvalidPage):
		hardware = paginator.page(1)
	pagelist = create_pagelist(page, paginator.num_pages)
	return hardware, pagelist, paginator.count

def searchHardware(request, page=1):
	"""list all available hardware"""
	try:
		page = int(hfa.util.stripSlash(page))
	except:
		page = 1
	context = {}
	if request.method == "POST":
		form = SimpleSearchForm(request.POST)
		if form.is_valid():
			searchquery = form.cleaned_data["searchquery"]
			context["searchquery"] = searchquery
			hardware = Hardware.objects.filter(name__icontains=searchquery)
	else:
		form = SimpleSearchForm()
		hardware = Hardware.objects.all()
	paginator = Paginator(hardware, 20)
	try:
		hardware = paginator.page(page)
	except (EmptyPage, InvalidPage):
		return redirect(reverse(listAll))

	pagelist = create_pagelist(page, paginator.num_pages)

	context['hardware'] = hardware
	context["searchform"] = form
	context["pagelist"] = pagelist
	context["itemcount"] = paginator.count
	return render_to_response('hardware/hardwaresearch.html', context, RequestContext(request))