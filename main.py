#itemdb_oldschool
#https://secure.runescape.com/m=itemdb_oldschool/api/catalogue/detail.json?item=379
import urllib2 #for handling url requests
import json #converts string data into usable dictionary


ITEM_DATABASE = 'items_osrs.json' #const for item database pulled from online


class item_data:
	def __init__(self, item_id): #item name accepts string of item name or iteger of item ID
		self.item_id = item_id
	def name_to_id(self):
		with open(ITEM_DATABASE) as f:
			json_data = json.load(f)
		itemsList = json_data.items()
		for item in itemsList:
			if item[1]['name'] == self.item_id:
				self.item_id = str(item[0])
				
	def grab_data(self): #to handle calling wiki and grabbing raw data to convert to usable format, returns a dictionary of item data
		item_url = 'https://secure.runescape.com/m=itemdb_oldschool/api/catalogue/detail.json?item='
		if isinstance(self.item_id,str):
			self.name_to_id()
		raw_data = urllib2.urlopen(item_url + str((self.item_id)))
		for line in raw_data:
			raw_data = line
			#print(raw_data)
		data = json.loads(raw_data)
		return data
		
	def item_image(self):
		image_url = 'https://secure.runescape.com/m=itemdb_oldschool/api/obj_sprite.gif?id='
		image = urllib2.urlopen(image_url + str((self.item_id)))
def main(args):
	print('What item would you like price info for?')
	SGS = item_data(raw_input())
	data = SGS.grab_data()
	print(data['item']['name'] + 's cost ' + str(data['item']['current']['price']))
	return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
