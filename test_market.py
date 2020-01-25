import pudb
import market
from copy import deepcopy

def test_create_asks():
    o = {
        'account': '123',
        'side': 'ask',
        'product': 'A-B',
        'price': 100.0,
        'size': 5,
    }

    m = {}

    market.add_account(m, '123')
    market.add_funds(m, '123', 'A', 10000)

    prices = [99.0, 100.0, 101.0]
    for price in prices:
        o = deepcopy(o)
        o['price'] = price
        market.create_order(m, **o)

    asks = m['products']['A-B']['asks']
    assert(asks[0][0] == 99.0)
    assert(asks[1][0] == 100.0)
    assert(asks[2][0] == 101.0)

    assert(m['accounts']['123']['balances']['A'] == 10000 - sum(prices) * 5)

def test_create_bids():
    o = {
        'account': '123',
        'side': 'bid',
        'product': 'A-B',
        'price': 100.0,
        'size': 5,
    }

    m = {}

    market.add_account(m, '123')
    market.add_funds(m, '123', 'B', 10000)

    prices = [99.0, 100.0, 101.0]
    for price in prices:
        o = deepcopy(o)
        o['price'] = price
        market.create_order(m, **o)

    bids = m['products']['A-B']['bids']
    assert(bids[2][0] == 99.0)
    assert(bids[1][0] == 100.0)
    assert(bids[0][0] == 101.0)

    assert(m['accounts']['123']['balances']['B'] == 10000 - sum(prices) * 5)

def test_fill_orders():
    bid = {
        'account': '123',
        'side': 'bid',
        'product': 'A-B',
        'price': 100.0,
        'size': 5,
    }

    ask = {
        'account': '456',
        'side': 'ask',
        'product': 'A-B',
        'price': 100.0,
        'size': 5,
    }

    m = {}
    market.add_account(m, '123')
    market.add_account(m, '456')
    market.add_currency(m, 'A', '0.001')
    market.add_currency(m, 'B', '0.001')

    market.add_product(m, 'A-B', '0.001', '100', '0.001')
    pudb.set_trace()

    market.add_funds(m, '123', 'B', 10000)
    market.add_funds(m, '456', 'A', 10000)

    assert(m['accounts']['123']['balances']['B'] == 10000)
    assert(m['accounts']['456']['balances']['A'] == 10000)

    market.create_order(m, **bid)

    assert(m['accounts']['123']['balances']['B'] == 10000 - 500.0)

    market.create_order(m, **ask)

    assert(m['accounts']['123']['balances']['A'] == 500)
    assert(m['accounts']['456']['balances']['B'] == 500)

def test_add_funds():
    m = {}
    market.add_account(m, 'acct0')
    market.add_account(m, 'acct1')
    market.add_currency(m, 'cur0', '0.001')

    market.add_funds(m, 'acct0', 'cur0', 101.0)
    market.add_funds(m, 'acct1', 'cur0', 105.0)

    assert(m['accounts']['acct0']['balances']['cur0'] == 101.0)
    assert(m['accounts']['acct1']['balances']['cur0'] == 105.0)

def test_cancel_order():
    o = {
        'account': '123',
        'side': 'ask',
        'product': 'A-B',
        'price': 100.0,
        'size': 5,
    }

    m = {}

    market.add_account(m, '123')
    market.add_funds(m, '123', 'A', 10000)
    order, _ = market.create_order(m, **o)

    # pudb.set_trace()
    market.cancel_order(m, order['id'])
    x = 0
