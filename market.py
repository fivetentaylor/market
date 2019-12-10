import dataclasses as dcs
from binsearch import insert
from operator import le, ge
from typing import Dict, List
from enum import Enum, auto


class Color(Enum):
    RED = auto()
    GREEN = auto()
    BLUE = auto()


@dcs.dataclass
class Order:
    account: str
    kind: str
    product: str
    rate: float
    amount: float


@dcs.dataclass
class Fill:
    aggressor: str
    account: str
    kind: str
    product: str
    rate: float
    amount: float


@dcs.dataclass
class Market:
    asks: List[Order]
    bids: List[Order]
    fills: List[Fill]


@dcs.dataclass
class Account:
    name: str
    balances: Dict[str, float]


def fill_order(market: dict, maker: bool, order: Order):
    market[order.product]['fills'].append(Fill(
        aggressor = 'maker' if maker else 'taker',
        **dcs.asdict(order)
    ))


def place_order(market: dict, order: Order):
    if order.product not in market:
        market[order.product] = {
            'ask': [],
            'bid': [],
            'fills': [],
        }

    product = market[order.product]

    book_type = 'bid' if order.kind == 'ask' else 'ask'
    comp = le if order.kind == 'ask' else ge
    while (
        len(product[book_type]) > 0 and
        comp(order.rate, product[book_type][0].rate)
    ):
        if order.amount >= product[book_type][0].amount:
            o = product[book_type].pop(0)
            fill_order(market, True, o)
            fill_order(market, False, dcs.replace(order, amount=o.amount, rate=o.rate))
            order.amount -= o.amount
        else:
            o = product[book_type][0]
            fill_order(market, True, dcs.replace(o, amount=order.amount))
            fill_order(market, False, dcs.replace(order, rate=o.rate))
            o.amount -= order.amount

    if order.amount > 0:
        insert(
            order,
            product[order.kind],
            key=lambda m: m.rate,
            reverse=order.kind == 'bid',
        )
