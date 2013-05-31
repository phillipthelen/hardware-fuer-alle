from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from django.template.loader import render_to_string
from hardware.views import get_list_page, create_pagelist, get_search_page

@dajaxice_register
def listPagination(request, p, ready_to_use):
	items, pagelist, itemcount = get_list_page(ready_to_use, p)

	render = render_to_string('hardware/hardwarelisttable.html', {'hardware': items, 'pagelist':pagelist, 'itemcount':itemcount, 'ready_to_use':ready_to_use})
	dajax = Dajax()
	dajax.assign('#pagination', 'innerHTML', render)
	return dajax.json()


@dajaxice_register
def listPagination(request, p):
	items, pagelist, itemcount = get_list_page(True, p, True)

	render = render_to_string('hardware/hardwarelisttable.html', {'hardware': items, 'pagelist':pagelist, 'itemcount':itemcount, 'history':True})
	dajax = Dajax()
	dajax.assign('#pagination', 'innerHTML', render)
	return dajax.json()


@dajaxice_register
def searchPagination(request, p, searchquery, searchstate, searchcategory, searchcondition, searchsort):
	items, pagelist, itemcount = get_search_page(p, searchquery,  searchstate, searchcategory, searchcondition, searchsort)

	render = render_to_string('hardware/hardwarelisttable.html', {'hardware': items, 'pagelist':pagelist, 'searchquery':searchquery, 'itemcount':itemcount, 'search':True})
	dajax = Dajax()
	dajax.assign('#pagination', 'innerHTML', render)
	return dajax.json()