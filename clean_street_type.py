#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET  # Use cElementTree or lxml if too slow
from collections import defaultdict
import pprint, re
from operator import itemgetter
import json

# Regex matches first word from string
street_type_re = re.compile(r'([^\s]+)', re.IGNORECASE)

# Load expected_street_types from our common_street_types.json file
expected_street_types = []
with open('common_street_types.json', 'rw') as f:
	expected_street_types = [e.encode('utf-8') for e in json.load(f)]

def is_street_name(elem):
	return (elem.attrib['k'] == "addr:street")

def lowercase_list(value_list):
	return(str(v).lower() for v in value_list)

def audit_street_type(osmfile):
	osm_file = open(osmfile, 'r')
	streets = defaultdict(int)
	for event, elem in ET.iterparse(osm_file, events=("start",)):
		if elem.tag == "node" or elem.tag == "way":
			for tag in elem.iter("tag"):
				if is_street_name(tag):
					street_name = str(tag.attrib.get('v').encode('utf-8'))
					m = street_type_re.search(street_name)
					if m and m.group() not in expected_street_types:
						streets[m.group()] += 1
						c = clean_street_type(tag)
					#if m.group().lower() not in lowercase_list(expected_street_types):
						# print(tag.attrib['v'].encode('utf-8'))
	return sorted(streets.items(), key=itemgetter(1), reverse=True)

mapping = {
	"rue": "Rue",
	"quai": "Quai",
	"Saint": "Rue",
	"La": "La",
	"françois": "Rue François",
}

def clean_street_type(tag):
	street_name = str(tag.attrib.get('v').encode('utf-8'))
	m = street_type_re.search(street_name)
	val = m.group()
	if m and (val not in expected_street_types):
		if val.lower() in lowercase_list(expected_street_types):
			bad_to_good = dict(zip(lowercase_list(expected_street_types), expected_street_types)) # {'boulevard': 'Boulevard', ...}
			street_name = street_name.replace(val, bad_to_good[val])
		else:
			if mapping.get(val):
				street_name = street_name.replace(val, mapping[val])
	return street_name

audit_street_type("la-rochelle_france.osm")
