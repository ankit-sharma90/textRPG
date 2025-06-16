"""
Game Manager - Controls the main game loop and state
"""
from game.player import Player
from game.world import World
from game.time_system import TimeSystem
from game.events import FirstEncounter

class GameManager:
    """Manages the game state and main loop"""
    
    def __init__(self):
        self.player = Player()
        self.world = World()
        self.time_system = TimeSystem()
        self.action_count = 0
        self.game_over = False
        
    def start_game(self):
        """Start the game with the first encounter"""
        print("Welcome to Text RPG!")
        print("-------------------")
        
        # Start with the first encounter
        first_event = FirstEncounter(self)
        first_event.run()
        
        # Main game loop
        while not self.game_over:
            self.show_status()
            self.process_action()
            
    def show_status(self):
        """Display the current game status"""
        print("\n===== STATUS =====")
        print(f"Health: {self.player.health}/{self.player.max_health}")
        print(f"Gold: {self.player.gold}")
        print(f"Time: {self.time_system.get_time_of_day()}")
        print("=================\n")
        
    def process_action(self):
        """Process a player action"""
        print("Choose an action:")
        print("1. Move on the map")
        print("2. Check inventory")
        print("3. Quit game")
        
        choice = input("> ")
        
        if choice == "1":
            self.world.move_player()
            self.action_taken()
        elif choice == "2":
            self.player.show_inventory()
        elif choice == "3":
            self.game_over = True
            print("Thanks for playing!")
        else:
            print("Invalid choice. Try again.")
    
    def action_taken(self):
        """Update game state after an action is taken"""
        self.action_count += 1
        
        # Update time (day/night cycle every 3 actions)
        if self.action_count % 3 == 0:
            self.time_system.advance_time()
            
            # If player is a vampire, take damage during day
            if self.player.is_vampire and self.time_system.is_daytime():
                damage = int(self.player.max_health * 0.05)
                self.player.take_damage(damage)
                print(f"You take {damage} sun damage as a vampire!")
                
                if self.player.health <= 0:
                    self.handle_player_death()
    
    def handle_player_death(self):
        """Handle player death"""
        print("\n===== YOU DIED =====")
        print("Choose your fate:")
        print("1. Lose everything and start new")
        print("2. Resurrect as a vampire (keep items but take 5% damage during day)")
        
        choice = input("> ")
        
        if choice == "1":
            # Reset player
            self.player = Player()
            print("You've been reborn. All progress lost.")
        elif choice == "2":
            # Resurrect as vampire
            self.player.resurrect_as_vampire()
            print("You've been resurrected as a vampire!")
        else:
            print("Invalid choice. Defaulting to option 1.")
            self.player = Player()
            print("You've been reborn. All progress lost.")