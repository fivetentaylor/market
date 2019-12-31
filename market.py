import pudb

from copy import deepcopy
from binsearch import insert
from operator import le, ge, itemgetter
from typing import Dict, List, Union, Literal, Tuple


def _account_defaults(exchange: dict, account: str):
    accounts = exchange.setdefault('accounts', {})
    accounts.setdefault(account, {
        'balances': {},
        'orders': {},
    })

    return exchange


def _market_defaults(exchange: dict, market: str):
    markets = exchange.setdefault('markets', {})
    markets.setdefault(market, {
        'asks': [],
        'bids': [],
    })

    return exchange


def add_funds(exchange: dict, account: str, product: str, size: float):
    if size <= 0:
        raise ValueError('size must be greater than 0')
    _account_defaults(exchange, account)
    balances = exchange['accounts'][account]['balances']
    balances[product] = balances.get(product, 0) + size


def _verify_holdings(
    exchange: dict,
    order: dict
):
    account, market, side, rate, size = itemgetter(
        'account', 'market', 'side', 'rate', 'size'
    )(order)

    left, right = market.split('-')
    product = left if side == 'ask' else right
    balance = exchange['accounts'][account]['balances'].setdefault(product, 0)
    if size * rate > balance:
        raise ValueError(
            ('Account %s has ' +
            'insuficient funds %f in %s ' +
            'to cover size * rate = %f') %
            (account, balance, product, size * rate)
        )
    else:
        exchange['accounts'][account]['balances'][product] -= rate * size


def _fill_orders(
    exchange: dict,
    account: str,
    market: str,
    side: Union[Literal['ask'], Literal['bid']],
    rate: float,
    size: float
):
    pass


def _update_holdings(
    exchange: dict,
    account: str,
    market: str,
    side: Union[Literal['ask'], Literal['bid']],
    rate: float,
    size: float
):
    pass


def place_order(
    exchange: dict,
    account: str,
    market: str,
    side: Union[Literal['ask'], Literal['bid']],
    rate: float,
    size: float
):
    # set defaults, verify holdings, fill any orders, update holdings, insert remaining order

    _account_defaults(exchange, account)
    _market_defaults(exchange, market)

    order = {
        'account': account,
        'market': market,
        'side': side,
        'rate': rate,
        'size': size,
    }
    _verify_holdings(exchange, order)

    mrkt = exchange['markets'][market]
    book = 'bids' if side == 'ask' else 'asks'
    comp = le if side == 'ask' else ge
    while (
        len(mrkt[book]) > 0 and
        order['size'] > 0 and
        comp(rate, mrkt[book][0]['rate'])
    ):
        make = deepcopy(mrkt[book][0])
        make['maker'] = True
        take = deepcopy(order)
        take['maker'] = False

        if take['size'] < make['size']:
            # make is partially filled
            make['size'] = take['size']
            mrkt[book][0]['size'] -= take['size']
            order['size'] = 0
        else:
            # make is completely filled
            take['size'] = make['size']
            mrkt[book].pop(0)
            order['size'] -= make['size']

        take['rate'] = make['rate']
        yield [make, take]

    if order['size'] > 0:
        book = '%ss' % side
        insert(
            order,
            mrkt[book],
            key=lambda m: m['rate'],
            reverse=book == 'bids',
        )
