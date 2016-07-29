from pprint import pprint
from collections import defaultdict

before = {
	"test":"ok",
	"verygood":"yes",
	"seamark:topmark:shape":"2 cones base together",
	"seamark:topmark:colour":"black",
	"seamark:buoy_cardinal:shape":"spar",
	"seamark:buoy_cardinal:colour":"black;yellow;black",
	"seamark:buoy_cardinal:category":"east",
	"seamark:buoy_cardinal:colour_pattern":"horizontal",
}

after = {
	"test":"ok",
	"verygood":"yes",
	"seamark": {
		"topmark": {
			"shape": "2 cones base together",
			"colour": "black",
		},
		"buoy_cardinal": {
			"shape": "spar",
			"colour": ["black", "yellow", "black"],
			"category": "east",
			"colour_pattern": "horizontal",
		}
	}
}



def nested_dict():
	return defaultdict(nested_dict)
a = nested_dict()
a['a']['b']['c']['didin'] = 1
a['a']['b']['d']['oulaaalala'] = 2



def clean_default_dict(d):
	if isinstance(d, defaultdict):
		d = dict(d)
	for k, v in d.items():
		if isinstance(v, defaultdict):
			d[k] = clean_default_dict(v)
	return d


def create_nested_dicts(data):
	"""
		Returns a list of nested dictionaries
		mapping only one value.
		[ {'seamark': {'buoy_cardinal': {'colour_pattern': 'horizontal'}}},
		  {'seamark': {'topmark': {'shape': '2 cones base together'}}} ... ]
	"""
	nodes = []
	for k, v in data.items():
		if ":" in str(k):
			k_elems = k.split(':')
			node = v
			for k in reversed(k_elems):
				node = {k: node}
			nodes.append(node)
	return nodes

import collections
def update_nested_dict(d, nested_dict):
	"""
		This functions uses recursion to update nested dicts
		while avoiding duplicates. By looping this function over the list
		of values extracted by create_nested_dicts we build our final valid nested dict.
	"""
	for k, v in nested_dict.items():
		if isinstance(v, collections.Mapping):
			r = update_nested_dict(d.get(k, {}), v)
			d[k] = r
		else:
			d[k] = nested_dict[k]
	return d

data_list = create_nested_dicts(before)
b = {}
for el in data_list:
	update_nested_dict(b, el)

pprint(b)
pprint(after)
pprint(b == after)

def process_data2(data):
	nodes = nested_dict()
	for k, v in data.items():
		if ":" in str(k):
			k_elems = k.split(':')
			nodes = process_keys(nodes, k_elems, v)
			break
	return nodes
#
# def process_keys(nodes, k_elem, v):
# 	if len(k_elem) > 0:
# 		nodes[k_elem[0]] = v
# 		process_keys(nodes, k_elem[1:], nodes)
# 	else:
# 		return nodes

if __name__ == '__main__':
	# pprint(process_data(before))
	# pprint(process_data2(before))
	# assert process_data(before) == after
	pass


def nested_dict():
	return defaultdict(nested_dict)
a = nested_dict()
a['a']['b']['c'] = 1
a['a']['b']['d'] = 2
# print(clean_default_dict(a))

b = ['a','b','c']
c = 1
