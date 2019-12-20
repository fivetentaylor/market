from copy import deepcopy
import dataclasses as dcs
from binsearch import insert
from operator import le, ge
from typing import Dict, List, Union, Literal
from enum import Enum, auto


def place_order(
    market: dict,
    account: str,
    product: str,
    kind: Union[Literal['ask'], Literal['bid']],
    rate: float,
    amount: float
):
    if product not in market:
        market[product] = {
            'asks': [],
            'bids': [],
            'fills': [],
        }

    order = {
        'account': account,
        'product': product,
        'kind': kind,
        'rate': rate,
        'amount': amount,
    }

    product = market[product]

    book = 'bids' if kind == 'ask' else 'asks'
    comp = le if kind == 'ask' else ge
    while (
        len(product[book]) > 0 and
        order['amount'] > 0 and
        comp(rate, product[book][0]['rate'])
    ):
        make = deepcopy(product[book][0])
        make['maker'] = True
        take = deepcopy(order)
        take['maker'] = False

        if take['amount'] < make['amount']:
            # make is partially filled
            make['amount'] = take['amount']
            product[book][0]['amount'] -= take['amount']
            order['amount'] = 0
        else:
            # make is completely filled
            take['amount'] = make['amount']
            product[book].pop(0)
            order['amount'] -= make['amount']

        take['rate'] = make['rate']
        yield [make, take]

    if order['amount'] > 0:
        book = '%ss' % kind
        insert(
            order,
            product[book],
            key=lambda m: m['rate'],
            reverse=book == 'bids',
        )
