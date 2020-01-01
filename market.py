import pudb

from uuid import uuid4
from copy import deepcopy
from binsearch import insert
from operator import le, ge, itemgetter
from typing import Dict, List, Union, Literal, Tuple


def _account_defaults(exchange: dict, account: str):
    accounts = exchange.setdefault('accounts', {})
    accounts.setdefault(account, {
        'balances': {},
        'orders': [],
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
    order: dict
):
    mrkt = exchange['markets'][order['market']]
    book = mrkt['bids' if order['side'] == 'ask' else 'asks']
    comp = le if order['side'] == 'ask' else ge

    while (
        len(book) > 0 and
        order['size'] > 0 and
        comp(order['rate'], book[0][0])
    ):
        make = deepcopy(exchange['orders'][book[0][2]])
        make['maker'] = True
        take = deepcopy(order)
        take['maker'] = False

        if take['size'] < make['size']:
            # make partially filled, take completely filled
            make['size'] = take['size']
            book[0][1] -= take['size']
            order['size'] = 0
        else:
            # make completely filled, take partially filled
            take['size'] = make['size']
            book.pop(0)
            order['size'] -= make['size']

        take['rate'] = make['rate']
        yield [make, take]


def _update_holdings(
    exchange: dict,
    fill: dict
):
    order_id, account, market, side, rate, size, maker = itemgetter(
        'id', 'account', 'market', 'side', 'rate', 'size', 'maker'
    )(fill)

    left, right = market.split('-')
    product = left if side == 'bid' else right
    balance = exchange['accounts'][account]['balances'].setdefault(product, 0)

    exchange['accounts'][account]['balances'][product] += rate * size

    return deepcopy(fill)


def _insert_order(
    exchange: dict,
    order: dict
):
    if order['size'] <= 0:
        return None

    exchange.setdefault('orders', {})[order['id']] = order

    book = '%ss' % order['side']
    mrkt = exchange['markets'][order['market']]

    insert(
        itemgetter('rate', 'size', 'id')(order),
        mrkt[book],
        reverse=book == 'bids',
    )

    return deepcopy(order)

def cancel_order(
    exchange: dict,
    order_id: str
):
    pass

def create_order(
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
        'id': str(uuid4()),
        'account': account,
        'market': market,
        'side': side,
        'rate': rate,
        'size': size,
    }
    _verify_holdings(exchange, order)

    fills = []
    for make, take in _fill_orders(exchange, order):
        fills.append(_update_holdings(exchange, make))
        fills.append(_update_holdings(exchange, take))

    return _insert_order(exchange, order), fills
