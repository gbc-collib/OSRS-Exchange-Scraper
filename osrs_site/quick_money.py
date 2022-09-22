"""This file contains an user-made list of quick and profittable money making
methods that are dependant on market prices i.e. combining diamond bolt tips
with adamant or dragon bolts when to do so is profittable"""
import requests
import json
import get_price

flip_list = 'get_rich.json' #a json file containing a graph of items with final product having vertices of ingridients

class Node:
    def __init__(self, data):
        self.data = data
        self.child = []
def print_tree(node, level=0):
    if node != None:
        print_tree(node.left, level + 1)
        print(' ' * 4 * level + '-> ' + str(node.data))
        print_tree(node.right, level + 1)

def calculate_profit():
    with open(flip_list, 'r') as f:
        potential_flips = json.load(f)
    profits = Node('flips')
    counter = 0
    for key in potential_flips:
        profits.child.append(Node({key: get_price.ItemData(key).grab_data()['high']}))
        for ingredient in potential_flips[key]:
            (profits.child[counter].child).append(Node({ingredient: get_price.ItemData(ingredient).grab_data()['low']}));
        counter += 1

def main(args):
    calculate_profit()


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
"""
    formatted_data = {
    'name': self.item_name,
    'item_id': self.item_id,
    'high': data['data'][self.item_id]['high'],
    'low': data['data'][self.item_id]['low'],
    'icon': 'https://secure.runescape.com/m=itemdb_oldschool/1663239679537_obj_big.gif?id=' + str(self.item_id)
    }
"""
