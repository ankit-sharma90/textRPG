"""
Unit tests for GameManager class
"""
import unittest
from unittest.mock import patch, MagicMock
from game.game_manager import GameManager
from game.player import Player
from game.world import World, CellType
from game.time_system import TimeSystem


class TestGameManager(unittest.TestCase):
    
    def setUp(self):
        self.game_manager = GameManager()
    
    def test_initialization(self):
        self.assertIsInstance(self.game_manager.player, Player)
        self.assertIsInstance(self.game_manager.world, World)
        self.assertIsInstance(self.game_manager.time_system, TimeSystem)
        self.assertEqual(self.game_manager.action_count, 0)
        self.assertFalse(self.game_manager.game_over)
    
    def test_action_taken(self):
        initial_count = self.game_manager.action_count
        self.game_manager.action_taken()
        self.assertEqual(self.game_manager.action_count, initial_count + 1)
    
    def test_time_advancement_every_5_actions(self):
        initial_time = self.game_manager.time_system.time
        
        # Take 4 actions - time should not advance
        for _ in range(4):
            self.game_manager.action_taken()
        self.assertEqual(self.game_manager.time_system.time, initial_time)
        
        # Take 5th action - time should advance
        self.game_manager.action_taken()
        expected_time = (initial_time + 1) % 2
        self.assertEqual(self.game_manager.time_system.time, expected_time)
    
    def test_vampire_damage_during_day(self):
        # Make player a vampire
        self.game_manager.player.resurrect_as_vampire()
        initial_health = self.game_manager.player.health
        
        # Ensure it's daytime
        self.game_manager.time_system.time = 0
        
        # Take 5 actions to trigger time advancement
        for _ in range(5):
            self.game_manager.action_taken()
        
        # Player should take damage if still daytime after advancement
        if self.game_manager.time_system.is_daytime():
            expected_damage = int(self.game_manager.player.max_health * 0.05)
            expected_health = initial_health - expected_damage
            self.assertEqual(self.game_manager.player.health, expected_health)
    
    @patch('game.game_manager.random.randint')
    def test_handle_location_interaction_treasure(self, mock_randint):
        mock_randint.return_value = 10
        
        # Mock world to return treasure
        self.game_manager.world.get_current_cell = MagicMock(return_value=CellType.TREASURE)
        self.game_manager.world.get_current_map = MagicMock()
        mock_map = MagicMock()
        mock_map.grid = [[CellType.TREASURE]]
        self.game_manager.world.get_current_map.return_value = mock_map
        self.game_manager.world.player_x = 0
        self.game_manager.world.player_y = 0
        
        initial_gold = self.game_manager.player.gold
        result = self.game_manager.handle_location_interaction(1)  # Search treasure
        
        self.assertEqual(self.game_manager.player.gold, initial_gold + 10)
        self.assertIn("10 gold", result)
    
    @patch('game.game_manager.random.randint')
    def test_handle_location_interaction_npc_quest(self, mock_randint):
        mock_randint.return_value = 5
        
        self.game_manager.world.get_current_cell = MagicMock(return_value=CellType.NPC)
        
        initial_gold = self.game_manager.player.gold
        result = self.game_manager.handle_location_interaction(3)  # Request quest
        
        self.assertEqual(self.game_manager.player.gold, initial_gold + 5)
        self.assertIn("5 gold", result)


if __name__ == '__main__':
    unittest.main()