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
	return high_alc_values

def alc_profit(items=grab_alc_price(), margin=10): #takes dict keyed by item name with value of high alc, defaults to all items
	nature_rune_cost = get_price.ItemData('561').grab_data()['low']
	profittable_alc = {}
	for name, price in items.items():
		ge_price = get_price.ItemData(name).grab_data()
		if not ge_price:
			continue
		ge_price = ge_price['low']
		actual_margin = ge_price - nature_rune_cost
		if  actual_margin > margin:
			profittable_alc[name] = actual_margin
	return profittable_alc

def main(args):
	print(alc_profit())
	
	return 0

if __name__ == '__main__':
	import sys
	sys.exit(main(sys.argv))
