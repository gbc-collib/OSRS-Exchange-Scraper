import json

import get_price
ITEM_DATABASE = 'items_osrs.json'

def grab_alc_price():
	with open(ITEM_DATABASE) as f: #opens prebuilt item database and closes as soon as it's importeds
		json_data = json.load(f)
		itemslist = json_data.items()
		high_alc_values = {}
		for item in itemslist:
			high_alc_values[item[1]['name']] = item[1]['value']
		import pdb; pdb.set_trace()


def main(args):
	get_price.item_data(565)
	grab_alc_price()
	return 0

if __name__ == '__main__':
	import sys
	sys.exit(main(sys.argv))
