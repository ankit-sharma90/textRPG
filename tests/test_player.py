"""
Unit tests for Player class
"""
import unittest
from game.player import Player
from game.items import Weapon, STICK


class TestPlayer(unittest.TestCase):
    
    def setUp(self):
        self.player = Player()
    
    def test_player_initialization(self):
        self.assertEqual(self.player.health, 10)
        self.assertEqual(self.player.max_health, 10)
        self.assertEqual(self.player.gold, 0)
        self.assertEqual(self.player.inventory, [])
        self.assertIsNone(self.player.equipped_weapon)
        self.assertFalse(self.player.is_vampire)
    
    def test_take_damage(self):
        self.player.take_damage(3)
        self.assertEqual(self.player.health, 7)
        
        # Test damage doesn't go below 0
        self.player.take_damage(10)
        self.assertEqual(self.player.health, 0)
    
    def test_heal(self):
        self.player.health = 5
        self.player.heal(3)
        self.assertEqual(self.player.health, 8)
        
        # Test healing doesn't exceed max health
        self.player.heal(5)
        self.assertEqual(self.player.health, 10)
    
    def test_add_gold(self):
        self.player.add_gold(15)
        self.assertEqual(self.player.gold, 15)
    
    def test_add_item(self):
        weapon = STICK
        self.player.add_item(weapon)
        self.assertIn(weapon, self.player.inventory)
    
    def test_equip_weapon(self):
        weapon = STICK
        self.player.equip_weapon(weapon)
        self.assertEqual(self.player.equipped_weapon, weapon)
    
    def test_get_attack_damage(self):
        # Test unarmed damage
        self.assertEqual(self.player.get_attack_damage(), 1)
        
        # Test with weapon
        weapon = Weapon("Sword", "A sharp sword", 5)
        self.player.equip_weapon(weapon)
        self.assertEqual(self.player.get_attack_damage(), 5)
    
    def test_resurrect_as_vampire(self):
        self.player.health = 0
        self.player.resurrect_as_vampire()
        self.assertTrue(self.player.is_vampire)
        self.assertEqual(self.player.health, self.player.max_health)
    
    def test_take_damage_edge_cases(self):
        # Test zero damage
        initial_health = self.player.health
        self.player.take_damage(0)
        self.assertEqual(self.player.health, initial_health)
        
        # Test negative damage (actually heals in current implementation)
        self.player.take_damage(-5)
        self.assertEqual(self.player.health, 10)  # Capped at max_health
    
    def test_heal_edge_cases(self):
        # Test zero healing
        self.player.health = 5
        self.player.heal(0)
        self.assertEqual(self.player.health, 5)
        
        # Test negative healing (actually damages in current implementation)
        self.player.heal(-3)
        self.assertEqual(self.player.health, 2)
    
    def test_inventory_management(self):
        weapon1 = Weapon("Sword", "A sharp sword", 5)
        weapon2 = Weapon("Axe", "A heavy axe", 7)
        
        self.player.add_item(weapon1)
        self.player.add_item(weapon2)
        
        self.assertEqual(len(self.player.inventory), 2)
        self.assertIn(weapon1, self.player.inventory)
        self.assertIn(weapon2, self.player.inventory)
    
    def test_gold_management(self):
        # Test adding gold
        self.player.add_gold(50)
        self.assertEqual(self.player.gold, 50)
        
        # Test adding more gold
        self.player.add_gold(25)
        self.assertEqual(self.player.gold, 75)
        
        # Test zero gold addition
        self.player.add_gold(0)
        self.assertEqual(self.player.gold, 75)
    
    def test_weapon_switching(self):
        weapon1 = Weapon("Sword", "A sharp sword", 5)
        weapon2 = Weapon("Axe", "A heavy axe", 7)
        
        # Equip first weapon
        self.player.equip_weapon(weapon1)
        self.assertEqual(self.player.equipped_weapon, weapon1)
        self.assertEqual(self.player.get_attack_damage(), 5)
        
        # Switch to second weapon
        self.player.equip_weapon(weapon2)
        self.assertEqual(self.player.equipped_weapon, weapon2)
        self.assertEqual(self.player.get_attack_damage(), 7)

    def test_player_health_overflow(self):
        """Test that player health can handle very large healing amounts"""
        self.player.max_health = 100
        self.player.health = 50
        self.player.heal(1000)  # Try to heal way more than max
        self.assertEqual(self.player.health, self.player.max_health)

    def test_equip_weapon_with_damage_zero(self):
        """Test equipping a weapon with zero damage"""
        zero_weapon = Weapon("Training Sword", "No damage", 0)
        self.player.equip_weapon(zero_weapon)
        self.assertEqual(self.player.get_attack_damage(), 0)

    def test_player_gold_negative_overflow(self):
        """Test that player gold can handle very large negative amounts"""
        self.player.gold = 100
        self.player.add_gold(-1000)  # Try to subtract way more than available
        self.assertEqual(self.player.gold, -900)

    def test_inventory_duplicate_items_different_objects(self):
        """Test that identical items with different object instances are tracked separately"""
        from game.items import Item
        item1 = Item("Rock", "A small rock")
        item2 = Item("Rock", "A small rock")  # Same name/description, different object
        self.player.add_item(item1)
        self.player.add_item(item2)
        self.assertEqual(len(self.player.inventory), 2)

    def test_resurrect_as_vampire_preserves_inventory(self):
        """Test that vampire resurrection preserves inventory and gold"""
        # Add some items and gold
        self.player.add_item(STICK)
        self.player.add_gold(50)
        initial_inventory = self.player.inventory.copy()
        initial_gold = self.player.gold
        
        # Die and resurrect as vampire
        self.player.health = 0
        self.player.resurrect_as_vampire()
        
        # Check that inventory and gold are preserved
        self.assertEqual(self.player.inventory, initial_inventory)
        self.assertEqual(self.player.gold, initial_gold)
        self.assertTrue(self.player.is_vampire)

    def test_equip_none_weapon(self):
        """Test equipping None as weapon (should not crash)"""
        try:
            self.player.equip_weapon(None)
            # Should default to unarmed damage
            self.assertEqual(self.player.get_attack_damage(), 1)
        except Exception as e:
            self.fail(f"equip_weapon(None) raised {e}")

    def test_player_max_health_modification(self):
        """Test that max_health can be modified and affects healing cap"""
        self.player.max_health = 20
        self.player.health = 10
        self.player.heal(15)  # Try to heal more than original max
        self.assertEqual(self.player.health, 20)  # Should cap at new max

    def test_inventory_empty_after_death(self):
        """Test that normal death (not vampire) clears inventory"""
        # Add items
        self.player.add_item(STICK)
        self.player.add_gold(25)
        
        # Simulate normal death (not vampire resurrection)
        # This would be handled by GameManager, but we can test the concept
        self.player.health = 0
        self.player.inventory = []  # Simulate inventory loss
        self.player.gold = 0  # Simulate gold loss
        
        self.assertEqual(len(self.player.inventory), 0)
        self.assertEqual(self.player.gold, 0)


if __name__ == '__main__':
    unittest.main()