"""
Player class - Represents the player character
"""
from game.items import Weapon

class Player:
    """Player character class"""
    
    def __init__(self):
        self.health = 10
        self.max_health = 10
        self.gold = 0
        self.inventory = []
        self.equipped_weapon = None
        self.is_vampire = False
    
    def take_damage(self, amount):
        """Take damage from an attack"""
        self.health -= amount
        if self.health < 0:
            self.health = 0
    
    def heal(self, amount):
        """Heal the player"""
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health
    
    def add_item(self, item):
        """Add an item to inventory"""
        self.inventory.append(item)
        print(f"Added {item.name} to inventory")
    
    def add_gold(self, amount):
        """Add gold to player"""
        self.gold += amount
        print(f"Added {amount} gold")
    
    def equip_weapon(self, weapon):
        """Equip a weapon"""
        self.equipped_weapon = weapon
        print(f"Equipped {weapon.name}")
    
    def get_attack_damage(self):
        """Get the player's attack damage"""
        if self.equipped_weapon:
            return self.equipped_weapon.damage
        return 1  # Unarmed damage
    
    def show_inventory(self):
        """Display the player's inventory"""
        print("\n===== INVENTORY =====")
        if not self.inventory:
            print("Your inventory is empty.")
        else:
            for i, item in enumerate(self.inventory):
                print(f"{i+1}. {item.name} - {item.description}")
        
        print(f"\nGold: {self.gold}")
        print(f"Equipped weapon: {self.equipped_weapon.name if self.equipped_weapon else 'None'}")
        print("====================\n")
    
    def resurrect_as_vampire(self):
        """Resurrect player as a vampire"""
        self.is_vampire = True
        self.health = self.max_health
        # Keep inventory and gold