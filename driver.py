import json
import market
from random import choice, random
import itertools as it

exchange = {}
accounts = ['user%d' % i for i in range(5)]
products = ['A', 'B', 'C']
markets = ['%s-%s' % p for p in it.permutations(products, 2)]
side = ['ask', 'bid']

for account, product in it.product(accounts, products):
    market.add_funds(exchange, account, product, 10000)

fill_count = 0
for i in range(1000):
    params = {
        'account': choice(accounts),
        'market': choice(markets),
        'side': choice(side),
        'rate': random() * 10,
        'size': random() * 10,
    }
    order, fills = market.create_order(exchange, **params)
    for fill in fills:
        fill_count += 1
        if fill['size'] <= 0:
            raise Exception('invalid size!!!')
        print(json.dumps(fill))

print('%d orders filled' % fill_count)
# print(json.dumps(exchange))
