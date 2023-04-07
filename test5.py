from itertools import zip_longest

print(list(zip_longest(range(5), range(10), range(3), fillvalue=0)))
