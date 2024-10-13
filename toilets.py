# toilets.py
from ursina import *
from abc import ABC, abstractmethod

# Abstract Base Class for Toilets
class Toilet(ABC):
    def __init__(self, position):
        self.position = position

    @abstractmethod
    def flush(self):
        pass

# Different Toilet Types
class StandardToilet(Toilet):
    def __init__(self, position):
        super().__init__(position)
        self.entity = Entity(
            model='cube',
            scale=(1, 1, 1),
            position=position,
            color=color.white,
            collider='box'
        )

    def flush(self):
        print("Standard toilet flush sound!")

class FancyToilet(Toilet):
    def __init__(self, position):
        super().__init__(position)
        self.entity = Entity(
            model='cube',
            scale=(1.2, 1.2, 1.2),
            position=position,
            color=color.gold,
            collider='box'
        )

    def flush(self):
        print("Fancy toilet flush with music!")