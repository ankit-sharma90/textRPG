"""
World module - Manages the game world and map
"""
import random
from game.events import BattleEvent

class World:
    """Manages the game world and map"""
    
    def __init__(self):
        # Map is not visible to player in V1
        self.current_location = "Earth"
        
    def move_player(self):
        """Move the player on the map and trigger random events"""
        print("You move to a new location...")
        
        # 70% chance of encountering an enemy in V1
        if random.random() < 0.7:
            print("You've encountered an enemy!")
            battle = BattleEvent("Goblin")
            battle.run()
        else:
            print("You find nothing of interest here.")