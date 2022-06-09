from src.items import Items

items = Items.from_json_file("data/items/items.json")

bread_sword1 = items["bread_sword"]
print(bread_sword1)
bread_sword1.do_damage(25)
print(bread_sword1)

bread_sword2 = items["bread_sword"]
print(bread_sword2)
bread_sword2.do_damage(10)
print(bread_sword2)

print(bread_sword1)

print(bread_sword1.__class__.__name__)
