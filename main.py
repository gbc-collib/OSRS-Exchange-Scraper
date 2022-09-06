#itemdb_oldschool
#https://secure.runescape.com/m=itemdb_oldschool/api/catalogue/detail.json?item=379
import urllib2 #for handling url requests
import json #converts string data into usable dictionary
import ast
def main(args):
	raw_data = urllib2.urlopen('https://secure.runescape.com/m=itemdb_oldschool/api/catalogue/detail.json?item=379')
	for line in raw_data:
		raw_data = line
		#print(raw_data)
	data = json.loads(raw_data)
	print(data['item']['name'] + 's cost ' + str(data['item']['current']['price']))
	return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
