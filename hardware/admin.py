from django.utils.translation import ugettext_lazy as _
from models import Hardware, State, Condition, Category
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.comments.moderation import CommentModerator, moderator

class HardwareAdmin(admin.ModelAdmin):

	# List display
	list_display = ('name',)
	# Fields in which should be searched.
	search_fields = ['name', 'description']

admin.site.register(Hardware, HardwareAdmin)

admin.site.register(State)
admin.site.register(Condition)
admin.site.register(Category)