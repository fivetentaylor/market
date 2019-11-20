import dataclasses as dcs
from binsearch import insert

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

def place_order(order: Order):
    if order.market not in markets:
        markets[order.market] = {
            'ask': [],
            'bid': [],
        }

    market = markets[order.market]

    insert(
        order,
        market[order.kind],
        key=lambda m: m.rate,
        reverse=order.kind == 'bid',
    )


    # if no orders can be filled
    if (
        len(market['ask']) == 0 or
        len(market['bid']) == 0 or
        market['ask'][0].rate > market['bid'][0].rate)
    ):
        return






