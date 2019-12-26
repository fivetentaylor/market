from copy import deepcopy
from binsearch import insert
from operator import le, ge
from typing import Dict, List, Union, Literal


def market_defaults(market: dict, account: str, product: str):
    accounts = market.setdefault('accounts', {})
    accounts.setdefault(account, {
        'balances': {},
        'orders': {},
    })

    products = market.setdefault('products', {})
    prod = products.setdefault(product, {
        'asks': [],
        'bids': [],
    })

    return market


def add_funds(market: dict, account: str, product: str, amount: float):
    if amount <= 0:
        raise ValueError('Amount must be greater than 0')
    market_defaults(market, account, product)
    balances = market['accounts'][account]['balances']
    balances[product] = balances.get(product, 0) + amount


def place_order(
    market: dict,
    account: str,
    product: str,
    side: Union[Literal['ask'], Literal['bid']],
    rate: float,
    amount: float
):
    market_defaults(market, account, product)
    prod = market['products'][product]

    balance = market['accounts'][account]['balances'].get(product, 0)
    if amount:
        pass

    order = {
        'account': account,
        'product': product,
        'side': side,
        'rate': rate,
        'amount': amount,
    }

    book = 'bids' if side == 'ask' else 'asks'
    comp = le if side == 'ask' else ge
    while (
        len(prod[book]) > 0 and
        order['amount'] > 0 and
        comp(rate, prod[book][0]['rate'])
    ):
        make = deepcopy(prod[book][0])
        make['maker'] = True
        take = deepcopy(order)
        take['maker'] = False

        if take['amount'] < make['amount']:
            # make is partially filled
            make['amount'] = take['amount']
            prod[book][0]['amount'] -= take['amount']
            order['amount'] = 0
        else:
            # make is completely filled
            take['amount'] = make['amount']
            prod[book].pop(0)
            order['amount'] -= make['amount']

        take['rate'] = make['rate']
        yield [make, take]

    if order['amount'] > 0:
        book = '%ss' % side
        insert(
            order,
            prod[book],
            key=lambda m: m['rate'],
            reverse=book == 'bids',
        )
