# itemdb_oldschool
# https://secure.runescape.com/m=itemdb_oldschool/api/catalogue/detail.json?item=379
import datetime
import json  # converts string data into usable dictionary
import logging

import requests  # for handling url requests

DATABASE = 'data_base.json'


# Use a singleton class to ensure that no matter how many items are pulled we are using one api request
# Api gets called from too many different places so implementing this control makes it easiest.
class API(object):
    _instance = None
    api_data = None
    time = datetime.datetime.now()

    def __new__(cls):
        # Only get new api object if one does not exist or is older than 5 minutes ( 300 seconds)
        if not cls._instance or ((datetime.datetime.now() - cls.time).total_seconds() > 300):
            cls._instance = super(API, cls).__new__(cls)
            cls.api_data = establish_connection()
            cls.time = datetime.datetime.now()
        return cls._instance


def establish_connection():
    logging.basicConfig(filename='error_log.log', encoding='utf-8', level=logging.ERROR)
    try_counter = 0
    while try_counter < 3:
        try:
            api_data = requests.get('http://prices.runescape.wiki/api/v1/osrs/latest',
                                    headers={'User-Agent': 'gbc_collib\'s amateur price tracker',
                                             'From': 'collinstasiak@gmail.com'})
        except requests.exceptions.Timeout as erorr:
            logging.erorr(erorr)
            try_counter += 1
        break

    return api_data


class ItemData():
    def __init__(self, item_id):  # item name accepts string of item name or iteger of item ID
        self.item_id = item_id
        self.item_name = None
        self.high = None
        self.low = None
        self.icon = None
        API()

    def name_to_id(self):
        # TODO: change to sql database format
        with open('data_base.json', 'r') as f:
            data = json.load(f)
        for item in data:
            if ''.join(item['name'].lower().split()) == ''.join(
                    self.item_id.lower().split()):  # checks name to item id  database
                self.item_name = item['name']
                self.item_id = str(item['id'])  # return the id
                return self.item_id
        return False

    def id_to_name(self):
        # TODO: change to sql database format
        with open(DATABASE, 'r') as f:
            data = json.load(f)
        for item in data:
            if str(item[
                       'id']) == self.item_id:  # checks name to item id database and normalizes caps to make user friendly
                self.item_name = str(item['name'])  # return the id
                return self.item_name

    def grab_data(
            self):  # to handle calling wiki and grabbing raw data to convert to usable format, returns a dictionary of item data if it's valid item, returns 0 if not
        # TODO: change to sql database format
        data = API.api_data.json()  # uses response's json handling to return dictoinary of item data
        if self.item_id.isnumeric():  # if passed item name instead of id convert it
            self.id_to_name()
        else:
            self.name_to_id()
        if self.item_id in data['data']:
            formatted_data = {
                'name': self.item_name,
                'item_id': self.item_id,
                'high': data['data'][self.item_id]['high'],
                'low': data['data'][self.item_id]['low'],
                'icon': 'https://secure.runescape.com/m=itemdb_oldschool/1663239679537_obj_big.gif?id=' + str(
                    self.item_id)
            }
            self.high = formatted_data['high']
            self.low = formatted_data['low']
            self.icon = formatted_data['icon']
            return formatted_data
        return False


def main():
    while True:
        requested_item_data = ItemData(input('What item would you like price info for?\n'))
        requested_item_data.grab_data()
        time_retrieved = datetime.datetime.now()
        print(requested_item_data.item_name + 's profit margin is ' + str(
            requested_item_data.high - requested_item_data.low) + ' at ' + time_retrieved.strftime("%H:%M:%S"))
    return 0


if __name__ == '__main__':
    import sys

    sys.exit(main())
