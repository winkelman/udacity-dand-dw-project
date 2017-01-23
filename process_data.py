#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Your task is to wrangle the data and transform the shape of the data
into the model we mentioned earlier. The output should be a list of dictionaries
that look like this:
{
"id": "2406124091",
"type: "node",
"visible":"true",
"created": {
          "version":"2",
          "changeset":"17206049",
          "timestamp":"2013-08-03T16:43:42Z",
          "user":"linuxUser16",
          "uid":"1219059"
        },
"pos": [41.9757030, -87.6921867],
"address": {
          "housenumber": "5157",
          "postcode": "60625",
          "street": "North Lincoln Ave"
        },
"amenity": "restaurant",
"cuisine": "mexican",
"name": "La Cabana De Don Luis",
"phone": "1 (773)-271-5176"
}
You have to complete the function 'shape_element'.
We have provided a function that will parse the map file, and call the function with the element
as an argument. You should return a dictionary, containing the shaped data for that element.
We have also provided a way to save the data in a file, so that you could use
mongoimport later on to import the shaped data into MongoDB. You could also do some cleaning
before doing that, like in the previous exercise, but for this exercise you just have to
shape the structure.
In particular the following things should be done:
- you should process only 2 types of top level tags: "node" and "way"
- all attributes of "node" and "way" should be turned into regular key/value pairs, except:
    - attributes in the CREATED array should be added under a key "created"
    - attributes for latitude and longitude should be added to a "pos" array,
      for use in geospacial indexing. Make sure the values inside "pos" array are floats
      and not strings. 
- if second level tag "k" value contains problematic characters, it should be ignored
- if second level tag "k" value starts with "addr:", it should be added to a dictionary "address"
- if second level tag "k" value does not start with "addr:", but contains ":", you can process it
  same as any other tag.
- if there is a second ":" that separates the type/direction of a street,
  the tag should be ignored, for example:
<tag k="addr:housenumber" v="5158"/>
<tag k="addr:street" v="North Lincoln Avenue"/>
<tag k="addr:street:name" v="Lincoln"/>
<tag k="addr:street:prefix" v="North"/>
<tag k="addr:street:type" v="Avenue"/>
<tag k="amenity" v="pharmacy"/>
  should be turned into:
{...
"address": {
    "housenumber": 5158,
    "street": "North Lincoln Avenue"
}
"amenity": "pharmacy",
...
}
- for "way" specifically:
  <nd ref="305896090"/>
  <nd ref="1719825889"/>
should be turned into
"node_refs": ["305896090", "1719825889"]
"""

import xml.etree.cElementTree as ET
import re
import codecs
import json

from update import has_street_abbv, update_street_name, has_bad_zipcode
from update import has_bad_city_name, update_city

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = ["version", "changeset", "timestamp", "user", "uid"]
education_type = ['school', 'kindergarten', 'college', 'university', 'college;school']


def shape_element(element):

    node = {}
    if element.tag == "node" or element.tag == "way":
        node["type"] = element.tag
        node["created"] = {}
        # node or way attributes first
        for key, val in element.attrib.items():
            # CREATED keys in dictionary
            if key in CREATED:
                node['created'][key] = val
                continue
            # geo location in list
            if key in ['lat', 'lon']:
                # check if have 'pos'
                if 'pos' not in node:
                    node['pos'] = [None, None]
                # asign index for 'pos' list
                idx = 0 if key == 'lat' else 1
                node['pos'][idx] = float(val)
            # all other attributes
            else:
                node[key] = val

        # child tags 
        has_education_amenity, has_sep = False, False # reset for each element
        for tag in element.iter("tag"):
            key = tag.attrib["k"]
            val = tag.attrib["v"]
            # check problem chars
            if problemchars.search(key):
                continue
            # check for uppercase SEP here
            if key == 'SEP:CLAVEESC':
                has_sep = True
                node[key] = val
                continue
            # lowercase keys without colon
            if lower.search(key):
                # check for education amenity
                if key == 'amenity' and val in education_type:
                    has_education_amenity = True
                # fix 'desciption' key
                if key == 'desciption':
                    key = 'description'                
                node[key] = val
                continue
            # lowercase keys with single colon
            if lower_colon.search(key):
                prefix, suffix = key.split(":")
                # address keys
                if prefix == 'addr':
                    if suffix == 'street' and has_street_abbv(val):
                        val = update_street_name(val)
                    if suffix == 'postcode' and has_bad_zipcode(val):
                        continue
                    if suffix == 'city' and has_bad_city_name(val):
                        val = update_city(val)
                node[key] = val
        # fix amenity if has SEP but no education
        if has_sep and not has_education_amenity:
            node['amenity'] = 'school'

        # nd refs to list
        if element.findall("nd"): # namespace conflict with 'find'...
            node["node_refs"] = []
            for nd in element.iter('nd'):
                ref = nd.attrib["ref"]
                node["node_refs"].append(ref)

    return node if node else None


def process_map(file_in, pretty = False):
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data


if __name__ == "__main__":
    pass
    #filename = 'gdl.osm'
    #data = process_map(filename)