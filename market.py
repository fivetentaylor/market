import dataclasses as dcs
from binsearch import insert

fills = []
markets = {}


@dcs.dataclass
class Order:
    account: str
    kind: str
    market: str
    rate: float
    amount: float


@dcs.dataclass
class Fill:
    account: str
    aggressor: str

def fill_order(maker: bool, order: Order):
    pass

def place_order(order: Order):
    if order.market not in markets:
        markets[order.market] = {
            'ask': [],
            'bid': [],
        }

    market = markets[order.market]

    while (
        order.kind == 'ask' and
        len(market['bid']) > 0 and
        order.rate < market['bid'][0].rate
    ):
        if order.amount > market['bid'][0].amount:
            o = market['bid'].pop(0)
            fill_order(True, o)
            fill_order(False, dcs.replace(order, amount=o.amount, rate=o.rate))
            order.amount -= o.amount
        else:
            o = market['bid'][0]
            fill_order(True, dcs.replace(o, amount=order.amount))
            fill_order(False, dcs.replace(order, rate=o.rate))
            o.amount -= order.amount

    while (
        order.kind == 'bid' and
        len(market['ask']) > 0 and
        order.rate > market['ask'][0].rate
    ):
        break

    if order.amount > 0:
        insert(
            order,
            market[order.kind],
            key=lambda m: m.rate,
            reverse=order.kind == 'bid',
        )
