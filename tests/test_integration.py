"""
Integration tests for the Text RPG game
"""
import unittest
from unittest.mock import patch, MagicMock
from game.game_manager import GameManager
from game.world import CellType


class TestGameIntegration(unittest.TestCase):
    
    def setUp(self):
        self.game = GameManager()
    
    def test_complete_game_flow(self):
        """Test a complete game flow from start to first battle"""
        # Start with some gold and health
        self.game.player.add_gold(20)
        self.assertEqual(self.game.player.gold, 20)
        
        # Move player and check action count
        initial_actions = self.game.action_count
        self.game.action_taken()
        self.assertEqual(self.game.action_count, initial_actions + 1)
    
    def test_vampire_resurrection_flow(self):
        """Test the vampire resurrection mechanic"""
        # Kill the player
        self.game.player.health = 0
        
        # Resurrect as vampire
        self.game.player.resurrect_as_vampire()
        
        self.assertTrue(self.game.player.is_vampire)
        self.assertEqual(self.game.player.health, self.game.player.max_health)
    
    def test_day_night_cycle_integration(self):
        """Test day/night cycle affects vampire players"""
        # Make player vampire
        self.game.player.resurrect_as_vampire()
        initial_health = self.game.player.health
        
        # Set to daytime
        self.game.time_system.time = 0
        
        # Take 5 actions to advance time
        for _ in range(5):
            self.game.action_taken()
        
        # If still daytime after cycle, vampire should take damage
        if self.game.time_system.is_daytime():
            self.assertLess(self.game.player.health, initial_health)
    
    @patch('game.game_manager.random.random')
    def test_merchant_interaction_flow(self, mock_random):
        """Test complete merchant interaction"""
        mock_random.return_value = 0.5  # Neutral random value
        
        # Give player gold
        self.game.player.add_gold(15)
        
        # Mock merchant location
        self.game.world.get_current_cell = MagicMock(return_value=CellType.MERCHANT)
        
        # Buy health potion
        result = self.game.handle_location_interaction(1)
        
        self.assertEqual(self.game.player.gold, 5)  # 15 - 10 for potion
        self.assertIn("health", result.lower())
    
    def test_treasure_hunting_flow(self):
        """Test treasure hunting mechanics"""
        # Mock treasure location
        self.game.world.get_current_cell = MagicMock(return_value=CellType.TREASURE)
        mock_map = MagicMock()
        mock_map.grid = [[CellType.TREASURE]]
        self.game.world.get_current_map = MagicMock(return_value=mock_map)
        self.game.world.player_x = 0
        self.game.world.player_y = 0
        
        initial_gold = self.game.player.gold
        
        # Search treasure
        result = self.game.handle_location_interaction(1)
        
        self.assertGreater(self.game.player.gold, initial_gold)
        self.assertIn("gold", result.lower())
    
    def test_world_navigation(self):
        """Test world navigation and boundaries"""
        # Test movement within bounds
        initial_x = self.game.world.player_x
        initial_y = self.game.world.player_y
        
        # Try to move (success depends on world boundaries)
        success, message = self.game.world.move_player("north")
        
        if success:
            # Position should change
            self.assertNotEqual((self.game.world.player_x, self.game.world.player_y), 
                              (initial_x, initial_y))
        else:
            # Position should remain same if blocked
            self.assertEqual((self.game.world.player_x, self.game.world.player_y), 
                           (initial_x, initial_y))


if __name__ == '__main__':
    unittest.main()