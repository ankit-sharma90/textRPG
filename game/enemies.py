"""
Enemies module - Defines all enemies in the game
"""

class Enemy:
    """Base class for all enemies"""
    
    def __init__(self, name, health, attack):
        self.name = name
        self.health = health
        self.attack = attack


# Define basic enemies
GOBLIN = Enemy("Goblin", 3, 1)
OLD_MAN = Enemy("Old Man", 5, 1)