"""
Unit tests for Item classes
"""
import unittest
from game.items import Item, Weapon, STICK


class TestItem(unittest.TestCase):
    
    def test_item_initialization(self):
        item = Item("Test Item", "A test item")
        self.assertEqual(item.name, "Test Item")
        self.assertEqual(item.description, "A test item")


class TestWeapon(unittest.TestCase):
    
    def test_weapon_initialization(self):
        weapon = Weapon("Sword", "A sharp blade", 5)
        self.assertEqual(weapon.name, "Sword")
        self.assertEqual(weapon.description, "A sharp blade")
        self.assertEqual(weapon.damage, 5)
    
    def test_stick_weapon(self):
        self.assertEqual(STICK.name, "Stick")
        self.assertEqual(STICK.description, "A simple wooden stick")
        self.assertEqual(STICK.damage, 1)

    def test_weapon_inheritance(self):
        """Test that Weapon inherits from Item"""
        weapon = Weapon("Sword", "A sharp blade", 5)
        self.assertIsInstance(weapon, Item)

    def test_item_empty_name_and_description(self):
        """Test creating item with empty name and description"""
        item = Item("", "")
        self.assertEqual(item.name, "")
        self.assertEqual(item.description, "")

    def test_item_none_name_and_description(self):
        """Test creating item with None name and description"""
        item = Item(None, None)
        self.assertIsNone(item.name)
        self.assertIsNone(item.description)

    def test_weapon_zero_damage(self):
        """Test creating weapon with zero damage"""
        weapon = Weapon("Zero Sword", "No damage", 0)
        self.assertEqual(weapon.damage, 0)

    def test_weapon_negative_damage(self):
        """Test creating weapon with negative damage"""
        weapon = Weapon("Broken Sword", "Negative damage", -10)
        self.assertLess(weapon.damage, 0)

    def test_weapon_float_damage(self):
        """Test creating weapon with float damage"""
        weapon = Weapon("Magic Staff", "Mystical damage", 3.5)
        self.assertEqual(weapon.damage, 3.5)

    def test_item_equality_comparison(self):
        """Test item equality comparison"""
        item1 = Item("Sword", "A sharp blade")
        item2 = Item("Sword", "A sharp blade")
        item3 = Item("Axe", "A heavy axe")
        
        # Same name and description should be equal
        self.assertEqual(item1.name, item2.name)
        self.assertEqual(item1.description, item2.description)
        
        # Different items should not be equal
        self.assertNotEqual(item1.name, item3.name)

    def test_stick_predefined_item(self):
        """Test the predefined STICK item"""
        self.assertEqual(STICK.name, "Stick")
        self.assertEqual(STICK.description, "A simple wooden stick")
        self.assertEqual(STICK.damage, 1)
        self.assertIsInstance(STICK, Weapon)
        self.assertIsInstance(STICK, Item)


if __name__ == '__main__':
    unittest.main()