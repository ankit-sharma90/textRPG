"""
Unit tests for Battle System integration
"""
import unittest
from unittest.mock import patch, MagicMock
from game.events import BattleEvent
from game.player import Player
from game.enemies import Enemy, GOBLIN, OLD_MAN


class TestBattleSystem(unittest.TestCase):
    
    def setUp(self):
        self.player = Player()
        self.battle = BattleEvent("Goblin")
    
    def test_battle_initialization(self):
        self.assertEqual(self.battle.enemy_name, "Goblin")
        self.assertEqual(self.battle.enemy_health, 3)
        self.assertEqual(self.battle.enemy_attack, 1)
        self.assertFalse(self.battle.battle_over)
    
    def test_player_attack(self):
        initial_enemy_health = self.battle.enemy.health
        damage = self.player.get_attack_damage()
        
        result = self.battle.player_attack()
        
        expected_health = initial_enemy_health - damage
        self.assertEqual(self.battle.enemy.health, expected_health)
        self.assertIn("attack", result.lower())
    
    def test_player_defend(self):
        self.player.health = 5  # Set low health
        initial_health = self.player.health
        
        result = self.battle.player_defend()
        
        # Should heal some amount
        self.assertGreaterEqual(self.player.health, initial_health)
        self.assertIn("defend", result.lower())
    
    def test_enemy_defeat(self):
        # Set enemy health to 1 for easy defeat
        self.battle.enemy.health = 1
        
        result = self.battle.player_attack()
        
        self.assertTrue(self.battle.battle_over)
        self.assertIn("defeated", result.lower())
    
    def test_player_defeat(self):
        # Set player health to 1 and enemy damage high
        self.player.health = 1
        self.battle.enemy.attack_damage = 10
        
        # Enemy attacks player
        self.battle.enemy_turn()
        
        self.assertEqual(self.player.health, 0)
        self.assertTrue(self.battle.battle_over)
    
    @patch('game.events.random.randint')
    def test_flee_success(self, mock_randint):
        mock_randint.return_value = 8  # High roll for successful flee
        
        result = self.battle.player_flee()
        
        self.assertTrue(self.battle.battle_over)
        self.assertIn("escape", result.lower())
    
    @patch('game.events.random.randint')
    def test_flee_failure(self, mock_randint):
        mock_randint.return_value = 2  # Low roll for failed flee
        
        result = self.battle.player_flee()
        
        self.assertFalse(self.battle.battle_over)
        self.assertIn("failed", result.lower())


if __name__ == '__main__':
    unittest.main()