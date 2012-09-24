from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response

# Create your views here.
def home(request):
	"""Home view, displays login mechanism"""
	return render_to_response('home.html', {},
		RequestContext(request))

