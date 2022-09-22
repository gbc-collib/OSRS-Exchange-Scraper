"""This file contains an user-made list of quick and profittable money making
methods that are dependant on market prices i.e. combining diamond bolt tips
with adamant or dragon bolts when to do so is profittable"""
import requests
import json
import get_price
import cProfile

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

def update_flip_list():
    with open(flip_list, 'r') as f:
        potential_flips = json.load(f)
    profits = Node('flips')
    counter = 0
    for key in potential_flips:
        item = get_price.ItemData(key).grab_data()
        profits.child.append(Node(item))
        for ingredient in potential_flips[key]:
            #(profits.child[counter].child).append(Node({ingredient: get_price.ItemData(ingredient).grab_data()['low']}));
            item = get_price.ItemData(ingredient).grab_data()
            profits.child[counter].child.append(item)
            #profits.child[counter].child.append(Node(get_price.ItemData(ingredient).grab_data()['low']))
        counter += 1
    return profits

def calculate_profit():
    flips = update_flip_list()
    item_profit = {}
    for item in flips.child:
        profit = int(item.data['high'])
        print(item.data['name'] + str(item.data['high']))
        for ingredient in item.child:
            print(ingredient['name'] + str(ingredient['low']))
            profit -= int(ingredient['low'])
#         - (int(item.child[0]['low']) + int(item.child[1]['low']))
        item_profit[item.data['name']] = profit
    print(item_profit)
    return item_profit

def main(args):
    calculate_profit()


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
