import requests
import json

def main(args):
    item_url = 'http://prices.runescape.wiki/api/v1/osrs/mapping'
    headers = {
      'User-Agent': 'gbc_collib\'s amateur price tracker',
      'From': 'collinstasiak@gmail.com'
    }
    raw_data = requests.get(item_url, headers=headers, stream=True)
    data = raw_data.json()
    with open('data_base.json', 'w') as f:
        json.dump(data, f)
if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
