import pudb

from uuid import uuid4
from copy import deepcopy
from binsearch import insert, bisect
from operator import le, ge, itemgetter
from typing import Dict, List, Union, Literal, Tuple


def _account_defaults(exchange: dict, account: str):
    accounts = exchange.setdefault('accounts', {})
    accounts.setdefault(account, {
        'balances': {},
        'orders': [],
    })

    return exchange


def _product_defaults(exchange: dict, product: str):
    products = exchange.setdefault('products', {})
    products.setdefault(product, {
        'asks': [],
        'bids': [],
    })

    return exchange


def _add_currency(
    exchange: dict,
    cur_id: str,
    name: str,
    min_size: str
):
    pass


def _add_product(
    exchange: dict,
    prod_id: str,
    base_currency: str,
    quote_currency: str,
    base_min_size: str,
    base_max_size: str,
    quote_increment: str
):
    products = exchange.setdefault('products', {})
    products[prod_id] = {
        'id': prod_id,
        'base_currency': base_currency,
        'quote_currency': quote_currency,
        'base_min_size': base_min_size,
        'base_max_size': base_max_size,
        'quote_increment': quote_increment,
    }

    return exchange


def add_funds(exchange: dict, account: str, currency: str, size: float):
    if size <= 0:
        raise ValueError('size must be greater than 0')
    _account_defaults(exchange, account)
    balances = exchange['accounts'][account]['balances']
    balances[currency] = balances.get(currency, 0) + size


def _verify_holdings(
    exchange: dict,
    order: dict
):
    account, product, side, rate, size = itemgetter(
        'account', 'product', 'side', 'rate', 'size'
    )(order)

    left, right = product.split('-')
    currency = left if side == 'ask' else right
    balance = exchange['accounts'][account]['balances'].setdefault(currency, 0)
    if size * rate > balance:
        raise ValueError(
            ('Account %s has ' +
            'insuficient funds %f in %s ' +
            'to cover size * rate = %f') %
            (account, balance, currency, size * rate)
        )
    else:
        exchange['accounts'][account]['balances'][currency] -= rate * size


def _fill_orders(
    exchange: dict,
    order: dict
):
    mrkt = exchange['products'][order['product']]
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

            make['complete'] = False
            take['complete'] = True
        else:
            # make completely filled, take partially filled
            take['size'] = make['size']
            book.pop(0)
            order['size'] -= make['size']

            make['complete'] = True
            take['complete'] = False

        take['rate'] = make['rate']
        yield [make, take]


def _update_holdings(
    exchange: dict,
    fill: dict
):
    oid, account, product, side, rate, size, maker = itemgetter(
        'id', 'account', 'product', 'side', 'rate', 'size', 'maker'
    )(fill)

    if maker:
        orders = exchange['orders']
        orders[oid]['size'] -= size

        if orders[oid]['size'] == 0:
            del orders[oid]

    left, right = product.split('-')
    currency = left if side == 'bid' else right
    balance = exchange['accounts'][account]['balances'].setdefault(currency, 0)

    exchange['accounts'][account]['balances'][currency] += rate * size

    return deepcopy(fill)


def _insert_order(
    exchange: dict,
    order: dict
):
    if order['size'] <= 0:
        return None

    exchange.setdefault('orders', {})[order['id']] = order

    book = '%ss' % order['side']
    mrkt = exchange['products'][order['product']]

    insert(
        list(itemgetter('rate', 'size', 'id')(order)),
        mrkt[book],
        reverse=book == 'bids',
    )

    return deepcopy(order)


def cancel_order(
    exchange: dict,
    order_id: str
):
    # remove order from exchange
    order = exchange['orders'].pop(order_id)

    aid, product, side, rate, size = itemgetter(
        'account', 'product', 'side', 'rate', 'size'
    )(order)

    # remove order from book
    book = exchange['products'][product]['%ss' % side]
    ix = bisect(rate, book, key=lambda o: o[0], reverse=side == 'bid')
    for i in range(ix, len(book)):
        if book[i][0] > rate:
            break

        # this is okay since we break right after deleting
        if book[i][2] == order_id:
            del book[i]
            break

    # return funds to account holdings
    account = exchange['accounts'][aid]

    left, right = product.split('-')
    currency = left if side == 'ask' else right

    account['balances'][currency] += rate * size


def create_order(
    exchange: dict,
    account: str,
    product: str,
    side: Union[Literal['ask'], Literal['bid']],
    rate: float,
    size: float
):
    _account_defaults(exchange, account)
    _product_defaults(exchange, product)

    order = {
        'id': str(uuid4()),
        'account': account,
        'product': product,
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
