# Market

A very simple market simulator

It places the whole marketplace in a dictionary

## Order

```python
order = {
  'account': 'owner of the account',
  'order_type': 'ask | bid',
  'market': string: name of market,
  'rate': float: price you'd like to buy/sell,
  'amount': float: how many units at that price
}
```

## Markets

```python
market = {
    'BTC-USD': {
        'ask': [],
        'bid': [],
        'fills': [],
    },
    'BTC-ETH': {
        'ask': [],
        'bid': [],
        'fills': [],
    },
}
```
