#!/usr/bin/env python
# -*- coding: utf-8 -*-


###
### BEFORE EXECUTING THIS SCRIPT, YOU MUST HAVE A MONGODB INSTANCE OPEN!!!
###


import json
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
# Creating the 'osm' database...
db = client.osm

# Note that below we are inserting each dictionary document one by one into the collection.
# This means that the osm.json file here must not actually be a legit .json file,
# in our case each entry/line is a .json document itself.

def import_json_docs(filename):
	with open(filename, 'r') as fin:
		for line in fin:
			data = json.loads(line)
			db.guadsample.insert(data)


if __name__ == "__main__":
	filename = 'guad-sample.osm.json'
	import_json_docs(filename)