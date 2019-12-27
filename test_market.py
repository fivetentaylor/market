import pudb
import market
from copy import deepcopy

def test_place_asks():
    o = {
        'account': '123',
        'side': 'ask',
        'market': 'A-B',
        'rate': 100.0,
        'amount': 5,
    }

    m = {}

    market.add_funds(m, '123', 'A', 10000)

    rates = [99.0, 100.0, 101.0]
    for rate in rates:
        o = deepcopy(o)
        o['rate'] = rate
        list(market.place_order(m, **o))

    asks = m['markets']['A-B']['asks']
    assert(asks[0]['rate'] == 99.0)
    assert(asks[1]['rate'] == 100.0)
    assert(asks[2]['rate'] == 101.0)

def test_place_bids():
    o = {
        'account': '123',
        'side': 'bid',
        'market': 'A-B',
        'rate': 100.0,
        'amount': 5,
    }

    m = {}

    market.add_funds(m, '123', 'B', 10000)

    rates = [99.0, 100.0, 101.0]
    for rate in rates:
        o = deepcopy(o)
        o['rate'] = rate
        list(market.place_order(m, **o))

    bids = m['markets']['A-B']['bids']
    assert(bids[2]['rate'] == 99.0)
    assert(bids[1]['rate'] == 100.0)
    assert(bids[0]['rate'] == 101.0)

def test_fill_orders():
    bid = {
        'account': '123',
        'side': 'bid',
        'market': 'A-B',
        'rate': 100.0,
        'amount': 5,
    }

    ask = {
        'account': '456',
        'side': 'ask',
        'market': 'A-B',
        'rate': 100.0,
        'amount': 5,
    }

    m = {}
    market.add_funds(m, '123', 'B', 10000)
    market.add_funds(m, '456', 'A', 10000)

    list(market.place_order(m, **bid))
    list(market.place_order(m, **ask))
    x = 1

def test_add_funds():
    m = {}
    market.add_funds(m, 'acct0', 'prod0', 101.0)
    market.add_funds(m, 'acct1', 'prod0', 105.0)
    #pudb.set_trace()
    x = 0
