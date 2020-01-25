from uuid import uuid4
from copy import deepcopy
from binsearch import insert, bisect
from operator import le, ge, itemgetter
from typing import Dict, List, Union, Literal, Tuple


def add_account(market: dict, account_id: str):
    accounts = market.setdefault('accounts', {})
    accounts.setdefault(account_id, {
        'balances': {},
        'orders': [],
    })

    return market


def add_funds(market: dict, account_id: str, currency: str, size: float):
    if size <= 0:
        raise ValueError('size must be greater than 0')
    balances = market['accounts'][account_id]['balances']
    balances[currency] = balances.get(currency, 0) + size

    return market


def add_currency(
    market: dict,
    cur_id: str,
    min_size: str
):
    currencies = market.setdefault('currencies', {})
    currencies[cur_id] = {
        'id': cur_id,
        'min_size': min_size,
    }

    return market


def add_product(
    market: dict,
    prod_id: str,
    base_min_size: str,
    base_max_size: str,
    quote_increment: str
):
    base_currency, quote_currency = prod_id.split('-')

    if base_currency not in market['currencies']:
        raise KeyError('Currency %s not in market' % base_currency)
    if quote_currency not in market['currencies']:
        raise KeyError('Currency %s not in market' % quote_currency)

    products = market.setdefault('products', {})
    products.setdefault(prod_id, {
        'id': prod_id,
        'base_currency': base_currency,
        'quote_currency': quote_currency,
        'base_min_size': base_min_size,
        'base_max_size': base_max_size,
        'quote_increment': quote_increment,
    })

    books = market.setdefault('books', {})
    books.setdefault(prod_id, {
        'asks': [],
        'bids': [],
    })

    return market


def _verify_holdings(
    market: dict,
    order: dict
):
    account, product, side, price, size = itemgetter(
        'account', 'product', 'side', 'price', 'size'
    )(order)

    base, quote = product.split('-')

    ask = side == 'ask'
    currency = quote if ask else base
    required = size if ask else size * price
    balance = market['accounts'][account]['balances'].setdefault(currency, 0)

    if required > balance:
        raise ValueError(
            ('Account %s has ' +
            'insuficient funds %f in %s ' +
            'to cover %f') %
            (account, balance, currency, required)
        )

    market['accounts'][account]['balances'][currency] -= required
    return market


def _fill_orders(
    market: dict,
    order: dict
):
    mrkt = market['products'][order['product']]
    ask = order['side'] == 'ask'
    book = mrkt['bids' if ask else 'asks']
    comp = le if ask else ge

    while (
        len(book) > 0 and
        order['size'] > 0 and
        comp(order['price'], book[0][0])
    ):
        make = deepcopy(market['orders'][book[0][2]])
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

        take['price'] = make['price']
        yield [make, take]


def _update_holdings(
    market: dict,
    fill: dict
):
    oid, account, product, side, price, size, maker = itemgetter(
        'id', 'account', 'product', 'side', 'price', 'size', 'maker'
    )(fill)

    if maker:
        orders = market['orders']
        orders[oid]['size'] -= size

        if orders[oid]['size'] == 0:
            del orders[oid]

    base, quote = product.split('-')
    ask = side == 'ask'
    currency = base if ask else quote
    amount = size * price if ask else size

    market['accounts'][account]['balances'][currency] += amount

    return deepcopy(fill)


def _insert_order(
    market: dict,
    order: dict
):
    if order['size'] <= 0:
        return None

    market.setdefault('orders', {})[order['id']] = order

    book = '%ss' % order['side']
    mrkt = market['products'][order['product']]

    insert(
        list(itemgetter('price', 'size', 'id')(order)),
        mrkt[book],
        reverse=book == 'bids',
    )

    return deepcopy(order)


def cancel_order(
    market: dict,
    order_id: str
):
    # remove order from market
    order = market['orders'].pop(order_id)

    aid, product, side, price, size = itemgetter(
        'account', 'product', 'side', 'price', 'size'
    )(order)

    # remove order from book
    book = market['products'][product]['%ss' % side]
    ix = bisect(price, book, key=lambda o: o[0], reverse=side == 'bid')
    for i in range(ix, len(book)):
        if book[i][0] > price:
            break

        # this is okay since we break right after deleting
        if book[i][2] == order_id:
            del book[i]
            break

    # return funds to account holdings
    account = market['accounts'][aid]

    left, right = product.split('-')
    currency = left if side == 'ask' else right

    account['balances'][currency] += price * size


def create_order(
    market: dict,
    account: str,
    product: str,
    side: Union[Literal['ask'], Literal['bid']],
    price: float,
    size: float
):
    order = {
        'id': str(uuid4()),
        'account': account,
        'product': product,
        'side': side,
        'price': float(price),
        'size': float(size),
    }
    _verify_holdings(market, order)

    fills = []
    for make, take in _fill_orders(market, order):
        fills.append(_update_holdings(market, make))
        fills.append(_update_holdings(market, take))

    return _insert_order(market, order), fills
