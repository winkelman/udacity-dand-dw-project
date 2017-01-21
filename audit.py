#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ET
import pprint
import re
from scrape_cities import csv_to_list


def order_dict_by_val(input_dict):
    return sorted(input_dict.items(), key = lambda x: x[1], reverse=True)


def audit_elements(filename):
        tags_dict = {} # set() for no counts
        for event, elem in ET.iterparse(filename):
            tag = elem.tag

            if tag not in tags_dict:
                tags_dict[tag] = 1
            else:
                tags_dict[tag] += 1

        return order_dict_by_val(tags_dict)


def audit_tag_keys(filename):
        keys_dict = {}
        for event, elem in ET.iterparse(filename):
            for attr in elem.iter("tag"):
                k = attr.attrib["k"]

                if k not in keys_dict:
                    keys_dict[k] = 1
                else:
                    keys_dict[k] += 1

        return order_dict_by_val(keys_dict)


def audit_tag_values(filename, attribute):
        vals_dict = {}
        for event, elem in ET.iterparse(filename):
            for attr in elem.iter("tag"):
                k = attr.attrib["k"]
                v = attr.attrib["v"]

                if attribute in k:
                    if v not in vals_dict:
                        vals_dict[v] = 1
                    else:
                        vals_dict[v] += 1

        return order_dict_by_val(vals_dict)


def cross_ref_sep(filename):
    count = 0
    education_type = ['school', 'kindergarten', 'college',
                        'university', 'college;school'
                        ]
    for event, elem in ET.iterparse(filename):
        has_sep, has_school = False, False
        for attr in elem.iter("tag"):
            k = attr.attrib["k"]
            v = attr.attrib["v"]

            if k == "SEP:CLAVEESC":
                has_sep = True
            if k == "amenity" == k and v in education_type:
                has_school = True
            if has_sep and has_school:
                count += 1
                break
    return count


def get_street_abbv():
    data = audit_tag_values("gdl.osm", "addr:street")
    abbv = set()
    for street, count in data:
        match = re.search(r'^[\w]+(\s|\.)', street)
        if match:
            abbv.add(match.group())
    return abbv


def get_bad_zipcode():
    data = audit_tag_values("gdl.osm", "addr:postcode")
    # valid zipcode begins with 44-48
    invalid = [code for code, count in data if not re.search(r'^4[4-8]\d{3}$', code)]
    return set(invalid)


def get_bad_cities():
    # decode utf-8 and render accents
    good_cities = [city.decode('utf-8') for city in csv_to_list("cities.csv")]
    good_cities.append(u'Tonalá') # this major city not in wikipedia
    cities = audit_tag_values("gdl.osm", "addr:city")
    bad_cities = [city for city, count in cities if city not in good_cities]
    return set(bad_cities)


if __name__ == "__main__":

    pprint.pprint(get_bad_cities())

    #shops = audit_attribute_values(filename, 'shop')
    #pprint.pprint(shops)

    #religions = audit_attribute_values(filename, 'religion')
    #pprint.pprint(religions)

    #sports = audit_attribute_values(filename, 'sport')
    #pprint.pprint(sports)

    #cuisines = audit_attribute_values(filename, 'cuisine')
    #pprint.pprint(cuisines)