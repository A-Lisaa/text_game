from room import RoomCity, RoomForest
from src.event import Event
from src.item import Item

locations_pool = {
    RoomCity: {
        "generation": (5, 1),
        "loot": {
            (Item("Bread"), 2, 1): (2, 1),
            (Item("Water"), 2, 3): (5, 3),
            (Item("Knife"), 1, 0.25): (1, 0.25)
        },
        "events": {
        }
    },

    RoomForest: {
        "generation": (-1, 2),
        "loot": {
            (Item("Bread"), 1, 1): (1, 1),
            (Item("Water"), 3, 3): (2, 2),
            (Item("Stick"), 5, 5): (5, 5)
        },
        "events": {
        }
    }
}
