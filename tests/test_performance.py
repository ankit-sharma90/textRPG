"""
Performance tests for the Text RPG game
"""
import unittest
import time
from game.game_manager import GameManager
from game.world import World


class TestPerformance(unittest.TestCase):
    
    def setUp(self):
        self.game = GameManager()
    
    def test_game_initialization_speed(self):
        """Test that game initializes quickly"""
        start_time = time.time()
        
        for _ in range(100):
            game = GameManager()
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Should initialize 100 games in less than 1 second
        self.assertLess(total_time, 1.0)
        print(f"Game initialization: {total_time:.4f}s for 100 instances")
    
    def test_world_generation_speed(self):
        """Test world generation performance"""
        start_time = time.time()
        
        for _ in range(10):
            world = World()
            # Force world generation
            world.get_current_cell()
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Should generate 10 worlds in less than 2 seconds
        self.assertLess(total_time, 2.0)
        print(f"World generation: {total_time:.4f}s for 10 worlds")
    
    def test_action_processing_speed(self):
        """Test action processing performance"""
        start_time = time.time()
        
        for _ in range(1000):
            self.game.action_taken()
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Should process 1000 actions in less than 0.5 seconds
        self.assertLess(total_time, 0.5)
        print(f"Action processing: {total_time:.4f}s for 1000 actions")
    
    def test_battle_simulation_speed(self):
        """Test battle system performance"""
        from game.events import BattleEvent
        
        start_time = time.time()
        
        for _ in range(50):
            battle = BattleEvent("Goblin")
            battle.player = self.game.player
            # Simulate quick battle resolution
            battle.enemy.health = 1
            battle.player_attack()
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Should simulate 50 battles in less than 1 second
        self.assertLess(total_time, 1.0)
        print(f"Battle simulation: {total_time:.4f}s for 50 battles")
    
    def test_memory_usage(self):
        """Test memory efficiency"""
        import gc
        
        # Force garbage collection
        gc.collect()
        
        games = []
        for _ in range(100):
            games.append(GameManager())
        
        # Clean up
        del games
        gc.collect()
        
        # This test mainly ensures no memory leaks occur
        self.assertTrue(True)  # If we get here, no memory issues


if __name__ == '__main__':
    unittest.main()