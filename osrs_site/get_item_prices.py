# itemdb_oldschool
# https://secure.runescape.com/m=itemdb_oldschool/api/catalogue/detail.json?item=379
import datetime
import json  # converts string data into usable dictionary
import logging
import sqlite3

import requests  # for handling url requests


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


def insert_timeseries_data(connection, data):
    columns = list(data.keys())  # Pull columns from json and remove useless ones
    joined_columns = "item_" + ", item_".join(columns)
    placeholders = ", ".join("coalesce(:{}, 0)".format(col) for col in columns)
    # not concerned about sanitizing sql because this query will never come from user input
    connection.execute(
        "CREATE TABLE IF NOT EXISTS prices_timeseries (item_time_retrieved, item_id, item_icon, item_name, item_high, item_low);")
    query = 'INSERT INTO prices_timeseries (%s) VALUES (%s)' % (joined_columns, placeholders)
    connection.execute(query, data)
    connection.commit()
    return connection


class ItemData:
    def __init__(self, item_id):  # item id accepts string of item name or iteger of item ID
        self.item_id = item_id
        self.item_name = None
        self.high = None
        self.low = None
        self.icon = None
        self.connection = sqlite3.connect("item_info.db")
        API()

    def name_to_id(self):
        self.item_name = self.item_id
        # query_result = self.connection.execute("SELECT item_id, item_name FROM items_info WHERE item_name=?", self.item_id)
        query_result = self.connection.execute("SELECT item_id FROM items_info WHERE item_name=:item_name",
                                               {"item_name": self.item_name})
        res = query_result.fetchone()
        if res is not None:
            self.item_id = res[0]
            return self.item_id
        return False

    def id_to_name(self):
        query_result = self.connection.execute("SELECT item_name FROM items_info WHERE item_id=:item_id;",
                                               {"item_id": int(self.item_id)})
        if query_result is not None:
            self.item_name = query_result.fetchone()[0]
            return self.item_name
        return False

    def grab_data(
            self):  # to handle calling wiki and grabbing raw data to convert to usable format, returns a dictionary of item data if it's valid item, returns 0 if not
        data = API.api_data.json()  # uses response's json handling to return dictoinary of item data
        if self.item_id.isnumeric():  # if passed item name instead of id convert it
            self.id_to_name()
        else:
            self.name_to_id()
        if self.item_id in data['data']:
            formatted_data = {
                'name': self.item_name,
                'id': self.item_id,
                'high': data['data'][self.item_id]['high'],
                'low': data['data'][self.item_id]['low'],
                'icon': 'https://secure.runescape.com/m=itemdb_oldschool/1663239679537_obj_big.gif?id=' + str(
                    self.item_id),
                'time_retrieved': API.time.strftime("%b:%D:%H:%M:%S")
            }
            insert_timeseries_data(self.connection, formatted_data)
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

if __name__ == '__main__':
    import sys

    sys.exit(main())
