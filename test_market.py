import pudb
import market
from copy import deepcopy

def test_place_asks():
    o = {
        'account': '123',
        'side': 'ask',
        'product': 'test',
        'rate': 100.0,
        'amount': 5,
    }

    m = {}
    rates = [99.0, 100.0, 101.0]
    for rate in rates:
        o = deepcopy(o)
        o['rate'] = rate
        list(market.place_order(m, **o))

    asks = m['products']['test']['asks']
    assert(asks[0]['rate'] == 99.0)
    assert(asks[1]['rate'] == 100.0)
    assert(asks[2]['rate'] == 101.0)

def test_place_bids():
    o = {
        'account': '123',
        'side': 'bid',
        'product': 'test',
        'rate': 100.0,
        'amount': 5,
    }

    m = {}
    rates = [99.0, 100.0, 101.0]
    for rate in rates:
        o = deepcopy(o)
        o['rate'] = rate
        list(market.place_order(m, **o))

    bids = m['products']['test']['bids']
    assert(bids[2]['rate'] == 99.0)
    assert(bids[1]['rate'] == 100.0)
    assert(bids[0]['rate'] == 101.0)

def test_fill_orders():
    bid = {
        'account': '123',
        'side': 'bid',
        'product': 'test',
        'rate': 100.0,
        'amount': 5,
    }

    ask = {
        'account': '456',
        'side': 'ask',
        'product': 'test',
        'rate': 100.0,
        'amount': 5,
    }

    m = {}
    list(market.place_order(m, **bid))
    list(market.place_order(m, **ask))
    x = 1
