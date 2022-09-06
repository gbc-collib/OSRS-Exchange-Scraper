#itemdb_oldschool
#https://secure.runescape.com/m=itemdb_oldschool/api/catalogue/detail.json?item=379
import urllib2 #for handling url requests
import urllib
import json #converts string data into usable dictionary
import ast
class item_data:
	def __init__(self, item_name):
		self.item_name = item_name
	def grab_data(self): #to handle calling wiki and grabbing raw data and converting to usable format	
		item_url = 'https://secure.runescape.com/m=itemdb_oldschool/api/catalogue/detail.json?item='
		raw_data = urllib2.urlopen(item_url + (self.item_name))
		for line in raw_data:
			raw_data = line
			#print(raw_data)
		data = json.loads(raw_data)
		return data
def main(args):
	print('What item would you like price info for?')
	SGS = item_data(raw_input())
	data = SGS.grab_data()
	print(data['item']['name'] + 's cost ' + str(data['item']['current']['price']))
	return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
