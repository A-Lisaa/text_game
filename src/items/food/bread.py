from ..interfaces.IConsumable import IConsumable


class Bread(IConsumable):
    def consume(self, character):
        character.hunger.restore(10)