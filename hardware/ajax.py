from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from django.template.loader import render_to_string
from hardware.views import get_list_page, create_pagelist, get_search_page

@dajaxice_register
def listPagination(request, p):
	print "pagination"
	items, pagelist, itemcount = get_list_page(p)
	print items
	
	render = render_to_string('hardware/hardwarelisttable.html', {'hardware': items, 'pagelist':pagelist, 'itemcount':itemcount})
	dajax = Dajax()
	dajax.assign('#pagination', 'innerHTML', render)
	return dajax.json()

@dajaxice_register
def searchPagination(request, p, searchquery):
	print "pagination"
	items, pagelist, itemcount = get_search_page(p, searchquery)
	print items
	
	render = render_to_string('hardware/hardwarelisttable.html', {'hardware': items, 'pagelist':pagelist, 'searchquery':searchquery, 'itemcount':itemcount})
	dajax = Dajax()
	dajax.assign('#pagination', 'innerHTML', render)
	return dajax.json()