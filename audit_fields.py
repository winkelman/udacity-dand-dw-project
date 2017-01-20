#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ET
import pprint
import re

def order_dict_by_val(input_dict):
    return sorted(input_dict.items(), key = lambda x: x[1], reverse=True)

def audit_elements(filename):
        #tags = set()
        tags_dict = {}
        for event, elem in ET.iterparse(filename):
            tag = elem.tag
            #if tag not in tags:
            #    tags.add(tag)

            if tag not in tags_dict:
                tags_dict[tag] = 1
            else:
                tags_dict[tag] += 1

        return order_dict_by_val(tags_dict)


def audit_tag_keys(filename):
        #attributes_keys = set()
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


lower = re.compile(r'^([a-z]|_)*$')

'''
def get_bad_cuisines(filename):
    bad = []
    cuisines = [pair[0] for pair in audit_tag_values(filename, 'cuisine')]
    for cuisine in cuisines:
        if isinstance(cuisine, unicode):
            cuisine = cuisine.encode('UTF-8')
        if not lower.search(cuisine):
            bad.append(cuisine)
    return bad
'''


if __name__ == "__main__":

    print audit_tag_values("gdl.osm", "cuisine")
    #filename = 'gdl-sample.osm'
    #print get_bad_cuisines(filename)

    #print audit_tags(filename)

    # Audit tags
    #tags = audit_tags(filename)
    #pprint.pprint(tags)
    
    # Audit tag attributes
    #attributes_keys = audit_tag_attributes(filename)
    #pprint.pprint(attributes_keys)

    # Audit cities names
    #cities = audit_attribute_values(filename, 'addr:city')
    #pprint.pprint(cities)

    # Audit post codes
    #codes = audit_attribute_values(filename, 'addr:postcode')
    #pprint.pprint(codes)

    # Audit street names
    #names = audit_attribute_values(filename, 'addr:street')
    #pprint.pprint(names)

    # Audit amenities...
    #amenities = audit_attribute_values(filename, 'amenity')
    #pprint.pprint(amenities)

    # Audit shops... most popular: convenience, supermarket
    #shops = audit_attribute_values(filename, 'shop')
    #pprint.pprint(shops)

    # Audit religions... most popular: christian, 3 jewish
    #religions = audit_attribute_values(filename, 'religion')
    #pprint.pprint(religions)

    # Audit sports... most popular: soccer, basketball, tennis, baseball, volleyball, swimming
    #sports = audit_attribute_values(filename, 'sport')
    #pprint.pprint(sports)

    # Audit cuisines... most popular: mexican, pizza, burger
    #cuisines = audit_attribute_values(filename, 'cuisine')
    #pprint.pprint(cuisines)
    # Cuisine names that are inconsistent...
    #bad_cuisines = get_bad_cuisines(filename)
    #pprint.pprint(bad_cuisines)