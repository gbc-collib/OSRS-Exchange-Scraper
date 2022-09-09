#itemdb_oldschool
#https://secure.runescape.com/m=itemdb_oldschool/api/catalogue/detail.json?item=379
import requests #for handling url requests
import json #converts string data into usable dictionary
import datetime


ITEM_DATABASE = 'items_osrs.json' #const for item database pulled from online


class item_data:
	def __init__(self, item_id): #item name accepts string of item name or iteger of item ID
		self.item_id = item_id
	def name_to_id(self):
		with open(ITEM_DATABASE) as f: #opens prebuilt item database and closes as soon as it's importeds
			json_data = json.load(f)
		itemsList = json_data.items()
		for item in itemsList:
			if item[1]['name'].lower() == self.item_id.lower(): #checks name to item id database and normalizes caps to make user friendly
				self.item_id = str(item[0]) #return the id
				
	def grab_data(self): #to handle calling wiki and grabbing raw data to convert to usable format, returns a dictionary of item data if it's valid item, returns 0 if not
		item_url = 'https://secure.runescape.com/m=itemdb_oldschool/api/catalogue/detail.json?item='
		if isinstance(self.item_id,str): #if passed item name instead of id convert it
			self.name_to_id()
		raw_data = requests.get(item_url + str((self.item_id))) #pull item data from osrs api
		if raw_data.status_code == 404: #will only give 404 error if item doesnt exist
			print('No Item found')
			return False
		data = raw_data.json() # uses response's json handling to return dictoinary of item data
		return data['item']
		
def main(args):
	requested_item_data = 0
	while requested_item_data == 0: #keeps running until item is found maybe not good
		requested_item_data = item_data(input('What item would you like price info for?\n')).grab_data()
	time_retrieved = datetime.datetime.now()
	print(requested_item_data['item']['name'] + 's cost ' + str(requested_item_data['item']['current']['price']) + ' at ' + time_retrieved.strftime("%H:%M:%S"))
	return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
