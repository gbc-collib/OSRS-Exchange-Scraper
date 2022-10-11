"""This file contains a user-made list of quick and profitable money making
methods that are dependent on market prices i.e. combining diamond bolt tips
with adamant or dragon bolts when to do so is profitable"""
from __future__ import annotations

import json

import get_price
from prices.models import QuickFlips, Ingredient

flip_list = 'get_rich.json'  # a json file containing a graph of items with final product having vertices of ingredients


class Node:
    def __init__(self, key):
        self.data = key
        self.child = []


def update_flip_list() -> Node:
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


def node_to_profit_dict() -> dict:
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
    return dict(sorted(item_profit.items(), key=lambda i: i[1], reverse=True))


def build_profits_db(profit_node):
    ing_list = []
    QuickFlips.objects.all().delete()  # These two lines clear the database because this function will only be called
    # when it should be rebuilt
    Ingredient.objects.all().delete()
    for parent_item in profit_node.child:
        profit = int(parent_item.data['high'])
        ing_list.clear()
        # print(item.data['name'] + str(item.data['high']))
        finished = QuickFlips.objects.create(item_name=parent_item.data['name'], profit=profit,
                                             item_price=parent_item.data['high'])
        for ingredient in parent_item.child:
            ing_list.append(ingredient)
            # print(ingredient['name'] + str(ingredient['low']))
            profit -= int(ingredient['low'])
            # - (int(item.child[0]['low']) + int(item.child[1]['low']))
            Ingredient.objects.create(item_name=ingredient['name'],
                                      item_price=ingredient['low'],
                                      parent_item=finished, profit=0)
        Ingredient.objects.filter(parent_item=finished).update(profit=profit)


def main(args):
    print(build_profits_db(update_flip_list()))
    # print(node_to_profit_dict))


if __name__ == '__main__':
    import sys

    sys.exit(main(sys.argv))
