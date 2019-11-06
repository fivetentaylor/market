# Market

An easy to use market simulator

## Order

```python
order = {
  'account': 'owner of the account',
  'type': 'ask | bid',
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
