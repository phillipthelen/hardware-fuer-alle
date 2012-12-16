 # -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext, loader, Context, Template
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.contrib.messages.api import get_messages
from django.contrib.auth.models import User
from hardware.models import Hardware, Category, Condition, State
from django.core.paginator import Paginator, InvalidPage, EmptyPage
import hfa.util as util
from django.core.urlresolvers import reverse
from main.views import home
from main.models import Location
from geopy import geocoders
import urllib
from hardware.forms import SendmailForm, HardwareForm, SimpleSearchForm, SearchForm, LendForm
from django.core.mail import EmailMessage
from fileupload.models import MultiuploaderImage
from django.contrib import messages
from allauth.socialaccount.models import SocialAccount, SocialApp

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
		if hardware.owner != request.user and hardware.location != None and request.user.get_profile().location != None:
			hardwarelocation = hardware.location
			userlocation = request.user.get_profile().location
			context["distance"] = util.get_distance_string(hardwarelocation, userlocation)
	if hardware.owner.get_profile().displayLocation  or request.user.is_staff:
		map, showmap = util.create_map(hardware.location, (500, 300))
		context["map"] = map
		context["showmap"] = showmap
	images = MultiuploaderImage.objects.filter(hardware=hardware.id)
	context["images"] = images
	return render_to_response('hardware/hardwareview.html', context, RequestContext(request))

from django.core.paginator import Paginator, InvalidPage, EmptyPage

def get_list_page(ready_to_use, page=1):
	hardware = Hardware.objects.filter(category__ready_to_use = ready_to_use)
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

def listHardware(request, page=1):
	"""list all available hardware"""
	hardware, pagelist, itemcount = get_list_page(True, page)
	context = {'hardware':hardware, 'pagelist':pagelist, 'itemcount':itemcount, "ready_to_use":True}
	return render_to_response('hardware/hardwarelist.html', context, RequestContext(request))

def listComponents(request, page=1):
	"""list all available hardware"""
	hardware, pagelist, itemcount = get_list_page(False, page)
	context = {'hardware':hardware, 'pagelist':pagelist, 'itemcount':itemcount, "ready_to_use":False}
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
			#Create new hardware
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
							try:
								places = g.geocode(urllib.quote(searchstring), exactly_one=False)
								location.latitude = places[0][1][0]
								location.longitude = places[0][1][1]
								location.save()
							except geocoders.google.GQueryError, e:
								messages.add_message(request, messages.ERROR, u"Es konnte kein Ort gefunden werden, der deiner Eingabe entspricht. Hast du dich vielleicht vertippt?")
						else:
							location.latitude = None
							location.longitude = None
							location.save()
						h.location = location
					else:
						h.location = profile.location
					if h.state.temporary and form.cleaned_data['lendlength'] != None:
						h.lendlength = form.cleaned_data['lendlength'] * form.cleaned_data['lendlengthtype']

					h.save()
					messages.add_message(request, messages.SUCCESS, u"Deine Hardware wurde erfolgreich angelegt. Bitte füge noch ein paar Bilder hinzu.")
					context = {'form':form, 'hardware':h}
					return render_to_response('hardware/imageform.html', context, RequestContext(request))
			else:
				form = HardwareForm()

			context = {'form':form, 'edit':False}
			return render_to_response('hardware/hardwareform.html', context, RequestContext(request))
		else:
			#edit existing hardware
			hardware = get_object_or_404(Hardware, id=id)
			if user == hardware.owner:
				if request.method == 'POST':
					form = HardwareForm(request.POST) # A form bound to the POST data
					if form.is_valid():
						hardware.name = form.cleaned_data['name']
						hardware.description = form.cleaned_data['description']
						hardware.condition = form.cleaned_data['condition']
						hardware.category = form.cleaned_data['category']
						hardware.state = get_object_or_404(State, id=form.cleaned_data['state'])
						hardware.owner = user
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
							hardware.location = location
						else:
							hardware.location = profile.location
						hardware.save()
						messages.add_message(request, messages.SUCCESS, "Hardware wurde erfolgreich bearbeitet.")
						return HttpResponseRedirect(reverse(displayHardware, args=[hardware.id, hardware.slug])) # Redirect after POST
				else:
					form = HardwareForm()

					form.initial["name"] = hardware.name
					form.initial["description"] = hardware.description
					form.initial["condition"] = hardware.condition
					form.initial["category"] = hardware.category
					form.initial["state"] = hardware.state.id
					images = MultiuploaderImage.objects.filter(hardware=hardware.id)
					context = {'form':form, 'hardware':hardware, 'edit':True, 'images':images}
					return render_to_response('hardware/hardwareform.html', context, RequestContext(request))
			else:
				return HttpResponseForbidden(loader.get_template("403.html").render(RequestContext({})))
	else:
		return render_to_response('hardware/hardwareform.html', {"invalidmail":True} , RequestContext(request))

