from binsearch import bisect
from binsearch import insert

def test_bisect():
    assert(bisect(10, []) == 0)
    assert(bisect(10, [5]) == 1)
    assert(bisect(10, [15]) == 0)
    assert(bisect(10, [5, 15]) == 1)

    key = lambda x: x[0]
    assert(bisect(10, [], key=key) == 0)
    assert(bisect(10, [[5]], key=key) == 1)
    assert(bisect(10, [[15]], key=key) == 0)
    assert(bisect(10, [[5], [15]], key=key) == 1)

def test_bisect_reverse():
    assert(bisect(10, [], reverse=True) == 0)
    assert(bisect(10, [5], reverse=True) == 0)
    assert(bisect(10, [15], reverse=True) == 1)
    assert(bisect(10, [15, 5], reverse=True) == 1)

def test_bisect_right():
    assert(bisect(10, [], left=False) == 0)
    assert(bisect(10, [5], left=False) == 1)
    assert(bisect(10, [15], left=False) == 0)
    assert(bisect(10, [5,10], left=False) == 2)

def test_insert():
    x = []
    insert(5, x)
    assert(x == [5])
    insert(6, x)
    assert(x == [5, 6])
    insert(100, x)
    assert(x == [5, 6, 100])
    insert(3, x)
    assert(x == [3, 5, 6, 100])

def test_insert_reverse():
    x = []
    insert(5, x, reverse=True)
    assert(x == [5])
    insert(6, x, reverse=True)
    assert(x == [6, 5])
    insert(100, x, reverse=True)
    assert(x == [100, 6, 5])
    insert(3, x, reverse=True)
    assert(x == [100, 6, 5, 3])

def test_insert_right():
    x = []
    key = lambda x: x[0]
    insert((5, 0), x, key=key, left=False)
    assert(x == [(5, 0)])
    insert((5, 1), x, key=key, left=True)
    assert(x == [(5, 1), (5, 0)])
    insert((5, 2), x, key=key, left=False)
    assert(x == [(5, 1), (5, 0), (5, 2)])
