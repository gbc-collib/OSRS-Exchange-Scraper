import json
import collections
from pathlib import Path
from osrsbox import items_api
from osrsbox import monsters_api
from osrsbox import prayers_api


def generate_items_complete():
	# Read in the item database content
	path_to_items_json = Path("items-complete.json")
	all_db_items = items_api.all_items.AllItems("items-complete.json")
	items = {}

	for item in all_db_items:
		json_out = item.construct_json()
		items[item.id] = json_out

# Save all items to docs/items_complete.json
	out_fi = Path("items-complete-new.json")
	with open(out_fi, "w") as f:
		json.dump(items, f)

# Save all items to osrsbox/docs/items_complete.json
	out_fi = Path("items-complete-new.json")
	with open(out_fi, "w") as f:
		json.dump(items, f)

def main(args):
	generate_items_complete()
if __name__ == '__main__':
	import sys
	sys.exit(main(sys.argv))

