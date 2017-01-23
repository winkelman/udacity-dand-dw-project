#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ET
import re
from scrape_cities import csv_to_list
import pprint


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
                key = attr.attrib["k"]

                if key not in keys_dict:
                    keys_dict[key] = 1
                else:
                    keys_dict[key] += 1

        return order_dict_by_val(keys_dict)


def audit_tag_values(filename, attribute):
        vals_dict = {}
        for event, elem in ET.iterparse(filename):
            for attr in elem.iter("tag"):
                key = attr.attrib["k"]
                val = attr.attrib["v"]

                if key == attribute:
                    if val not in vals_dict:
                        vals_dict[val] = 1
                    else:
                        vals_dict[val] += 1

        return order_dict_by_val(vals_dict)


education_type = ['school', 'kindergarten', 'college', 'university', 'college;school']

def cross_ref_sep(filename):
    count = 0
    for event, elem in ET.iterparse(filename):
        has_sep, has_school = False, False
        for attr in elem.iter("tag"):
            key = attr.attrib["k"]
            val = attr.attrib["v"]

            if key == "SEP:CLAVEESC":
                has_sep = True
            if key == "amenity" and val in education_type:
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


def get_good_cities():
    # decode utf-8 and render accents
    good_cities = [city.decode('utf-8') for city in csv_to_list("cities.csv")]
    good_cities.append(u'Tonalá') # this major city not in wikipedia
    return good_cities


def get_bad_cities():
    good_cities = get_good_cities()
    cities = audit_tag_values("gdl.osm", "addr:city")
    bad_cities = [city for city, count in cities if city not in good_cities]
    return set(bad_cities)


if __name__ == "__main__":
    pass

    #pprint.pprint(get_street_abbv())
    #pprint.pprint(get_bad_zipcode())
    #pprint.pprint(get_bad_cities())


    # other attributes to consider

    #shops = audit_attribute_values(filename, 'shop')
    #pprint.pprint(shops)

    #religions = audit_attribute_values(filename, 'religion')
    #pprint.pprint(religions)

    #sports = audit_attribute_values(filename, 'sport')
    #pprint.pprint(sports)

    #cuisines = audit_attribute_values(filename, 'cuisine')
    #pprint.pprint(cuisines)