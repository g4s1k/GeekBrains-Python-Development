d = {'a': 'b', 'c': 'd'}
d.pop(tuple(d.keys())[0])
print(d)