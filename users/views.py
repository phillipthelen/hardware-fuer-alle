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
from django import forms
from django.core.urlresolvers import reverse
from main.models import Location
from users.models import UserProfile
from sorl.thumbnail import get_thumbnail
from hfa.util import create_map


class LocationForm(forms.Form):
	city = forms.CharField(max_length=200, required=False)
	street = forms.CharField(max_length=200, required=False)
	postcode = forms.CharField(max_length=5, required=False)
	displayLocation = forms.BooleanField(required=False)

class UserSettingsForm(forms.Form):
	email = forms.EmailField(required=False)
	avatar = forms.ImageField(required=False)

def error(request):
	"""Error view"""
	messages = get_messages(request)
	return render_to_response('error.html', {'messages': messages},
		RequestContext(request))

def login(request):
	"""Displays the login options"""
	return render_to_response('users/login.html', {},
		RequestContext(request))

def profile(request, id, username):
	"""displays a user profile"""
	user = get_object_or_404(User, id = id)
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
				user.email = mform.cleaned_data['email']
				user.save()
	else:
		lform = LocationForm()
		mform = UserSettingsForm()
	context = {"apps":apps, "accountlist":accountlist, 'profile':profile, 'lform':lform, 'mform':mform}
	map, showmap = create_map(profile.location)
	context["map"] = map
	context["showmap"] = showmap
	return render_to_response('users/usersettings.html', context, RequestContext(request))