from users.views import newEmail
from django.core.urlresolvers import reverse
from django.contrib import messages
def email(request):
	user = request.user
	if user.is_authenticated():
		if user.email == None or user.email == "":
			messages.add_message(request, messages.ERROR, "You haven't set a email adress. Please do so <a href='{0}'>here</a>".format(reverse(newEmail)))
		elif not user.get_profile().mail_confirmed:
			messages.add_message(request,messages.ERROR, "You still have to confirm your email adress. Please check your mail.")
	return {}