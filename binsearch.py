def bisect(val, array, key=lambda x: x, reverse=False):
    '''return the index of the first item >= key(val)'''
    if len(array) == 0:
        return 0

    if reverse:
        comp = lambda x,y: x < y
    else:
        comp = lambda x,y: x > y

    l, r = 0, len(array)

    while (r - l) > 1:
        ix = (l + r) // 2
        if comp(key(val), key(array[ix])):
            l = ix
        else:
            r = ix

    ix = (l + r) // 2
    ix += int(comp(key(val), key(array[ix])))
    return ix

def insert(val, array, key=lambda x: x, reverse=False):
    i = bisect(val, array, key, reverse)
    if i is None: return
    array.insert(i, val)
    return i
