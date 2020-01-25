# Market

A very simple market simulator

It places the whole marketplace in a dictionary

## Exchange

```python
exchange = {
  'products': {
    'A-B': {
      'asks': [[rate, amount]...],
      'bids': [[rate, amount]...],
    }, ...
  },
  'accounts': {
    'some-account': {
      'balances': {
        'A': 120.0,
        'B': 5.0,
        ...
      },
      'orders': {
        'id123': { ... }
      },
    }, ...
  }
}
```

## Add order

The quote_increment field specifies the min order price as well as the price increment

if you're trying to sell(ask), you need enough USD
if you're trying to buy(bid), you need enough BTC

```python
{
    "id": "BTC-USD",
    "base_currency": "BTC",
    "quote_currency": "USD",
    "base_min_size": "0.001",
    "base_max_size": "10000.00",
    "quote_increment": "0.01"
}
```


## TODO

- Convert and properly handle internal precision for each product
- I think the math is probably wrong between products, probably easy fix
- Create order and cancel order APIs
- Emit events equivalent to the [level2 channel](https://docs.pro.coinbase.com/#the-level2-channel) and the [user channel](https://docs.pro.coinbase.com/#the-user-channel)
- Create client to place/cancel orders and maintain orderbook + account balance given event streams

## Modelling Thoughts

- Our target is obviously just making more money, so our objective function should reward that
- We probably need a meta algorithm that removes losing models from the pool... and potentially creates copies of winning models with refreshed holdings...
- **Data**
  - Holdings is just our distribution of money across each product, and is a fixed width vector for a given model
  - Orders is a variable width vector representing our current orders in each product... should we use some recurrent net to understand them at each decision point?
  - Orderbook represents the current supply and demand of the product and is a large variable size tensor shaped (2, 2, N)
  - Recent events? Orders and fills over some recent period or fixed number like the last 10k events that lead to the current order book?
- Should we run inference at each market event? Or at some fixed time interval?
- The model can take a maker, taker or hybrid approach
- It can predict
  - [buy, rate, amount, product]
  - [prod1_amount, prod2_amount, ..., prodN_amount] and then aggresively try to rebalance once it's out of some threshold far enough
- Marketplaces have higher fees for taker orders vs maker orders, that should be baked into training

