import xml.etree.ElementTree as ET  # Use cElementTree or lxml if too slow
from collections import defaultdict
import pprint

def is_street_name(elem):
	return (elem.attrib['k'] == "addr:street")

def audit(osmfile):
	osm_file = open(osmfile, 'r')
	streets = []
	for event, elem in ET.iterparse(osm_file, events=("start",)):
		if elem.tag == "node" or elem.tag == "way":
			for tag in elem.iter("tag"):
				if is_street_name(tag):
					street_name = tag.attrib.get('v').encode('utf8')
					streets.append(street_name)
	return streets
print(audit("sample.osm"))


def count_tags(filename):
	tags = defaultdict(int)
	for event, elem in ET.iterparse(open(filename, 'r'), events=("start",)):
		tags[elem.tag] += 1
	return tags

#print(count_tags("sample.osm"))
