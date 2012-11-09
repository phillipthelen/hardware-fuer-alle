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
from users.models import UserProfile
from sorl.thumbnail import get_thumbnail
from hfa.util import create_map
import datetime, random, sha
from django.core.mail import send_mail

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
			email_body = """Hello, %s, and thanks for signing up for an
		example.com account!\n\nTo activate your account, click this link within 48
		hours:\n\nhttp://127.0.0.1:8000/accounts/confirm/%s""" % (
				user.username,
				profile.confirmation_key)
			send_mail(email_subject,
					email_body,
					'noreply@hardware-fuer-alle.de',
					[user.email])

def error(request):
	"""Error view"""
	messages = get_messages(request)
	return render_to_response('error.html', {'messages': messages, },
		RequestContext(request))

def login(request):
	"""Displays the login options"""
	return render_to_response('users/login.html', {},
		RequestContext(request))

def profile(request, username):
	"""displays a user profile"""
	user = get_object_or_404(User, username = username)
	hardware =Hardware.objects.filter(owner=user)
	context = {'userprofile':user, 'hardware':hardware}
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
					places = g.geocode(location.street + ", " + location.postcode + " " + location.city, exactly_one=False)
					location.latitude = places[0][1][0]
					location.longitude = places[0][1][1]
				else:
					location.latitude = None
					location.longitude = None
				location.save()
				profile.save()
				print profile.location.city
		else:
			lform = LocationForm()
			mform = UserSettingsForm(request.POST, request.FILES)
			if mform.is_valid():
				print "valid"
				if 'avatar' in request.FILES:
					profile.avatar = request.FILES["avatar"]
					profile.save()
					print "file saved"
				if mform.cleaned_data['email'] != user.email:
					set_mail(user, mform.cleaned_data['email'])
				if mform.cleaned_data['displayname'] != profile.displayname:
					profile.displayname = mform.cleaned_data['displayname'] 
					profile.save()
				user.save()
	else:
		lform = LocationForm()
		mform = UserSettingsForm()
	if not profile.mail_confirmed:
		context["mailconfirm"] = "We sent you a confirmation link. Please check your mail."
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
		if form.is_valid():
			set_mail(user, form.cleaned_data["email"])
			return render_to_response('users/newmail.html', {'set': True}, RequestContext(request))
	else:
		form = EmailForm()
		if not profile.mail_confirmed and user.email != "":
			return render_to_response('users/newmail.html', {'unfinished': True}, RequestContext(request))
	return render_to_response('users/newmail.html', {'form': form}, RequestContext(request))
