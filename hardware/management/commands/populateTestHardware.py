from django.core.management.base import BaseCommand, CommandError
from hardware.models import State, Category, Condition, Hardware
from django.contrib.auth.models import User
from main.models import Location
from random import randrange, choice, uniform
import os


class Command(BaseCommand):
	def handle(self, *args, **options):
		if len(args) > 0:
			raise CommandError('need exactly zero arguments')

		f = open('{0}/cleaned_list'.format(os.getcwd()), "r")
		lines = f.readlines()
		f.close()
		length = len(lines)
		print "Generating 10 States"
		for i in range(10):
			s = State()
			s.name = lines[randrange(1, length)-1]
			s.temporary = choice([True, False])
			s.save()
		print "Generating 10 Categories"
		for i in range(10):
			c = Category()
			c.name = lines[randrange(1, length)-1]
			c.save()
		print "Generating 10 Conditions"
		for i in range(10):
			c = Condition()
			c.name = lines[randrange(1, length)-1]
			c.save()

		print "Generating 4000 Hardwares"
		for i in range(4000):
			h = Hardware()
			h.name = lines[randrange(1, length)-1]
			h.state = choice(State.objects.all())
			h.condition = choice(Condition.objects.all())
			h.category = choice(Category.objects.all())
			h.description = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum nibh justo, ornare semper pharetra id, laoreet quis ligula. Mauris non sem elit, nec ornare lectus. Duis sit amet dolor eleifend tellus congue auctor eget a augue. Fusce aliquam, ipsum sit amet imperdiet viverra, neque nisl aliquet arcu, quis tristique libero diam a sem. Curabitur quis elementum enim. Cras id nulla a arcu sollicitudin condimentum vestibulum ac risus. In tincidunt hendrerit mollis. Nunc sed nulla nibh, aliquam aliquam neque. Aenean eget cursus dui. Ut a purus neque. Proin eu eros elit. Suspendisse nisl enim, sagittis vel vulputate eu, pretium vitae ligula. Morbi posuere luctus dolor, sit amet tempus dolor vestibulum id. In ornare, risus eget mattis varius, dui tellus dapibus ligula, vel adipiscing risus elit non risus. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. """
			h.owner = choice(User.objects.all())
			if choice([True, False]):
				h.location = h.owner.get_profile().location
			else:
				l = Location()
				l.latitude = uniform(7.5 ,13.6)
				l.longitude = uniform(47.5, 53.8)
				l.save()
				h.location = l
			h.save()