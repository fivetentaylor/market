import dataclasses as dcs
from binsearch import insert
from operator import lt, gt

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
    fills.append(order)


def place_order(order: Order):
    if order.market not in markets:
        markets[order.market] = {
            'ask': [],
            'bid': [],
        }

    market = markets[order.market]

    book_type = 'bid' if order.kind == 'ask' else 'ask'
    comp = lt if order.kind == 'ask' else gt
    while (
        len(market[book_type]) > 0 and
        comp(order.rate, market[book_type][0].rate)
    ):
        if order.amount >= market[book_type][0].amount:
            o = market[book_type].pop(0)
            fill_order(True, o)
            fill_order(False, dcs.replace(order, amount=o.amount, rate=o.rate))
            order.amount -= o.amount
        else:
            o = market[book_type][0]
            fill_order(True, dcs.replace(o, amount=order.amount))
            fill_order(False, dcs.replace(order, rate=o.rate))
            o.amount -= order.amount

    if order.amount > 0:
        insert(
            order,
            market[order.kind],
            key=lambda m: m.rate,
            reverse=order.kind == 'bid',
        )
