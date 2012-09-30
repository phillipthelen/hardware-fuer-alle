from django.db import models

class CustomUserManager(models.Manager):
	def create_user(self, username, email):
		return self.model._default_manager.create(username=username)


class CustomUser(models.Model):
	"""Custom user that also saves the geolocation of the user"""
	username = models.CharField(max_length=128)
	last_login = models.DateTimeField(blank=True, null=True)

	objects = CustomUserManager()

	def is_authenticated(self):
		return True