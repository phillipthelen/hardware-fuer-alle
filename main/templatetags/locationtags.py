from django import template

register = template.Library()

@register.simple_tag
def get_distance(origin, destination):
	if origin != None and destination != None:
		return str(origin.get_distance_string(destination))
	else:
		return "-"