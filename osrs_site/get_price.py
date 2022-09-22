#itemdb_oldschool
#https://secure.runescape.com/m=itemdb_oldschool/api/catalogue/detail.json?item=379
import requests #for handling url requests
import json #converts string data into usable dictionary
import datetime

class ItemData:
	def __init__(self, item_id): #item name accepts string of item name or iteger of item ID
		self.item_id = item_id
		self.item_name = None
	def name_to_id(self):
		item_url = 'http://prices.runescape.wiki/api/v1/osrs/mapping'
		headers = {
			'User-Agent': 'gbc_collib\'s amateur price tracker',
			'From': 'collinstasiak@gmail.com'
		}
		raw_data = requests.get(item_url, headers=headers, stream=True)
		data = raw_data.json() # uses response's json handling to return dictoinary of item data
		for item in data:
			if ''.join(item['name'].lower().split()) == ''.join(self.item_id.lower().split()): #checks name to item id database and normalizes caps to make user friendly
				self.item_name = item['name']
				self.item_id = str(item['id']) #return the id
				return self.item_id
		return False
	def id_to_name(self):
		url = 'https://secure.runescape.com/m=itemdb_oldschool/api/catalogue/detail.json?item='
		raw_data = requests.get(url + str(self.item_id))
		if raw_data.status_code == 404:
			self.item_name = 'Invalid'
			return False
		data = raw_data.json()
		self.item_name = data['item']['name']

	def grab_data(self): #to handle calling wiki and grabbing raw data to convert to usable format, returns a dictionary of item data if it's valid item, returns 0 if not
		item_url = 'http://prices.runescape.wiki/api/v1/osrs/latest'
		headers = {
			'User-Agent': 'gbc_collib\'s amateur price tracker',
			'From': 'collinstasiak@gmail.com'
		}
		raw_data = requests.get(item_url, headers=headers)
		data = raw_data.json() # uses response's json handling to return dictoinary of item data
		if self.item_id.isnumeric(): #if passed item name instead of id convert it
			self.id_to_name()
		else:
			self.name_to_id()
		if self.item_id in data['data']:
			formatted_data = {
			'name': self.item_name,
			'item_id': self.item_id,
			'high': data['data'][self.item_id]['high'],
		 	'low': data['data'][self.item_id]['low'],
		 	'icon': 'https://secure.runescape.com/m=itemdb_oldschool/1663239679537_obj_big.gif?id=' + str(self.item_id)
		 	}
			return formatted_data
		return False
def main(args):
	requested_item_data = 0
	while requested_item_data == 0: #keeps running until item is found maybe not good
		requested_item_data = ItemnData(input('What item would you like price info for?\n')).grab_data()
	time_retrieved = datetime.datetime.now()
	print(requested_item_data['name'] + 's profit margin is ' + str(requested_item_data['high'] - requested_item_data['low']) + ' at ' + time_retrieved.strftime("%H:%M:%S"))
	return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
