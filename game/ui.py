"""
UI module - Handles the user interface and display
"""
import os
import time

class UI:
    """Handles the user interface and display"""
    
    @staticmethod
    def clear_screen():
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def print_header(title):
        """Print a header with the given title"""
        UI.clear_screen()
        print("=" * 50)
        print(f"{title:^50}")
        print("=" * 50)
        print()
    
    @staticmethod
    def print_section(title):
        """Print a section header"""
        print("\n" + "-" * 50)
        print(f"{title:^50}")
        print("-" * 50)
    
    @staticmethod
    def print_status(player, time_system):
        """Print the player status"""
        UI.print_section("STATUS")
        print(f"Health: {player.health}/{player.max_health}")
        print(f"Gold: {player.gold}")
        print(f"Time: {time_system.get_time_of_day()}")
        if player.is_vampire:
            print("Status: Vampire (takes damage during day)")
        print()
    
    @staticmethod
    def print_options(options):
        """Print a list of options"""
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        print()
    
    @staticmethod
    def get_choice(options):
        """Get a valid choice from the user"""
        while True:
            try:
                choice = input("> ")
                choice_num = int(choice)
                if 1 <= choice_num <= len(options):
                    return choice_num
                else:
                    print(f"Please enter a number between 1 and {len(options)}")
            except ValueError:
                print("Please enter a valid number")
    
    @staticmethod
    def print_slow(text, delay=0.03):
        """Print text slowly for dramatic effect"""
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()
    
    @staticmethod
    def display_battle(player_health, player_max_health, enemy_name, enemy_health):
        """Display battle information"""
        UI.print_section(f"BATTLE: {enemy_name}")
        print(f"Your Health: {player_health}/{player_max_health}")
        print(f"{enemy_name}'s Health: {enemy_health}")
        print()
    
    @staticmethod
    def display_inventory(player):
        """Display the player's inventory"""
        UI.print_section("INVENTORY")
        if not player.inventory:
            print("Your inventory is empty.")
        else:
            for i, item in enumerate(player.inventory, 1):
                print(f"{i}. {item.name} - {item.description}")
        
        print(f"\nGold: {player.gold}")
        print(f"Equipped weapon: {player.equipped_weapon.name if player.equipped_weapon else 'None'}")
        print()