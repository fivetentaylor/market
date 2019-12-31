# Market

A very simple market simulator

It places the whole marketplace in a dictionary

## Exchange

```python
exchange = {
  'markets': {
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

## TODO

- Convert and properly handle internal precision for each product
- Create order and cancel order APIs
- Emit events equivalent to the [level2 channel](https://docs.pro.coinbase.com/#the-level2-channel) and the [user channel](https://docs.pro.coinbase.com/#the-user-channel)
- Create client to place/cancel orders and maintain orderbook + account balance given event streams
