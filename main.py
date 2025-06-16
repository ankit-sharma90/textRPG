#!/usr/bin/env python3
"""
Text RPG Game - Main Entry Point
"""
import sys
from game.game_manager import GameManager

def main():
    """Main entry point for the game"""
    game = GameManager()
    game.start_game()

if __name__ == "__main__":
    main()