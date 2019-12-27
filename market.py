import pudb

from copy import deepcopy
from binsearch import insert
from operator import le, ge
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


def add_funds(exchange: dict, account: str, product: str, amount: float):
    if amount <= 0:
        raise ValueError('Amount must be greater than 0')
    _account_defaults(exchange, account)
    balances = exchange['accounts'][account]['balances']
    balances[product] = balances.get(product, 0) + amount


def _verify_holdings(
    exchange: dict,
    account: str,
    market: str,
    side: Union[Literal['ask'], Literal['bid']],
    rate: float,
    amount: float
):
    pass


def _fill_orders(
    exchange: dict,
    account: str,
    market: str,
    side: Union[Literal['ask'], Literal['bid']],
    rate: float,
    amount: float
):
    pass


def _update_holdings(
    exchange: dict,
    account: str,
    market: str,
    side: Union[Literal['ask'], Literal['bid']],
    rate: float,
    amount: float
):
    pass


def place_order(
    exchange: dict,
    account: str,
    market: str,
    side: Union[Literal['ask'], Literal['bid']],
    rate: float,
    amount: float
):
    # set defaults, verify holdings, fill any orders, update holdings, insert remaining order

    _account_defaults(exchange, account)
    _market_defaults(exchange, market)
    mrkt = exchange['markets'][market]

    left, right = market.split('-')
    product = left if side == 'ask' else right
    balance = exchange['accounts'][account]['balances'].get(product, 0)
    if amount * rate > balance:
        raise ValueError('Insuficient funds to cover amount * rate = %f' % (amount * rate))
    else:
        # update holdings
        pass

    order = {
        'account': account,
        'market': market,
        'side': side,
        'rate': rate,
        'amount': amount,
    }

    book = 'bids' if side == 'ask' else 'asks'
    comp = le if side == 'ask' else ge
    while (
        len(mrkt[book]) > 0 and
        order['amount'] > 0 and
        comp(rate, mrkt[book][0]['rate'])
    ):
        make = deepcopy(mrkt[book][0])
        make['maker'] = True
        take = deepcopy(order)
        take['maker'] = False

        if take['amount'] < make['amount']:
            # make is partially filled
            make['amount'] = take['amount']
            mrkt[book][0]['amount'] -= take['amount']
            order['amount'] = 0
        else:
            # make is completely filled
            take['amount'] = make['amount']
            mrkt[book].pop(0)
            order['amount'] -= make['amount']

        take['rate'] = make['rate']
        yield [make, take]

    if order['amount'] > 0:
        book = '%ss' % side
        insert(
            order,
            mrkt[book],
            key=lambda m: m['rate'],
            reverse=book == 'bids',
        )
