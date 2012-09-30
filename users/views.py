from django.http import HttpResponseRedirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.contrib.messages.api import get_messages
from django.contrib.auth.models import User
from hardware.models import Hardware
from allauth.socialaccount.models import SocialAccount, SocialApp


def error(request):
	"""Error view"""
	messages = get_messages(request)
	return render_to_response('error.html', {'messages': messages},
		RequestContext(request))

def login(request):
	return render_to_response('login.html', {},
		RequestContext(request))

def profile(request, username):
	"""displays a user profile"""
	user = get_object_or_404(User, username = username)
	hardware =Hardware.objects.filter(owner=user)
	context = {'userprofile':user, 'hardware':hardware}
	return render_to_response('userprofile.html', context, RequestContext(request))

@login_required
def settings(request):
	"""displays the settings for an account"""
	user = request.user
	accounts = SocialAccount.objects.filter(user=user)
	accountlist = []
	for account in accounts:
		accountlist.append(account.provider)
	apps = SocialApp.objects.all()
	context = {"apps":apps, "accountlist":accountlist}
	return render_to_response('usersettings.html', context, RequestContext(request))