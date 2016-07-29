#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
from pprint import pprint
import collections
import codecs
import json
import re
import os

street_type_re = re.compile(r'([^\s]+)', re.IGNORECASE)

expected_street_types = []
with open('common_street_types.json', 'rw') as f:
	expected_street_types = [str(e.encode('utf-8')) for e in json.load(f)]

def is_street_name(elem):
	return (elem.attrib['k'] == "addr:street")

def lowercase_list(value_list):
	return(str(v).lower() for v in value_list)

corrected_mapping = {
	"rue": "Rue",
	"quai": "Quai",
	"Saint": "Rue",
	"La": "La",
	"françois": "Rue François",
}

def clean_street_type(tag):
	street_name = str(tag.attrib.get('v').encode('utf-8'))
	# street_name = tag.attrib.get('v')
	m = street_type_re.search(street_name)
	val = m.group()
	if m and (val not in expected_street_types):
		if val.lower() in lowercase_list(expected_street_types):
			bad_to_good = dict(zip(lowercase_list(expected_street_types), expected_street_types)) # {'boulevard': 'Boulevard', ...}
			street_name = street_name.replace(val, bad_to_good[val])
		else:
			if corrected_mapping.get(val):
				street_name = street_name.replace(val, corrected_mapping[val])
	return street_name

def process_value(value):
	"""
		Process a value to return it in the correct format:
			- numbers are converted to int, or float.
			- text with ";" charaters but no blank space are split and a list of processed values is returned.
			- unicode values are converted to string
	"""
	if ';' in value and ' ' not in value:
		process_value(value.split(';'))
	else:
		if isinstance(value, list):
			return [process_value(v) for v in value]
		else:
			try:
				value = int(value)
			except ValueError:
				try:
					value = float(value)
				except ValueError:
					try:
						value = str(value.encode('utf8'))
					except:
						pass
	return value

def process_data(osmfile):
	"""
		This function iterates over the "node" and "way" elements of the XML file,
		processing the values and keys of each of their tags and returning a list of nested
		dictionaries ready to be saved to the JSON file.
	"""
	osm_file = open(osmfile, 'r')
	nodes = []
	for event, elem in ET.iterparse(osm_file, events=("start",)):
		if elem.tag == "node" or elem.tag == "way":
			node = {"type": elem.tag}
			for k, v in elem.attrib.items():
				node[k] = process_value(v)
			for tag in elem.iter("tag"):
				k, v = tag.attrib.get('k'), (tag.attrib.get('v') if not is_street_name(tag) else clean_street_type(tag))
				if k and v:
					nested = create_nested_dict({k: process_value(v)})
					update_nested_dict(node, nested)
			for nd in elem.iter("nd"):
				if "ref" in nd.attrib.keys():
					val = process_value(nd.attrib['ref'])
					if node.get('node_refs'):
						node['node_refs'].append(val)
					else:
						node['node_refs'] = [val,]
			nodes.append(node)
	return nodes

def process_map(file_in, pretty = False):
	"""
		This function calls process_data for the file_in
		then writes a JSON file with the returned dict values.
	"""
	name, ext = os.path.splitext(file_in)
	file_out = "processed-{0}.json".format(name)

	data = process_data(file_in)

	with codecs.open(file_out, "w") as f:
		if pretty:
			f.write(json.dumps(data, indent=2)+"\n")
		else:
			f.write(json.dumps(data) + "\n")

def create_nested_dict(data):
	"""
		Returns a list of nested dictionaries
		mapping only one value.
		[ {'seamark': {'buoy_cardinal': {'colour_pattern': 'horizontal'}}},
		  {'seamark': {'topmark': {'shape': '2 cones base together'}}} ... ]
	"""
	nested_dicts = []
	for k, v in data.items():
		if ":" in str(k):
			k_elems = k.split(':')
			node = v
			for k in reversed(k_elems):
				node = {k: node}
		else:
			node = {k: v}
	return node

def update_nested_dict(d, nested_dict):
	"""
		This functions uses recursion to update nested dicts
		while avoiding duplicates. By looping this function over the list
		of values extracted by create_nested_dicts we build our final valid nested dictionary.
	"""
	for k, v in nested_dict.items():
		if isinstance(d, collections.Mapping):
			if isinstance(v, collections.Mapping):
				r = update_nested_dict(d.get(k, {}), v)
				d[k] = r
			else:
				d[k] = nested_dict[k]
		else:
			d = {k: nested_dict[k]}
	return d


process_map('la-rochelle_france.osm', pretty=True)
