from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response,  get_object_or_404
from django.contrib.auth.decorators import login_required
from hardware.models import Hardware
from main.forms import HardwareReportForm
from django.core.mail import EmailMessage
# Create your views here.
def home(request):
	"""Home view, displays login mechanism"""
	return render_to_response('home.html', {},
		RequestContext(request))

@login_required
def hardwareAbuse(request):
	if request.POST:
		report = request.user
		hardwareid = request.POST["object"]
		hardware = get_object_or_404(Hardware, id=hardwareid)
		form = HardwareReportForm(request.POST)
		if form.is_valid():
			headers = {'Reply-To':request.user.email}  # From-header
			from_email = 'support@hardware-fuer-alle.de'          # Return-Path header
			subject = "Es wurde ein Missbrauch gemeldet"
			body = """Der Benutzer {0} hat einen Missbrauch gemeldet.
Es geht um: http://beta.hardware-fuer-alle.de/hardware/{1}/{2}
Beschreibung:
{2}""".format(request.user.username, hardware.id, hardware.name, form.cleaned_data["description"])
			EmailMessage(subject, body, from_email, ["abuse@hardware-fuer-alle.de"],
									   headers=headers).send()
			return render_to_response('report.html', {'success':True}, RequestContext(request))
		else:
			return render_to_response('report.html', {'hardwareid':hardwareid, 'form':form}, RequestContext(request))
	else:
		form = HardwareReportForm()
		return render_to_response('report.html', {'form':form}, RequestContext(request))
