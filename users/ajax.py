from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from django.template.loader import render_to_string
from django.contrib.auth.models import User

@dajaxice_register
def get_users_to_lend(request, query):
	dajax = Dajax()
	userlist = User.objects.filter(username__icontains=query)
	endlist = []
	for user in userlist:
		endlist.append(user.username)
	dajax.assign('#id_username','data-source', endlist)
	return dajax.json()