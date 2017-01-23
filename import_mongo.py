#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from pymongo import MongoClient

# open mongodb connection from shell before running this
client = MongoClient("mongodb://localhost:27017")
# create 'osm' database
db = client.osm
# insert each dictionary one by one
# osm.json is not technically JSON but collection of JSONs
def import_json(filename):
	with open(filename, 'r') as fin:
		for line in fin:
			data = json.loads(line)
			db.gdl.insert(data)


if __name__ == "__main__":
	pass
	#filename = 'gdl.osm.json'
	#import_json(filename)