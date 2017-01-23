#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from audit import get_good_cities


def has_street_abbv(street_name):
	match = re.search(r'^(av[e]?|carr|dom|prol)(\s|\.)', street_name, re.IGNORECASE)
	return match is not None

street_abbv_map = {'av': 'Avenida', 'ave': 'Avenida',
					'carr': 'Carretera',
					'dom': 'Domicilio',
					'prol': u'Prolongación'}

def update_street_name(street_name):
	parts = re.split('\.| ', street_name) # split on period or whitespace
	# could also use re.findall(r'[\w]+', street_name)
	abbv = parts[0]
	# map keys are lowercase
	new_name = re.sub(abbv + r'[\.]?', street_abbv_map[abbv.lower()], street_name)
	return new_name


def has_bad_zipcode(code):
	match = re.search(r'^4[4-8]\d{3}$', code)
	return match is None


good_cities = get_good_cities()

def has_bad_city_name(city):
	return city not in good_cities

gdl = re.compile(r'guad', re.IGNORECASE)
zpn = re.compile(r'zapop', re.IGNORECASE)
tnl = re.compile(r'tonal', re.IGNORECASE)
tpq = re.compile(r'tlaque', re.IGNORECASE)
tjm = re.compile(r'tlajom', re.IGNORECASE)

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
	# if bad and cannot update, don't allow city
	return None


if __name__ == "__main__":
	pass
	#print update_street_name("PROL. Feder")