from django.http import HttpResponseRedirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.contrib.messages.api import get_messages
from django.contrib.auth.models import User
from hardware.models import Hardware
from allauth.socialaccount.models import SocialAccount, SocialApp
from django import forms
from geopy import geocoders
from gmapi import maps
from gmapi.forms.widgets import GoogleMap
from django.core.urlresolvers import reverse

class MapForm(forms.Form):
	map = forms.Field(widget=GoogleMap(attrs={'width':250, 'height':250}))


class LocationForm(forms.Form):
	city = forms.CharField(max_length=200, required=False)
	street = forms.CharField(max_length=200, required=False)
	postcode = forms.CharField(max_length=5, required=False)
	displayLocation = forms.BooleanField(required=False)

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
		form = LocationForm(request.POST) # A form bound to the POST data
		if form.is_valid(): # All validation rules pass
			profile.city = form.cleaned_data['city']
			profile.street = form.cleaned_data['street']
			profile.postcode = form.cleaned_data['postcode']
			profile.displayLocation = form.cleaned_data['displayLocation']
			g = geocoders.Google()
			place, (lat, lng) = g.geocode(profile.street + ", " + profile.postcode + " " + profile.city)
			profile.latitude = lat
			profile.longitude = lng  		
			profile.save()

			return HttpResponseRedirect(reverse(settings)) # Redirect after POST
	else:
		form = LocationForm() # An unbound form
		#if profile.city != None:
		#	form.fields['city'] = profile.city

	context = {"apps":apps, "accountlist":accountlist, 'form':form, 'profile':profile}
	if profile.latitude != None and profile.longitude != None:
		gmap = maps.Map(opts = {
			'center': maps.LatLng(profile.latitude, profile.longitude),
			'mapTypeId': maps.MapTypeId.ROADMAP,
			'zoom': 10,
		})
		marker = maps.Marker(opts = {
			'map': gmap,
			'position': maps.LatLng(profile.latitude, profile.longitude),
		})
		context['map'] =  MapForm(initial={'map': gmap})
		context['showmap'] = True
	else:
		context['showmap'] = False
	print context, profile.latitude, profile.longitude
	return render_to_response('users/usersettings.html', context, RequestContext(request))