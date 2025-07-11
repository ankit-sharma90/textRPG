import unittest
from game.player import Player
from game.game_manager import GameManager

class TestCore(unittest.TestCase):
    
    def test_player_basic(self):
        player = Player()
        self.assertEqual(player.health, 10)
        self.assertEqual(player.gold, 0)
    
    def test_game_manager_init(self):
        game = GameManager()
        self.assertIsNotNone(game.player)
        self.assertEqual(game.action_count, 0)

if __name__ == '__main__':
    unittest.main()