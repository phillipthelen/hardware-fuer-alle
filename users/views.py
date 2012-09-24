from django.http import HttpResponseRedirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.contrib.messages.api import get_messages
from django.contrib.auth.models import User
from hardware.models import Hardware

@login_required
def done(request):
	"""Login complete view, displays user data"""
	ctx = {
		'last_login': request.session.get('social_auth_last_login_backend')
	}
	return render_to_response('done.html', ctx, RequestContext(request))


def error(request):
	"""Error view"""
	messages = get_messages(request)
	return render_to_response('error.html', {'messages': messages},
		RequestContext(request))

def login(request):
	return render_to_response('login.html', {},
		RequestContext(request))


def logout(request):
	"""Logs out user"""
	auth_logout(request)
	return HttpResponseRedirect('/')

def profile(request, username):
	"""displays a user profile"""
	user = get_object_or_404(User, username = username)
	hardware =Hardware.objects.filter(owner=user)
	context = {'userprofile':user, 'hardware':hardware}
	return render_to_response('userprofile.html', context, RequestContext(request))
