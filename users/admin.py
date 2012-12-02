from django.utils.translation import ugettext_lazy as _
from models import UserProfile
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.comments.moderation import CommentModerator, moderator

admin.site.register(UserProfile)