@login_required
def new_images(request, hardwareid):
	hardware = get_object_or_404(Hardware, id=hardwareid)
	accounts = SocialAccount.objects.filter(user=request.user)
	accountlist = []
	for account in accounts:
		accountlist.append(account.provider)
	t = Template("""<script type="text/javascript" src="//platform.twitter.com/widgets.js"></script><script src="https://apis.google.com/js/plusone.js"></script>
Danke das du deine Hardware anderen zur verfügung stellen möchtest!<br />""")
#Willst du anderen mitteilen das deine Hardware nun hier verfügbar ist?<br />
#{% if 'facebook' in accountlist %}<a href='http://www.facebook.com/sharer.php' class="btn" target="blank">Auf Facebook teilen</a>{% endif %}
#{% if 'twitter' in accountlist %}<a href='https://twitter.com/intent/tweet' class="btn">Auf Twitter teilen</a>{% endif %}
#{% if 'google' in accountlist %}<a href='' class="btn">Auf Google+ teilen</a>{% endif %} """)
	c = Context({'accountlist':accountlist})
	messages.add_message(request, messages.SUCCESS, t.render(c))
	return HttpResponseRedirect(reverse(displayHardware, args=[hardware.id, hardware.slug]))

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
					from_email = 'support@hardware-fuer-alle.de'          # Return-Path header
					subject = "[hardware für alle] Hardwareanfrage eines Benutzers/einer Benutzerin"
					accounts = SocialAccount.objects.filter(user=request.user)
					accountlist = []
					for account in accounts:
						accountlist.append(account.provider)
					c = Context({"user":user, "hardware":hardware, "text":form.cleaned_data["text"], "accountlist":accountlist})
					body = render_to_string("hardware/requestmail.html", c)
					EmailMessage(subject, body, from_email, [hardware.owner.email],
									   headers=headers).send()
					messages.add_message(request, messages.SUCCESS, "E-Mail an den Besitzer wurde verschickt.")
					return HttpResponseRedirect(reverse(displayHardware, args=[hardware.id, hardware.slug]))
			else:
				form = SendmailForm()
			context = {"form":form, "hardware":hardware}
			return render_to_response('hardware/sendmail.html',context , RequestContext(request))
		else:
			return render_to_response('hardware/sendmail.html', {"invalidmail":True} , RequestContext(request))

	else:
		return render_to_response('hardware/sendmail.html', {"ownhardware":True} , RequestContext(request))

def get_search_page(page=1, searchquery="", searchstate="", searchcategory="", searchcondition="", searchsort=""):
	hardware = Hardware.objects.filter(name__icontains=searchquery)
	if searchstate != "":
		hardware = hardware.filter(state_id=searchstate)
	if searchcategory != "":
		hardware = hardware.filter(category_id=searchcategory)
	if searchcondition != "":
		hardware = hardware.filter(condition_id=searchcondition)
	if searchsort != "":
		hardware = hardware.extra(order_by=[searchsort,])
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
		page = int(util.stripSlash(page))
	except:
		page = 1
	context = {}
	if request.method == "POST":
		form = SearchForm(request.POST)
		if form.is_valid():
			searchquery = form.cleaned_data["searchquery"]
			searchstate = form.cleaned_data["state"]
			searchcategory = form.cleaned_data["category"]
			searchcondition = form.cleaned_data["condition"]
			
			
			if searchquery != None:
				context["searchquery"] = searchquery.strip()
			hardware = Hardware.objects.filter(name__icontains=searchquery)
			if searchstate != None:
				context["searchstate"] = str(searchstate.id).strip()
				hardware = hardware.filter(state=searchstate)
			else:
				context["searchstate"] = ""
			if searchcategory != None:
				context["searchcategory"] = str(searchcategory.id).strip()
				hardware = hardware.filter(category_id=searchcategory)
			else:
				context["searchcategory"] = ""
			if searchcondition != None:
				context["searchcondition"] = str(searchcondition.id).strip()
				hardware = hardware.filter(condition=searchcondition)
			else:
				context["searchcondition"] = ""
			if form.cleaned_data ["sortby"] != "":
				context["searchsort"] = str(form.cleaned_data["sortby"]).strip()
				hardware = hardware.extra(order_by=[form.cleaned_data["sortby"],])
			else:
				context["searchsort"] = ""
			paginator = Paginator(hardware, 20)
			try:
				hardware = paginator.page(page)
			except (EmptyPage, InvalidPage):
				return redirect(reverse(listAll))

			pagelist = create_pagelist(page, paginator.num_pages)
			context['hardware'] = hardware
			context["pagelist"] = pagelist
			context["itemcount"] = paginator.count

	else:
		form = SearchForm()
	context["searchform"] = form
	context["search"] = True
	return render_to_response('hardware/hardwaresearch.html', context, RequestContext(request))

@login_required
def giveaway(request):
	if request.POST:
		owner = request.user
		hardwareid = request.POST["hardware"]
		hardware = get_object_or_404(Hardware, id=hardwareid)
		if hardware.owner == owner:
			form = LendForm(request.POST)
			if form.is_valid():
				username = form.cleaned_data["username"]
				hardware.lent_to = get_object_or_404(User, username=username)
				hardware.availability = False
				hardware.save()
				return HttpResponseRedirect(reverse(displayHardware, args=[hardware.id, hardware.name])) # Redirect after POST
			else:
				return render_to_response('hardware/giveaway', {'hardwareid':hardwareid, 'form':form}, RequestContext(request))
		else:
			return render_to_response('error.html', {"messages":["Du kannst nur deine eigene hardware weg geben."]}, RequestContext(request))
	else:
		return HttpResponseRedirect(reverse(home))

@login_required
def takeback(request, hardwareid):
	owner = request.user
	hardware = get_object_or_404(Hardware, id=hardwareid)
	if hardware.owner == owner:
		hardware.lent_to = None
		hardware.availability = True
		hardware.save()
		return HttpResponseRedirect(reverse(displayHardware, args=[hardware.id, hardware.name])) # Redirect after POST
	else:
		return render_to_response('error.html', {"messages":["Nicht deine Hardware"]}, RequestContext(request))