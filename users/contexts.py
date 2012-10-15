from users.views import newEmail
from django.core.urlresolvers import reverse

def email(request):
	user = request.user
	if "hfaerrors" in request:
		errors = request["hfaerrors"]
	else:
		errors = []
	if user.is_authenticated:
		print user.email
		if user.email == None or user.email == "":
			errors.append("You haven't set a email adress. Please do so <a href='{0}'>here</a>".format(reverse(newEmail)),)
		elif not user.get_profile().mail_confirmed:
			errors.append("You still have to confirm your email adress. Please check your mail.")
	if errors != []:
		return {"hfaerrors":errors}
	else:
		return {}