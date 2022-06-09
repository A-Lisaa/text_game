from src.items import Items
from src.storage import Storage

items = Items.from_json_file("data/items/items.json")

bread_sword = items["bread_sword"]

storage = Storage()
storage.add_item(bread_sword)
print(storage)
