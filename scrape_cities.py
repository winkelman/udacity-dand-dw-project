#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import pprint

def get_cities():
    
    r = requests.get("https://en.wikipedia.org/wiki/Category:Populated_places_in_Jalisco")
    soup = BeautifulSoup(r.text)
    cities = []

    letter_categories = soup.find_all('div', {"class":"mw-category-group"})
    for category in letter_categories[1:]:
        city_tags = category.find_all('a')
        for city_tag in city_tags:
            city = city_tag['title']
            # Anything that is 'unicode' needs to be converted to 'UTF-8' or it will throw an error...
            if isinstance(city, unicode):
                city = city.encode('UTF-8')
            if ',' in city:
                index = city.find(',')
                city = city[0:index]
            cities.append(city)

    return cities


if __name__ == "__main__":
    cities = get_cities()
    pprint.pprint(cities)