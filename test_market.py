import pudb
import market

def test_place_asks():
    o1 = market.Order(
        account = '123',
        kind = 'ask',
        market = 'test',
        rate = 100.0,
        amount = 5
    )
    pudb.set_trace()
    market.place_order(o1)

    market.place_order(market.Order(
        account = '123',
        kind = 'ask',
        market = 'test',
        rate = 101.0,
        amount = 5
    ))

    market.place_order(market.Order(
        account = '123',
        kind = 'ask',
        market = 'test',
        rate = 99.0,
        amount = 5
    ))

    m = market.markets['test']['ask']
    assert(m[0].rate == 99.0)
    assert(m[1].rate == 100.0)
    assert(m[2].rate == 101.0)

def test_place_bids():
    market.place_order(market.Order(
        account = '123',
        kind = 'bid',
        market = 'test',
        rate = 100.0,
        amount = 5
    ))

    market.place_order(market.Order(
        account = '123',
        kind = 'bid',
        market = 'test',
        rate = 101.0,
        amount = 5
    ))

    market.place_order(market.Order(
        account = '123',
        kind = 'bid',
        market = 'test',
        rate = 99.0,
        amount = 5
    ))

    m = market.markets['test']['bid']
    assert(m[2].rate == 99.0)
    assert(m[1].rate == 100.0)
    assert(m[0].rate == 101.0)
