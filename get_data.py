#!/usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import Popen
import os
import time

have_gdl_data = os.path.isfile("gdl.osm")

def get_gdl():
    source_file = "https://s3.amazonaws.com/mapzen.odes/ex_tvaWMoe8QMguj4B6VLUnzwrfCbNc4.osm.bz2"
    dest_file = "gdl.osm.bz2"
    download = ["wget", "-O", dest_file, source_file]
    process = Popen(download)

    time.sleep(15) # there is a better way than this
    extract = "bunzip2 gdl.osm.bz2".split()
    process = Popen(extract)

if __name__ == "__main__" and not have_gdl_data:
	get_gdl()