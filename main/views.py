 # -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response,  get_object_or_404
from django.contrib.auth.decorators import login_required
from hardware.models import Hardware
from main.forms import HardwareReportForm
from django.core.mail import EmailMessage
from django.contrib import messages
from django.core.urlresolvers import reverse
from allauth.account.models import EmailAddress
# Create your views here.
def home(request):
	"""Home view, displays login mechanism"""
	user = request.user
	if user.is_authenticated() and user.email != "" and not user.get_profile().mail_confirmed:
		emails = EmailAddress.objects.filter(user=user)
		if len(emails) > 0:
			profile = user.get_profile()
			profile.mail_confirmed = emails[0].verified
			profile.save()
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
Es geht um: http://hardware-fuer-alle.de/hardware/{1}/{2}
Beschreibung:
{2}""".format(request.user.username, hardware.id, hardware.name, form.cleaned_data["description"])
			EmailMessage(subject, body, from_email, ["abuse@hardware-fuer-alle.de"],
									   headers=headers).send()
			messages.add_message(request, messages.SUCCESS, u"Die Email mit deiner Meldung wurde an uns verschickt. Wir werden uns so schnell wie möglich darum kümmern.")
			from hardware.views import displayHardware
			return HttpResponseRedirect(reverse(displayHardware, args=[hardware.id, hardware.slug]))
		else:
			return render_to_response('report.html', {'hardwareid':hardwareid, 'form':form}, RequestContext(request))
	else:
		form = HardwareReportForm()
		return HttpResponseRedirect(reverse(home))
