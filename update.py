#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from audit import get_bad_zipcode, get_bad_cities


def has_street_abbv(street_name):
	match = re.search(r'^(av|carr|dom|esq|prol)(\s|\.)', street_name, re.IGNORECASE)
	return match is not None

street_abbv_map = {'av': 'Avenida',
					'carr': 'Carretera',
					'dom': 'Domicilio',
					'esq': 'Esquina',
					'prol': u'Prolongación'}

def update_street_name(street_name):
	parts = re.split('\.| ', street_name) # split on period or whitespace
	# could also use re.findall(r'[\w]+', street_name)
	abbv = parts[0]
	new_name = re.sub(abbv + r'[\.]?', street_abbv_map[abbv.lower()], street_name) # map keys are lowercase
	return new_name


bad_zips = get_bad_zipcode()

def has_good_zipcode(code):
	return code not in bad_zips


bad_cities = get_bad_cities()

def has_good_city_name(city):
	return city not in bad_cities

gdl = re.compile(r'guad')
zpn = re.compile(r'zapop')
tnl = re.compile(r'tonal')
tpq = re.compile(r'tlaque')
tjm = re.compile(r'tlajom')

def update_city(city):
	if gdl.search(city):
		return 'Guadalajara'
	if zpn.search(city):
		return 'Zapopan'
	if tnl.search(city):
		return u'Tonalá'
	if tpq.search(city):
		return 'Tlaquepaque'
	if tjm.search(city):
		return u'Tlajomulco de Zúñiga'
	return None


'''
def update_cuisine(cuisine):
	if re.search('mariscos', cuisine, re.IGNORECASE):
		new = 'seafood'
	if re.search('hot_dogs', cuisine, re.IGNORECASE):
		new = 'hot_dogs'
	if re.search('nieve', cuisine, re.IGNORECASE):
		new = 'ice_cream'
	if re.search(u'Café', cuisine, re.IGNORECASE):
		new = 'coffee_shop'
	if re.search('pizza', cuisine, re.IGNORECASE):
		new = 'pizza'
	if re.search(u'oaxaqueña', cuisine):
		# We leave this one as is...
		new = cuisine
	# If multiple cuisines we return a list...
	if ',' in cuisine:
		cuisines_list = cuisine.split(',')
		new = [a_cuisine.strip('_') for a_cuisine in cuisines_list]

	return new
'''


'''
if __name__ == "__main__":
	print update_street_name("PROL. Feder")
'''