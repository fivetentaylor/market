from operator import gt, lt, ge, le

def bisect(val, array, key=lambda x: x, left=True, reverse=False):
    '''return the index of the first item >= key(val)'''
    if len(array) == 0: return 0

    comp = [[ge, le], [gt, lt]][left][reverse]
    l, r = 0, len(array)
    while True:
        ix = (l + r) // 2
        tmp = (l, r)[comp(val, key(array[ix]))]
        if r - l == 1: return tmp
        l, r = sorted((ix, tmp))

def insert(val, array, key=lambda x: x, left=True, reverse=False):
    i = bisect(key(val), array, key=key, left=left, reverse=reverse)
    array.insert(i, val)
    return array
