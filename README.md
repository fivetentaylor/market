# Market

A very simple market simulator

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
markets = {
  'name': {
      'asks': [],
      'bids': [],
  }, ...
}
```
