#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import codecs
import json
import re


def shape_element(element):
	node = {}
	if element.tag == "node" or element.tag == "way":
		for el in element.iter():
			print(el.tag, el.attrib)
		# return {str(el): str(el)}
	else:
		return None


def process_data(file_in, pretty=False):
	# file_out = "{0}.json".format(file_in)
	file_out = "output.json"
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

# data = process_data('sample.osm', True)

"""
"way"{
	"highway":"footway","path","residential"..
	"oneway": "yes"... or no
	"maxspeed": ...
	"lanes": ...
	"lit":....
	"name": Rue Charles Tellier...
	"service":"parking_aisle",
}

"way"{
	"building": yes,
	"name:"...
	"source":....
	"node_refs" = [83279372,3239287329]
	"roof":{
		"shape": "gabled",
		"levels": 1,
		"material",
	},
}
"""
