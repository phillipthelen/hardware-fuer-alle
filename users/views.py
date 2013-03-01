 # -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.contrib.messages.api import get_messages
from django.contrib.auth.models import User
from hardware.models import Hardware
from allauth.socialaccount.models import SocialAccount, SocialApp
from geopy import geocoders
from users.forms import EmailForm, LocationForm, UserSettingsForm
from django.core.urlresolvers import reverse
from main.models import Location
from main.views import home
from users.models import UserProfile
from sorl.thumbnail import get_thumbnail
from hfa.util import create_map
import datetime, random, sha
from django.core.mail import send_mail
from django.contrib import messages
from allauth.account.forms import LoginForm, SignupForm
def set_mail(user, email):
	if email != "":
		profile = user.get_profile()
		# Build the activation key for their account
		salt = sha.new(str(random.random())).hexdigest()[:5]
		confirmation_key = sha.new(salt+user.username).hexdigest()
		key_expires = datetime.datetime.today() + datetime.timedelta(2)



		profile.confirmation_key = confirmation_key
		profile.key_expires = key_expires
		profile.mail_confirmed = False
		profile.save()
		user.email = email
		user.save()
		# Send an email with the confirmation link

		email_subject = 'Your new hardware-fuer-alle.de email confirmation'
		email_body = """Hallo, {}, um deine E-Mail Adresse bei hardware-fuer-alle.de einzutragen musst du sie noch bestätigen\n
		Bitte klicke hierfür innerhalb der nächsten 48 Stunden auf diesen Link:\n\nhttp://hardware-fuer-alle.de/accounts/confirm/{}""".format(
			user.username,
			profile.confirmation_key)
		send_mail(email_subject,
				email_body,
				'support@hardware-fuer-alle.de',
				[user.email])

def error(request):
	"""Error view"""
	messages = get_messages(request)
	return render_to_response('error.html', {'messages': messages, },
		RequestContext(request))

def login(request,  **kwargs):
	success_url = kwargs.pop("success_url", None)

	if success_url is None:
		success_url = "/"

	if request.method == "POST":
		form = LoginForm(request.POST)
		if form.is_valid():
			return form.login(request, redirect_url=success_url)
	else:
		form = LoginForm()

	registerform = SignupForm()

	ctx = {
		"form": form,
		"registerform":registerform,
		"redirect_field_name": "next",
		"redirect_field_value": request.REQUEST.get("next"),
		"apps":SocialApp.objects.all(),
	}
	return render_to_response('users/login.html', RequestContext(request, ctx))

def profile(request, userid):
	"""displays a user profile"""
	user = get_object_or_404(User, id = userid)
	available_hardware =Hardware.objects.filter(owner=user, availability=True)
	
	accounts = SocialAccount.objects.filter(user=user)
	accountlist = []
	for account in accounts:
		accountlist.append(account)
	if user.get_profile().displayLocation:
		map, showmap = create_map(user.get_profile().location)
	else:
		map = None
	context = {
		'userprofile':user,
		'available_hardware':available_hardware,
		'map':map,
		'accountlist':accountlist}
	if request.user == user:
		unavailable_hardware =Hardware.objects.filter(owner=user, availability=False)
		context['unavailable_hardware'] = unavailable_hardware
	return render_to_response('users/userprofile.html', context, RequestContext(request))

@login_required
def settings(request):
	"""displays the settings for an account"""
	user = request.user
	profile = user.get_profile()
	accounts = SocialAccount.objects.filter(user=user)
	accountlist = []
	for account in accounts:
		accountlist.append(account.provider)
	apps = SocialApp.objects.all()
	context = {}
	if request.method == 'POST': # If the form has been submitted...
		if request.POST["type"] == "location":
			lform = LocationForm(request.POST)
			mform = UserSettingsForm()
			if lform.is_valid(): # All validation rules pass
				if profile.location==None:
					location = Location()
					location.save()
					profile.location = location
					profile.save()
				else:
					location = profile.location
				location.city = lform.cleaned_data['city']
				location.street = lform.cleaned_data['street']
				location.postcode = lform.cleaned_data['postcode']
				profile.displayLocation = lform.cleaned_data['displayLocation']
				g = geocoders.Google()
				if location.city!= "" or location.street!="" or location.street!="":
					try:
						places = g.geocode(location.street + ", " + location.postcode + " " + location.city, exactly_one=False)
						location.latitude = places[0][1][0]
						location.longitude = places[0][1][1]
						location.save()
					except geocoders.google.GQueryError, e:
						messages.add_message(request, messages.ERROR, u"Es konnte kein Ort gefunden werden, der deiner Eingabe entspricht. Hast du dich vielleicht vertippt?")
				else:
					location.latitude = None
					location.longitude = None
					location.save()
				profile.save()
		else:
			lform = LocationForm()
			mform = UserSettingsForm(request.POST)
			mform.user = request.user
			if mform.is_valid():
				if mform.cleaned_data['email'] != user.email:
					set_mail(user, mform.cleaned_data['email'])
				if mform.cleaned_data['displayname'] != profile.displayname:
					profile.displayname = mform.cleaned_data['displayname']
					profile.save()
				user.save()
	else:
		lform = LocationForm()
		mform = UserSettingsForm()
	context.update({"apps":apps, "accountlist":accountlist, 'profile':profile, 'lform':lform, 'mform':mform})
	map, showmap = create_map(profile.location)
	context["map"] = map
	context["showmap"] = showmap
	return render_to_response('users/usersettings.html', context, RequestContext(request))

@login_required
def confirmEmail(request, confirmation_key):
	profile = request.user.get_profile()
	if profile.confirmation_key==confirmation_key:
		#if profile.key_expires < datetime.datetime.today():
		#	return render_to_response('users/confirm.html', {'expired': True}, RequestContext(request))
		profile.mail_confirmed = True
		profile.save()
		return render_to_response('users/confirm.html', {'success': True}, RequestContext(request))
	else:
		return render_to_response('users/confirm.html', {'invalid': True}, RequestContext(request))

@login_required
def newEmail(request):
	user = request.user
	profile = user.get_profile()
	if request.POST:
		form = EmailForm(request.POST)
		form.user = request.user
		if form.is_valid():
			set_mail(user, form.cleaned_data["email"])
			return render_to_response('users/newmail.html', {'set': True}, RequestContext(request))
	else:
		form = EmailForm()
		if not profile.mail_confirmed and user.email != "":
			return render_to_response('users/newmail.html', {'unfinished': True}, RequestContext(request))
	return render_to_response('users/newmail.html', {'form': form}, RequestContext(request))

@login_required
def disconnect(request, socialacc=False):
	accounts = SocialAccount.objects.filter(user=request.user)
	if request.POST and socialacc == False:
		request.user.get_profile().delete()
		request.user.delete()
		return HttpResponseRedirect(reverse(home))
	if len(accounts) == 1:
		return render_to_response('users/deleteaccount.html', {}, RequestContext(request))
	account = accounts.filter(provider=socialacc)
	account.delete()	
	
	messages.add_message(request, messages.SUCCESS, u"Die Verknüpfung wurde aufgehoben.")
	return HttpResponseRedirect(reverse(settings))