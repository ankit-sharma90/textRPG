"""
Items module - Defines all items in the game
"""

class Item:
    """Base class for all items"""
    
    def __init__(self, name, description):
        self.name = name
        self.description = description


class Weapon(Item):
    """Weapon item that can be equipped"""
    
    def __init__(self, name, description, damage):
        super().__init__(name, description)
        self.damage = damage


# Define some basic weapons
STICK = Weapon("Stick", "A simple wooden stick", 1)