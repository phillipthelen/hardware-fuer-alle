from django.http import HttpResponseRedirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.contrib.messages.api import get_messages
from django.contrib.auth.models import User
from hardware.models import Hardware
from django.core.paginator import Paginator, InvalidPage, EmptyPage
import hfa.util

@login_required
def create(request):
	"""display form so that user can create new hardware"""

@login_required
def edit(request):
	"""display form so that user can edit existing hardware"""

def displayHardware(request, id):
	"""Display a hardware"""
	hardware = get_object_or_404(Hardware, id=id)
	context = {'hardware':hardware}
	return render_to_response('hardwareview.html', context, RequestContext(request))

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
		return redirect("/hardware/")
	
	
	context = {'hardware':hardware, }
	return render_to_response('hardwarelist.html', context, RequestContext(request))
