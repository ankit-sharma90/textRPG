"""
Unit tests for Events module
"""
import unittest
from unittest.mock import patch, MagicMock
from game.events import FirstEncounter, BattleEvent
from game.game_manager import GameManager


class TestFirstEncounter(unittest.TestCase):
    
    def setUp(self):
        self.game_manager = GameManager()
        self.first_encounter = FirstEncounter(self.game_manager)
    
    @patch('builtins.input', return_value='2')
    @patch('builtins.print')
    def test_first_encounter_accept_gold(self, mock_print, mock_input):
        """Test accepting gold from first encounter"""
        initial_gold = self.game_manager.player.gold
        self.first_encounter.run()
        self.assertEqual(self.game_manager.player.gold, initial_gold + 10)
    
    @patch('builtins.input', return_value='1')
    @patch('builtins.print')
    def test_first_encounter_reject_gold(self, mock_print, mock_input):
        """Test rejecting gold from first encounter"""
        initial_gold = self.game_manager.player.gold
        self.first_encounter.run()
        self.assertEqual(self.game_manager.player.gold, initial_gold)
    
    @patch('builtins.input', return_value='3')
    @patch('builtins.print')
    def test_first_encounter_fight(self, mock_print, mock_input):
        """Test fighting the old man in first encounter"""
        initial_gold = self.game_manager.player.gold
        # Mock the battle to avoid infinite loop
        with patch('game.events.BattleEvent.run'):
            self.first_encounter.run()
        self.assertEqual(self.game_manager.player.gold, initial_gold + 10)


class TestBattleEvent(unittest.TestCase):
    
    def setUp(self):
        self.battle = BattleEvent("Goblin")
    
    def test_battle_initialization_goblin(self):
        """Test battle initialization with Goblin"""
        self.assertEqual(self.battle.enemy_name, "Goblin")
        self.assertEqual(self.battle.enemy_health, 3)
        self.assertEqual(self.battle.enemy_attack, 1)
    
    def test_battle_initialization_old_man(self):
        """Test battle initialization with Old Man"""
        battle = BattleEvent("Old Man")
        self.assertEqual(battle.enemy_name, "Old Man")
        self.assertEqual(battle.enemy_health, 5)
        self.assertEqual(battle.enemy_attack, 1)
    
    def test_battle_initialization_default(self):
        """Test battle initialization with unknown enemy"""
        battle = BattleEvent("Unknown")
        self.assertEqual(battle.enemy_name, "Unknown")
        self.assertEqual(battle.enemy_health, 2)
        self.assertEqual(battle.enemy_attack, 1)
    
    @patch('builtins.input', side_effect=['1'])  # Attack once
    @patch('builtins.print')
    def test_battle_attack_victory(self, mock_print, mock_input):
        """Test winning a battle by attacking"""
        # Set enemy health to 1 for quick victory
        self.battle.enemy_health = 1
        self.battle.game_manager = GameManager()
        
        # Mock the give_rewards method to avoid random behavior
        with patch.object(self.battle, 'give_rewards'):
            self.battle.run()
        
        # Enemy should be defeated
        self.assertEqual(self.battle.enemy_health, 0)


if __name__ == '__main__':
    unittest.main()