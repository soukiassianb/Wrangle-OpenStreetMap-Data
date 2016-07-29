#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
from collections import defaultdict
from operator import itemgetter

def audit_street_type(osmfile):
	osm_file = open(osmfile, 'r')
	tag_elems = defaultdict(int)
	for event, elem in ET.iterparse(osm_file, events=("start",)):
		if elem.tag == "node" or elem.tag == "way":
			for tag in elem.iter("tag"):
				k = tag.get('k')
				if k:
					tag_elems[k] += 1
	return sorted(tag_elems.items(), key=itemgetter(1), reverse=True)

tags = audit_street_type("la-rochelle_france.osm")
for i, j in tags:
	print(i)
