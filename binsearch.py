from operator import gt, lt

def bisect(val, array, key=lambda x: x, reverse=False):
    '''return the index of the first item >= key(val)'''
    if len(array) == 0: return 0
    comp = lt if reverse else gt
    l, r = 0, len(array)
    while True:
        ix = (l + r) // 2
        tmp = (l, r)[comp(key(val), key(array[ix]))]
        if r - l == 1: return tmp
        l, r = sorted((ix, tmp))

def insert(val, array, key=lambda x: x, reverse=False):
    i = bisect(val, array, key, reverse)
    if i is None: return
    array.insert(i, val)
    return i
