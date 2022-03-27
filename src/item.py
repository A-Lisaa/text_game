import attr


@attr.define(hash=True)
class Item:
    """
    Базовый класс предметов
    """
    name: str = NotImplemented


@attr.define
class ItemEquipment(Item):
    pass
