from users.views import newEmail
from django.core.urlresolvers import reverse
from hfa.util import HfaError
def email(request):
	user = request.user
	if "hfaerrors" in request:
		errors = request["hfaerrors"]
	else:
		errors = []
	if user.is_authenticated():
		print user.email
		if user.email == None or user.email == "":
			error = HfaError(message="You haven't set a email adress. Please do so <a href='{0}'>here</a>".format(reverse(newEmail)))
			errors.append(error)
		elif not user.get_profile().mail_confirmed:
			error = HfaError(message="You still have to confirm your email adress. Please check your mail.")
			errors.append(error)
	if errors != []:
		return {"hfaerrors":errors}
	else:
		return {}
