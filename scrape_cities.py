#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import csv
import unicodecsv
import pprint


def get_cities():
    cities = []
    r = requests.get("https://en.wikipedia.org/wiki/Category:Populated_places_in_Jalisco")
    soup = BeautifulSoup(r.text, "lxml")
    first_letter_divs = soup.find_all('div', {"class":"mw-category-group"})

    for div in first_letter_divs:
        city_tags = div.find_all('a', title=True)

        for tag in city_tags:
            city = tag['title']
            # some cities with county or state separated by comma
            if ',' in city:
                city = city.split(",")[0]

            cities.append(city)
    return cities


def list_to_csv(list_data, filename):
    with open(filename, 'w') as csvout:
        # cities with accents in unicode handled here
        writer = unicodecsv.writer(csvout, encoding = 'utf-8')
        writer.writerow(list_data)


def csv_to_list(csv_file):
    with open(csv_file, 'r') as csvin:
        reader = csv.reader(csvin)
        return next(reader)


if __name__ == "__main__":
    pass
    #city_data = get_cities()
    #list_to_csv(city_data, "cities.csv")
    #pprint.pprint(city_data)