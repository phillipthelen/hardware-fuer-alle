from django.template import Library, Node, TemplateSyntaxError
from django.template import Variable, resolve_variable
from django.utils.translation import ugettext as _
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse


register = Library()

def disconnect_url(provider):

	return ""


register.simple_tag(disconnect_url)