import settings
import os, time
from django import forms
from gmapi import maps
from gmapi.forms.widgets import GoogleMap
from geopy import distance

class MapForm(forms.Form):
	map = forms.Field(widget=GoogleMap(attrs={'width':250, 'height':250}))

def stripSlash(string):
	if string[-1:] != '/':
		return string
	return string[:-1]

def getMapDepth(city=False, postcode=False, street=False):
	return 10

def get_file_name(instance, old_filename):
	extension = os.path.splitext(old_filename)[1]
	filename = str(time.time()) + extension
	return 'avatars/' + filename

def create_map(location):
	if location != None and location.latitude != None and location.longitude != None:
		gmap = maps.Map(opts = {
			'center': maps.LatLng(location.latitude, location.longitude),
			'mapTypeId': maps.MapTypeId.ROADMAP,
			'zoom': 10,
		})
		marker = maps.Marker(opts = {
			'map': gmap,
			'position': maps.LatLng(location.latitude, location.longitude),
		})
		map = MapForm(initial={'map': gmap})
		return map, True
	else:
		return None, False

def get_distance(location1, location2):
    pos1 = (location1.latitude, location1.longitude)
    pos2 = (location2.latitude, location2.longitude)
    dist = distance.distance(pos1, pos2).km
    return dist

def get_distance_string(location1, location2):
	dist = get_distance(location1, location2)
	return "{0:.2f}km".format(dist)
