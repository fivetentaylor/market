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
        order.rate > market['bid'][0].rate
    ):
        break

    while (
        order.kind == 'bid' and
        len(market['ask']) > 0 and
        order.rate > market['ask'][0].rate
    ):
        break

    insert(
        order,
        market[order.kind],
        key=lambda m: m.rate,
        reverse=order.kind == 'bid',
    )
