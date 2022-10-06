"""This file contains an user-made list of quick and profittable money making
methods that are dependant on market prices i.e. combining diamond bolt tips
with adamant or dragon bolts when to do so is profittable"""
from __future__ import annotations

import json


import get_price
from typing import Optional
from dataclasses import dataclass
flip_list = 'get_rich.json'  # a json file containing a graph of items with final product having vertices of ingridients



class Node:
    def __init__(self, key):
        self.data = key
        self.child = []
def update_flip_list():
    with open(flip_list, 'r') as f:
        potential_flips = json.load(f)
    profits = Node('flips')
    degree = 0
    for key in potential_flips:
        item = get_price.ItemData(key).grab_data()
        profits.child.append(Node(item))
        for ingredient in potential_flips[key]:
            item = get_price.ItemData(ingredient).grab_data()
            profits.child[degree].child.append(item)
        degree += 1
    return profits

def calculate_profit():
    flips = update_flip_list()
    item_profit = {}
    for item in flips.child:
        profit = int(item.data['high'])
        # print(item.data['name'] + str(item.data['high']))
        for ingredient in item.child:
            # print(ingredient['name'] + str(ingredient['low']))
            profit -= int(ingredient['low'])
        #         - (int(item.child[0]['low']) + int(item.child[1]['low']))
        item_profit[item.data['name']] = profit
    return dict(sorted(item_profit.items(), key=lambda item: item[1], reverse=True))


def main(args):
    print(calculate_profit())

if __name__ == '__main__':
    import sys

    sys.exit(main(sys.argv))
