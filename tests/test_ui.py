"""
Unit tests for UI module
"""
import unittest
from unittest.mock import patch
from io import StringIO
from game.ui import UI
from game.player import Player
from game.time_system import TimeSystem


class TestUI(unittest.TestCase):
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_print_header(self, mock_stdout):
        UI.print_header("TEST GAME")
        output = mock_stdout.getvalue()
        self.assertIn("TEST GAME", output)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_print_status(self, mock_stdout):
        player = Player()
        time_system = TimeSystem()
        
        UI.print_status(player, time_system)
        output = mock_stdout.getvalue()
        self.assertIn("Health:", output)
        self.assertIn("Gold:", output)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_print_options(self, mock_stdout):
        options = ["Option 1", "Option 2", "Option 3"]
        UI.print_options(options)
        output = mock_stdout.getvalue()
        
        self.assertIn("1. Option 1", output)
        self.assertIn("2. Option 2", output)
        self.assertIn("3. Option 3", output)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_display_inventory_empty(self, mock_stdout):
        player = Player()
        UI.display_inventory(player)
        output = mock_stdout.getvalue()
        self.assertIn("empty", output.lower())
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_display_inventory_with_items(self, mock_stdout):
        from game.items import STICK
        player = Player()
        player.add_item(STICK)
        
        UI.display_inventory(player)
        output = mock_stdout.getvalue()
        self.assertIn("Stick", output)


if __name__ == '__main__':
    unittest.main()