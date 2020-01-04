import pudb
import market
from copy import deepcopy

def test_create_asks():
    o = {
        'account': '123',
        'side': 'ask',
        'market': 'A-B',
        'rate': 100.0,
        'size': 5,
    }

    m = {}

    market.add_funds(m, '123', 'A', 10000)

    rates = [99.0, 100.0, 101.0]
    for rate in rates:
        o = deepcopy(o)
        o['rate'] = rate
        market.create_order(m, **o)

    asks = m['markets']['A-B']['asks']
    assert(asks[0][0] == 99.0)
    assert(asks[1][0] == 100.0)
    assert(asks[2][0] == 101.0)

    assert(m['accounts']['123']['balances']['A'] == 10000 - sum(rates) * 5)

def test_create_bids():
    o = {
        'account': '123',
        'side': 'bid',
        'market': 'A-B',
        'rate': 100.0,
        'size': 5,
    }

    m = {}

    market.add_funds(m, '123', 'B', 10000)

    rates = [99.0, 100.0, 101.0]
    for rate in rates:
        o = deepcopy(o)
        o['rate'] = rate
        market.create_order(m, **o)

    bids = m['markets']['A-B']['bids']
    assert(bids[2][0] == 99.0)
    assert(bids[1][0] == 100.0)
    assert(bids[0][0] == 101.0)

    assert(m['accounts']['123']['balances']['B'] == 10000 - sum(rates) * 5)

def test_fill_orders():
    bid = {
        'account': '123',
        'side': 'bid',
        'market': 'A-B',
        'rate': 100.0,
        'size': 5,
    }

    ask = {
        'account': '456',
        'side': 'ask',
        'market': 'A-B',
        'rate': 100.0,
        'size': 5,
    }

    m = {}
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
    market.add_funds(m, 'acct0', 'prod0', 101.0)
    market.add_funds(m, 'acct1', 'prod0', 105.0)

    assert(m['accounts']['acct0']['balances']['prod0'] == 101.0)
    assert(m['accounts']['acct1']['balances']['prod0'] == 105.0)

def test_cancel_order():
    o = {
        'account': '123',
        'side': 'ask',
        'market': 'A-B',
        'rate': 100.0,
        'size': 5,
    }

    m = {}

    market.add_funds(m, '123', 'A', 10000)
    order, _ = market.create_order(m, **o)

    # pudb.set_trace()
    market.cancel_order(m, order['id'])
    x = 0
