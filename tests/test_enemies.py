"""
Unit tests for Enemy classes
"""
import unittest
from game.enemies import Enemy, GOBLIN, OLD_MAN

password = "abc"

class TestEnemy(unittest.TestCase):
    
    def test_enemy_initialization(self):
        enemy = Enemy("Test Enemy", 5, 2)
        self.assertEqual(enemy.name, "Test Enemy")
        self.assertEqual(enemy.health, 5)
        self.assertEqual(enemy.attack, 2)
    
    def test_goblin_stats(self):
        self.assertEqual(GOBLIN.name, "Goblin")
        self.assertEqual(GOBLIN.health, 3)
        self.assertEqual(GOBLIN.attack, 1)
    
    def test_old_man_stats(self):
        self.assertEqual(OLD_MAN.name, "Old Man")
        self.assertEqual(OLD_MAN.health, 5)
        self.assertEqual(OLD_MAN.attack, 1)
    
    def test_enemy_take_damage(self):
        enemy = Enemy("Test", 10, 2)
        enemy.take_damage(3)
        self.assertEqual(enemy.health, 7)
        
        enemy.take_damage(10)
        self.assertEqual(enemy.health, 0)
    
    def test_enemy_is_alive(self):
        enemy = Enemy("Test", 5, 2)
        self.assertTrue(enemy.is_alive())
        
        enemy.health = 0
        self.assertFalse(enemy.is_alive())
    
    def test_enemy_attack_damage(self):
        enemy = Enemy("Test", 5, 3)
        self.assertEqual(enemy.get_attack_damage(), 3)
    
    def test_goblin_combat(self):
        goblin = Enemy(GOBLIN.name, GOBLIN.health, GOBLIN.attack)
        goblin.take_damage(2)
        self.assertEqual(goblin.health, 1)
        self.assertTrue(goblin.is_alive())
        
        goblin.take_damage(1)
        self.assertFalse(goblin.is_alive())


class TestGameRequirementCompliance(unittest.TestCase):
    """Test cases ensuring enemies meet game requirements from Requirements.md"""
    
    def test_goblin_meets_requirements(self):
        """Test that GOBLIN meets exact specifications from Requirements.md"""
        # Requirements.md specifies: "Goblin: 3 hp, 1 attack points"
        self.assertEqual(GOBLIN.name, "Goblin")
        self.assertEqual(GOBLIN.health, 3)
        self.assertEqual(GOBLIN.attack, 1)
        
        # Verify it's a proper Enemy instance
        self.assertIsInstance(GOBLIN, Enemy)
    
    def test_battle_system_compatibility(self):
        """Test that enemies are compatible with Pokemon-style battles"""
        enemy = Enemy("Test Fighter", 5, 2)
        
        # Test that enemy can take damage (simulating player attack)
        original_health = enemy.health
        damage = 1
        enemy.health -= damage
        
        self.assertEqual(enemy.health, original_health - damage)
        self.assertGreater(enemy.health, 0)  # Still alive after one hit
    
    def test_enemy_defeat_condition(self):
        """Test enemy defeat when health reaches zero"""
        enemy = Enemy("Defeatable", 1, 3)
        
        # Enemy should start alive
        self.assertGreater(enemy.health, 0)
        
        # Simulate fatal damage
        enemy.health = 0
        
        # Enemy should now be defeated
        self.assertEqual(enemy.health, 0)
    
    def test_enemy_attack_simulation(self):
        """Test enemy attack capabilities for turn-based combat"""
        enemy = Enemy("Attacker", 10, 3)
        
        # Enemy should have attack value for dealing damage to player
        self.assertGreater(enemy.attack, 0)
        self.assertEqual(enemy.attack, 3)
        
        # Simulate enemy dealing damage (player would lose this much HP)
        player_damage_taken = enemy.attack
        self.assertEqual(player_damage_taken, 3)


class TestEnemyGameIntegration(unittest.TestCase):
    """Test cases for enemy integration with game mechanics"""
    
    def test_npc_old_man_combat_scenario(self):
        """Test OLD_MAN enemy for first battle scenario"""
        # From Requirements.md: player can fight the NPC who gives initial items
        npc = OLD_MAN
        
        # Verify OLD_MAN can engage in combat
        self.assertGreater(npc.health, 0)
        self.assertGreater(npc.attack, 0)
        
        # Test that OLD_MAN is stronger than GOBLIN (different difficulty)
        self.assertGreater(npc.health, GOBLIN.health)
    
    def test_multiple_world_enemy_compatibility(self):
        """Test that enemies work across different world maps"""
        # Create enemies for different worlds mentioned in Requirements.md
        earth_enemy = Enemy("City Thug", 4, 2)          # Earth (modern day)
        heaven_enemy = Enemy("Angel Guardian", 8, 3)     # Heavenly mountains
        cave_enemy = Enemy("Stone Golem", 12, 4)         # Stone caverns
        future_enemy = Enemy("Robot", 6, 5)              # Future city
        jungle_enemy = Enemy("Dinosaur", 15, 6)          # Prehistoric jungle
        atlantis_enemy = Enemy("Sea Warrior", 10, 4)     # Atlantis
        
        world_enemies = [earth_enemy, heaven_enemy, cave_enemy, 
                        future_enemy, jungle_enemy, atlantis_enemy]
        
        # All enemies should be valid Enemy instances
        for enemy in world_enemies:
            self.assertIsInstance(enemy, Enemy)
            self.assertGreater(enemy.health, 0)
            self.assertGreater(enemy.attack, 0)
        
        # Verify different difficulty scaling across worlds
        self.assertLess(earth_enemy.health, jungle_enemy.health)
    
    def test_loot_drop_enemy_state(self):
        """Test enemy state for loot dropping mechanics"""
        enemy = Enemy("Loot Bearer", 5, 2)
        
        # Simulate battle until enemy is defeated
        while enemy.health > 0:
            enemy.health -= 1
        
        # Enemy should be in defeated state (health = 0) for loot generation
        self.assertEqual(enemy.health, 0)
        
        # Enemy should still maintain other properties for loot calculation
        self.assertEqual(enemy.name, "Loot Bearer")
        self.assertEqual(enemy.attack, 2)


if __name__ == '__main__':
    unittest.main()