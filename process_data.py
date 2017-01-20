#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json

from update_fields import has_good_city_name, update_city_name, has_good_postcode, update_postcode
from update_fields import has_good_street_name, update_street_name #has_good_cuisine, update_cuisine

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
#problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = ["version", "changeset", "timestamp", "user", "uid"]



def get_tag_types(element):
    types = set()
    for elem in element.iter():
        tag = elem.tag
        types.add(tag)
    return types

def get_atrb_types(element):
    types = set()
    for elem in element.iter():
        atrbs = elem.keys()
        for atrb in atrbs:
            types.add(atrb)
    return types



def has_address(element):
    if 'tag' in get_tag_types(element):
        for tag in element.iter("tag"):
            k = tag.attrib["k"]
            if lower_colon.search(k) and k.find("addr:") != -1:
                return True

def has_pos(element):
    atrb_list = get_atrb_types(element)
    return 'lon' in atrb_list or 'lat' in atrb_list

def has_node_refs(element):
    return 'nd' in get_tag_types(element)



def shape_element(element):
    node = {}
    if element.tag == "node" or element.tag == "way":

        # Store these as booleans for ease if we want to use them more than once...
        has_address_bool = has_address(element)
        has_pos_bool = has_pos(element)
        has_nodes_bool = has_node_refs(element)
        # Each element has these keys...
        node["type"] = element.tag
        node["created"] = {}


        ##### Taking care of attributes in 'node' or 'way' tags #####
        if has_pos_bool:
            node["pos"] = []

        keyval_pairs = element.items()
        for key, val in keyval_pairs:
            if key in CREATED:
                node["created"][key] = val
            elif has_pos_bool and (key == 'lon' or key == 'lat'):
                # If coordinates exist then we cast as floats an add to the list,
                # technically don't need to use the boolean value here but adds readability...
                node["pos"].append(float(val))
                # The longitude gets switched and it needs to be after the latitude for the grader...
                node["pos"].reverse()
            else:
                node[key] = val
    

        ##### Testing validity of 'k' attribute values in the 'tag' elements #####
        if has_address_bool:
            node["address"] = {}

        for tag in element.iter("tag"):
            k = tag.attrib["k"]
            v = tag.attrib["v"]
            # Encoding is a problem, making sure everything is utf-8...
            if isinstance(v, unicode):
                v = v.encode('UTF-8')

            '''
            if problemchars.search(k):
                pass
            '''
            ### Attribute names without a colon here ###
            if lower.search(k):
                # Some inconsistencies with labelling 'parking' in 'amenity'...
                if k == 'amenity' and 'parking' in v:
                    v = 'parking'
                # Fixing the cuisine field values...
                '''
                if k == 'cuisine':
                    if not has_good_cuisine(v):
                        v = update_cuisine(v)
                node[k] = v
                '''

            ### Attribute names with a colon here ###
            elif lower_colon.search(k):
                if has_address_bool and k.find("addr:") != -1:
                    # If we have and are looking at an address,
                    # then we add the tag/type as key and it's value to the 'address' dictionary.
                    # Technically we don't need to use the boolean value here but adds readability...
                    addr_tag = lower_colon.search(k).group()[5:]

                    ### Here we will test for and update fields if necessary ###
                    if addr_tag == 'city':
                        if not has_good_city_name(v):
                            v = update_city_name(v)
                    if addr_tag == 'postcode' and not has_good_postcode(v):
                        v = update_postcode(v)
                    if addr_tag == 'street':
                        if not has_good_street_name(v):
                            v = update_street_name(v)
                    if v:
                        # If we end up with not a valid attribute value then we do nothing...
                        node["address"][addr_tag] = v
                else:
                    # If we have a colon but it's not an address we still add...
                    node[k] = v

            ### Attributes that are not either without a colon or with only one colon we skip ###
            else:
                pass



        ##### If there are node references then we add to a list #####
        if has_nodes_bool:
            node["node_refs"] = []
            for nd in element.iter("nd"):
                ref = nd.attrib["ref"]
                node["node_refs"].append(ref)

        
        return node
    else:
        return None



def process_map(file_in, pretty = False):
    file_in_name = str(file_in)
    index_period = file_in_name.find('.')
    file_in_name = file_in_name[0:index_period]
    file_out = "{0}.osm.json".format(file_in_name)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            doc = shape_element(element)
            if doc:
                data.append(doc)
                if pretty:
                    fo.write(json.dumps(doc, indent=2)+"\n")
                else:
                    fo.write(json.dumps(doc) + "\n")
    return data



if __name__ == "__main__":
    filename = 'gdl.osm'
    data = process_map(filename)