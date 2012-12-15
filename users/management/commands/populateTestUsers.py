from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from users.models import UserProfile
from main.models import Location
from random import randrange, choice, randint, uniform
import os

class Command(BaseCommand):
	def handle(self, *args, **options):
		if len(args) > 0:
			raise CommandError('need exactly zero arguments')

		f = open('{0}/cleaned_list'.format(os.getcwd()), "r")
		lines = f.readlines()
		f.close()
		length = len(lines)
		print "Generating  200 User"
		for i in range(400):
			u = User.objects.create_user(lines[randint(0, length-1)].strip()+str(randint(1,100))+str(randint(1,100)))
			u.save()
			profile = u.get_profile()
			l = Location()
			l.latitude = uniform(7.5 ,13.6)
			l.longitude = uniform(47.5, 53.8)
			l.save()
			profile.location = l
			profile.displayLocation = choice([True, False])
			profile.save()