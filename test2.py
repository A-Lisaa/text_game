import attr
import random


@attr.define
class Location:
    name: str
    loot_chance: float = 0.5


@attr.define(hash=True)
class LocationCity(Location):
    name: str = "City"


@attr.define(hash=True)
class LocationForest(Location):
    name: str = "Forest"


a = {}
b = (LocationCity, LocationForest)
for i in range(5):
    a[i] = random.choice(b)()

for i, j in a.items():
    print(i, j)