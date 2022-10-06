import json

import get_price

ITEM_DATABASE = 'data_base.json'


def grab_alc_price():
    with open(ITEM_DATABASE) as f:  # opens prebuilt item database and closes as soon as it's imported
        items_list = json.load(f)
        high_alc_values = {}
        for item in items_list:
            if 'highalch' not in item or 'limit' not in item:   # handles edge case of non-alch-able items or non-tradable
                continue
            high_alc_values[item['name']] = item['highalch'], item['limit']
    return high_alc_values


def alc_profit(items: dict = grab_alc_price(), margin: int = 10,
               limit: int = 1000):  # takes dict keyed by item name with value of high alc, defaults to all items
    api_object = get_price.ItemData('561')
    nature_rune_cost = api_object.grab_data()['low']
    print(nature_rune_cost)
    profittable_alc = {}
    for name, price in items.items():
        api_object.item_id = name
        if price[1] < limit or price[0] < nature_rune_cost:
            continue
        ge_price = api_object.grab_data()
        ge_price = ge_price['high']
        if (price[0] - nature_rune_cost) < ge_price:
            continue
        potential_alc = (price[0] - nature_rune_cost) - ge_price
        if potential_alc > margin:
            profittable_alc[name] = potential_alc
    return profittable_alc


def sort_alc_list(dictionary: dict):
    return dict(sorted(dictionary.items(), key=lambda item: item[1], reverse=True))


def main():
    alc_dict = sort_alc_list(alc_profit())
    print("{:<10} {:<10}".format('Name', 'profit'))
    for key, value in alc_dict.items():
        print("{:<10} {:<10}".format(key, value))

    return 0
