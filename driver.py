import json
import market
from random import choice, random

marketplace = {}
accounts = ['user%d' % i for i in range(5)]
products = ['usd_prod%d' % i for i in range(3)]
side = ['ask', 'bid']

fills = 0
for i in range(10000):
    params = {
        'account': choice(accounts),
        'product': choice(products),
        'kind': choice(side),
        'rate': random() * 100,
        'amount': random() * 100,
    }
    for fill in market.place_order(marketplace, **params):
        fills += 1
        if fill[0]['amount'] <= 0:
            raise Exception('invalid amount!!!')
        print(json.dumps(fill))

print('%d orders filled' % fills)
# print(json.dumps(marketplace))
