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

def place_order(order: Order):
    if order.market not in markets:
        markets[order.market] = {
            'ask': [],
            'bid': [],
        }

    insert(
        order,
        markets[order.market][order.kind],
        key=lambda m: m.rate,
        reverse=order.kind == 'bid',
    )
