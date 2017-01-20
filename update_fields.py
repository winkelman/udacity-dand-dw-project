#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from scrape_cities import csv_to_list
from audit_fields import get_bad_cuisines


# decode utf-8 and render accents
cities = csv_to_list("cities.csv")
cities = [city.decode('utf-8') for city in cities]


def has_good_city_name(city):
	if city in cities:
		return True

def update_city_name(city):
	new = None
	if re.search('zapopan', city, re.IGNORECASE):
		new = 'Zapopan'
	if re.search('guadalajara', city, re.IGNORECASE):
		new = 'Guadalajara'
	if re.search('tlaquepaque', city, re.IGNORECASE):
		new = 'Tlaquepaque'
	if re.search('tlajomulco', city, re.IGNORECASE):
		new = u'Tlajomulco de Zúñiga'
	if re.search('tonal', city, re.IGNORECASE):
		new = u'Tonalá'
	return new



CODE_PREFIX = ['44', '45', '46', '47', '48']

def has_good_postcode(code):
	if len(code) == 5:
		prefix = code[0:2]
		if prefix in CODE_PREFIX:
			return True

def update_postcode(code):
	if len(code) == 6 and (code[-1] == '0' or code[-1] == ' '):
		code = code[:5]
		return code



av_type_re = re.compile(r'av+\.?\s', re.IGNORECASE)
esq_type_re = re.compile(r'esq+\.?\s', re.IGNORECASE)
prol_type_re = re.compile(r'prol+\.?\s', re.IGNORECASE)

def has_good_street_name(name):
	if av_type_re.search(name) or esq_type_re.search(name) or prol_type_re.search(name):
		return False
	else:
		return True

street_type_map = {'Av ': 'Avenida ', 'Av. ': 'Avenida ',
					'prol. ': u'Prolongación ', 'Prol': u'Prolongación ', 'PROL. ': u'Prolongación ', 'Prol. ': u'Prolongación ',
					'esq. ': 'Esquina ', 'ESQ. ': 'Esquina ', 'Esq. ': 'Esquina '}

def update_street_name(name):
	if av_type_re.search(name):
		old_name_type = av_type_re.search(name).group()
		new_name_type = street_type_map[old_name_type]
		name = name.replace(old_name_type, new_name_type)
	if esq_type_re.search(name):
		old_name_type = esq_type_re.search(name).group()
		new_name_type = street_type_map[old_name_type]
		name = name.replace(old_name_type, new_name_type)
	if prol_type_re.search(name):
		old_name_type = prol_type_re.search(name).group()
		new_name_type = street_type_map[old_name_type]
		name = name.replace(old_name_type, new_name_type)

	return name


'''
filename = 'gdl.osm'
bad_cuisines = get_bad_cuisines(filename)

def has_good_cuisine(cuisine):
	if cuisine not in bad_cuisines:
		return True

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
	print update_city_name("Tonal")
'''