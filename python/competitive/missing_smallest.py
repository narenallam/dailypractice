def missing_smallest(l: 'list[int]')->'int/None':
    if l:
        _min = min(l)
        n = len(l)
        for i, val in enumerate(l):
            pos = val -_min
            while 0 <=  pos < n and l[pos] != i:
                l[pos], l[i] = l[i], l[pos]
                pos = l[pos]

        for i, val in enumerate(l):
            pos = val -_min
            if  pos != i:
                return i + _min
        return None

    return None

l = [11, 13, 12, 10]
m = missing_smallest(l)
print(f'missing smallest number is {m} in {l}')