"""
Unit tests for ASCII Theme module
"""
import unittest
from game.ascii_theme import ASCIITheme
from game.player import Player
from game.time_system import TimeSystem


class TestASCIITheme(unittest.TestCase):
    
    def test_title_exists(self):
        self.assertIsInstance(ASCIITheme.TITLE, str)
        self.assertIn("TEXT", ASCIITheme.TITLE)
        self.assertIn("RPG", ASCIITheme.TITLE)
    
    def test_health_bar_creation(self):
        # Test full health
        bar = ASCIITheme.create_health_bar(10, 10, 10)
        self.assertIn("[", bar)
        self.assertIn("]", bar)
        self.assertIn("10/10", bar)
        
        # Test half health
        bar = ASCIITheme.create_health_bar(5, 10, 10)
        self.assertIn("5/10", bar)
        
        # Test zero health
        bar = ASCIITheme.create_health_bar(0, 10, 10)
        self.assertIn("0/10", bar)
    
    def test_health_bar_zero_max(self):
        bar = ASCIITheme.create_health_bar(0, 0, 10)
        self.assertIn("0/0", bar)
    
    def test_bordered_text(self):
        text = "Test message"
        bordered = ASCIITheme.create_bordered_text(text)
        self.assertIn("┌", bordered)
        self.assertIn("└", bordered)
        self.assertIn("│", bordered)
        self.assertIn(text, bordered)
    
    def test_status_display(self):
        player = Player()
        time_system = TimeSystem()
        
        status = ASCIITheme.create_status_display(player, time_system)
        self.assertIn("Health:", status)
        self.assertIn("Gold:", status)
        self.assertIn("Day", status)
    
    def test_status_display_vampire(self):
        player = Player()
        player.is_vampire = True
        time_system = TimeSystem()
        
        status = ASCIITheme.create_status_display(player, time_system)
        self.assertIn("VAMPIRE", status)
    
    def test_battle_display(self):
        battle = ASCIITheme.create_battle_display(
            "Player", 10, 10, "Goblin", 3, 3, "Battle starts!"
        )
        self.assertIn("BATTLE", battle)
        self.assertIn("Player", battle)
        self.assertIn("Goblin", battle)
        self.assertIn("Battle starts!", battle)
    
    def test_menu_options(self):
        options = ["Attack", "Defend", "Run"]
        menu = ASCIITheme.create_menu_options(options)
        
        self.assertIn("[1] Attack", menu)
        self.assertIn("[2] Defend", menu)
        self.assertIn("[3] Run", menu)
        self.assertIn("┌", menu)
        self.assertIn("└", menu)
    
    def test_death_screen_exists(self):
        self.assertIsInstance(ASCIITheme.DEATH_SCREEN, str)
        self.assertIn("DEATH", ASCIITheme.DEATH_SCREEN)
    
    def test_victory_screen_exists(self):
        self.assertIsInstance(ASCIITheme.VICTORY_SCREEN, str)
        self.assertIn("VICTORY", ASCIITheme.VICTORY_SCREEN)
    
    def test_sprites_exist(self):
        self.assertIsInstance(ASCIITheme.PLAYER_SPRITE, str)
        self.assertIsInstance(ASCIITheme.GOBLIN_SPRITE, str)
        self.assertIsInstance(ASCIITheme.DRAGON_SPRITE, str)
    
    def test_arrows_dict(self):
        self.assertIn('north', ASCIITheme.ARROWS)
        self.assertIn('south', ASCIITheme.ARROWS)
        self.assertIn('east', ASCIITheme.ARROWS)
        self.assertIn('west', ASCIITheme.ARROWS)


if __name__ == '__main__':
    unittest.main()