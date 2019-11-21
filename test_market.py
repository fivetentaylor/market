import pudb
import market
import dataclasses as dcs

def test_place_asks():
    o = market.Order(
        account = '123',
        kind = 'ask',
        product = 'test',
        rate = 100.0,
        amount = 5
    )

    m = {}
    market.place_order(m, o)
    market.place_order(m, dcs.replace(o, rate=101.0))
    market.place_order(m, dcs.replace(o, rate=99.0))

    asks = m['test']['ask']
    assert(asks[0].rate == 99.0)
    assert(asks[1].rate == 100.0)
    assert(asks[2].rate == 101.0)

def test_place_bids():
    o = market.Order(
        account = '123',
        kind = 'bid',
        product = 'test',
        rate = 100.0,
        amount = 5
    )

    m = {}
    market.place_order(m, o)
    market.place_order(m, dcs.replace(o, rate=101.0))
    market.place_order(m, dcs.replace(o, rate=99.0))

    bids = m['test']['bid']
    assert(bids[2].rate == 99.0)
    assert(bids[1].rate == 100.0)
    assert(bids[0].rate == 101.0)

def test_fill_orders():
    bid = market.Order(
        account = '123',
        kind = 'bid',
        product = 'test',
        rate = 100.0,
        amount = 5
    )

    ask = market.Order(
        account = '456',
        kind = 'ask',
        product = 'test',
        rate = 100.0,
        amount = 5
    )

    m = {}
    pudb.set_trace()
    market.place_order(m, bid)
    market.place_order(m, ask)
    x = 1
