"""
Game Manager - Controls the main game loop and state
"""
import random
from game.player import Player
from game.world import World, CellType
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
        # Show current location
        cell_content = self.world.get_current_cell()
        location_desc = self.world.get_location_description(cell_content)
        print(f"\n{location_desc}")
        
        # Show available directions
        directions = self.world.get_available_directions()
        print(f"Available directions: {', '.join(directions)}")
        
        print("\nChoose an action:")
        print("1. Move North" if "north" in directions else "")
        print("2. Move East" if "east" in directions else "")
        print("3. Move South" if "south" in directions else "")
        print("4. Move West" if "west" in directions else "")
        print("5. Interact with location")
        print("6. Check inventory")
        print("7. Quit game")
        
        choice = input("> ")
        
        if choice == "1" and "north" in directions:
            success, message = self.world.move_player("north")
            print(message)
            if success:
                self.action_taken()
        elif choice == "2" and "east" in directions:
            success, message = self.world.move_player("east")
            print(message)
            if success:
                self.action_taken()
        elif choice == "3" and "south" in directions:
            success, message = self.world.move_player("south")
            print(message)
            if success:
                self.action_taken()
        elif choice == "4" and "west" in directions:
            success, message = self.world.move_player("west")
            print(message)
            if success:
                self.action_taken()
        elif choice == "5":
            self.interact_with_location()
        elif choice == "6":
            self.player.show_inventory()
        elif choice == "7":
            self.game_over = True
            print("Thanks for playing!")
        else:
            print("Invalid choice. Try again.")
    
    def interact_with_location(self, action_choice=None):
        """Interact with the current location"""
        from game.events import BattleEvent
        
        cell_content = self.world.get_current_cell()
        
        if cell_content == CellType.ENEMY:
            if action_choice == 1:  # Attack the enemy
                print("You've encountered an enemy!")
                battle = BattleEvent("Goblin")
                battle.run()
            elif action_choice == 2:  # Try to sneak past
                if random.random() < 0.6:
                    print("You successfully sneak past the enemy!")
                else:
                    print("You failed to sneak past! The enemy notices you!")
                    battle = BattleEvent("Goblin")
                    battle.run()
            elif action_choice == 3:  # Observe from distance
                print("You observe the enemy from a safe distance.")
                print("It's a Goblin with 3 health. It looks aggressive.")
            self.action_taken()
            
        elif cell_content == CellType.NPC:
            if action_choice == 1:  # Talk to the NPC
                print("You talk to a local NPC.")
                print("'Greetings, traveler! The roads are dangerous these days.'")
            elif action_choice == 2:  # Ask for directions
                print("'The nearest town is to the east, but beware of the goblins!'")
            elif action_choice == 3:  # Request a quest
                quest_reward = random.randint(3, 8)
                self.player.gold += quest_reward
                print(f"'I lost my ring nearby. Here's {quest_reward} gold for finding it!'")
                print("(You pretend to find the ring)")
            self.action_taken()
            
        elif cell_content == CellType.MERCHANT:
            if action_choice == 1:  # Buy health potion
                if self.player.gold >= 10:
                    self.player.gold -= 10
                    heal_amount = random.randint(3, 7)
                    self.player.health = min(self.player.max_health, self.player.health + heal_amount)
                    print(f"You buy a health potion and recover {heal_amount} health!")
                else:
                    print("You don't have enough gold for a health potion.")
            elif action_choice == 2:  # Buy weapon upgrade
                if self.player.gold >= 15:
                    self.player.gold -= 15
                    # Increase attack damage (simplified)
                    print("You buy a weapon upgrade! Your attacks are now stronger!")
                    print("(Attack damage increased)")
                else:
                    print("You don't have enough gold for a weapon upgrade.")
            elif action_choice == 3:  # Sell items
                gold_earned = random.randint(2, 6)
                self.player.gold += gold_earned
                print(f"You sell some old items for {gold_earned} gold.")
            self.action_taken()
            
        elif cell_content == CellType.TREASURE:
            if action_choice == 1:  # Search the treasure
                gold_found = random.randint(8, 15)
                self.player.gold += gold_found
                print(f"You search the treasure and find {gold_found} gold!")
            elif action_choice == 2:  # Check for traps first
                if random.random() < 0.3:
                    print("You find a trap! You carefully disarm it.")
                    gold_found = random.randint(12, 20)
                    self.player.gold += gold_found
                    print(f"Safe treasure yields {gold_found} gold!")
                else:
                    print("No traps detected.")
                    gold_found = random.randint(8, 15)
                    self.player.gold += gold_found
                    print(f"You find {gold_found} gold!")
            elif action_choice == 3:  # Take only what you need
                gold_found = random.randint(5, 10)
                self.player.gold += gold_found
                print(f"You take {gold_found} gold and leave the rest.")
                print("Your restraint is noted by the universe...")
            
            # Remove treasure from this location
            current_map = self.world.get_current_map()
            current_map.grid[self.world.player_x][self.world.player_y] = CellType.EMPTY
            self.action_taken()
            
        elif cell_content == CellType.PORTAL:
            if action_choice == 1:  # Step through portal
                print("You step through the mysterious portal...")
                print("The world swirls around you, but nothing happens yet.")
                print("(Portal travel will be implemented later)")
            elif action_choice == 2:  # Examine closely
                print("You examine the portal closely.")
                print("Ancient runes glow with otherworldly energy.")
                print("It seems to lead to another realm...")
            elif action_choice == 3:  # Touch cautiously
                print("You cautiously touch the portal.")
                print("A warm energy flows through your hand.")
                heal_amount = random.randint(1, 3)
                self.player.health = min(self.player.max_health, self.player.health + heal_amount)
                print(f"You feel refreshed! Recovered {heal_amount} health.")
            self.action_taken()
            
        else:  # Empty location
            if action_choice == 1:  # Rest and recover
                heal_amount = random.randint(1, 3)
                self.player.health = min(self.player.max_health, self.player.health + heal_amount)
                print(f"You rest and recover {heal_amount} health.")
            elif action_choice == 2:  # Search the area
                if random.random() < 0.3:
                    gold_found = random.randint(1, 4)
                    self.player.gold += gold_found
                    print(f"You search the area and find {gold_found} gold!")
                else:
                    print("You search the area but find nothing.")
            elif action_choice == 3:  # Set up camp
                heal_amount = random.randint(2, 5)
                self.player.health = min(self.player.max_health, self.player.health + heal_amount)
                print(f"You set up camp and rest well. Recovered {heal_amount} health.")
            self.action_taken()
    
    def handle_location_interaction(self, action_choice):
        """Handle location interaction and return result message"""
        from game.events import BattleEvent
        from game.world import MajorEventType
        
        cell_content = self.world.get_current_cell()
        result_message = ""
        
        # Handle major events first
        if isinstance(cell_content, MajorEventType):
            if cell_content == MajorEventType.TREASURE_VAULT:
                if action_choice == 1:  # Attempt to break the seal
                    gold_found = random.randint(50, 100)
                    self.player.gold += gold_found
                    result_message = f"You break the ancient seal! The vault opens, revealing {gold_found} gold!"
                elif action_choice == 2:  # Search for the key
                    gold_found = random.randint(30, 60)
                    self.player.gold += gold_found
                    result_message = f"You find a hidden key and unlock the vault safely, gaining {gold_found} gold!"
                elif action_choice == 3:  # Study the magical locks
                    heal_amount = random.randint(5, 10)
                    self.player.health = min(self.player.max_health, self.player.health + heal_amount)
                    result_message = f"Studying the magic teaches you ancient healing. You recover {heal_amount} health!"
            
            elif cell_content == MajorEventType.MASTER_MERCHANT:
                if action_choice == 1:  # Buy legendary weapon
                    if self.player.gold >= 50:
                        self.player.gold -= 50
                        result_message = "You purchase a legendary weapon! Your attack power has greatly increased!"
                    else:
                        result_message = "You don't have enough gold for the legendary weapon (50 gold needed)."
                elif action_choice == 2:  # Buy master health elixir
                    if self.player.gold >= 30:
                        self.player.gold -= 30
                        self.player.max_health += 5
                        self.player.health = self.player.max_health
                        result_message = "You drink the master elixir! Your maximum health increased by 5 and you're fully healed!"
                    else:
                        result_message = "You don't have enough gold for the master elixir (30 gold needed)."
                elif action_choice == 3:  # Trade rare items
                    gold_earned = random.randint(20, 40)
                    self.player.gold += gold_earned
                    result_message = f"You trade rare items with the master merchant for {gold_earned} gold."
            
            elif cell_content == MajorEventType.DRAGON:
                if action_choice == 1:  # Challenge to combat
                    result_message = "You challenge the mighty dragon to battle!"
                    # This should trigger a battle, handled in the web API
                elif action_choice == 2:  # Attempt to negotiate
                    if random.random() < 0.3:
                        gold_reward = random.randint(30, 50)
                        self.player.gold += gold_reward
                        result_message = f"The dragon is impressed by your courage and grants you {gold_reward} gold!"
                    else:
                        result_message = "The dragon roars angrily! Negotiation failed - prepare for battle!"
                elif action_choice == 3:  # Try to sneak past
                    if random.random() < 0.4:
                        result_message = "You successfully sneak past the sleeping dragon!"
                    else:
                        result_message = "The dragon awakens and spots you! Battle is inevitable!"
            
            elif cell_content == MajorEventType.ANCIENT_PORTAL:
                if action_choice == 1:  # Activate the portal
                    result_message = "The portal activates with blinding light! (Portal travel not yet implemented)"
                elif action_choice == 2:  # Study the runes
                    heal_amount = random.randint(3, 8)
                    self.player.health = min(self.player.max_health, self.player.health + heal_amount)
                    result_message = f"The ancient runes teach you forgotten magic. You recover {heal_amount} health!"
                elif action_choice == 3:  # Channel energy
                    gold_found = random.randint(10, 25)
                    self.player.gold += gold_found
                    result_message = f"Channeling energy into the portal creates {gold_found} gold from pure magic!"
            
            elif cell_content == MajorEventType.BOSS_ENEMY:
                if action_choice == 1:  # Engage in epic battle
                    result_message = "You engage the boss enemy in epic combat!"
                    # This should trigger a battle, handled in the web API
                elif action_choice == 2:  # Find weakness
                    result_message = "You study the boss and discover its weakness! You'll have an advantage in battle!"
                elif action_choice == 3:  # Tactical retreat
                    if random.random() < 0.6:
                        result_message = "You successfully retreat from the dangerous boss enemy!"
                    else:
                        result_message = "Retreat failed! The boss blocks your escape - battle begins!"
        
        elif cell_content == CellType.ENEMY:
            if action_choice == 1:  # Attack the enemy
                result_message = "You've encountered an enemy!"
            elif action_choice == 2:  # Try to sneak past
                if random.random() < 0.6:
                    result_message = "You successfully sneak past the enemy!"
                else:
                    result_message = "You failed to sneak past! The enemy notices you!"
            elif action_choice == 3:  # Observe from distance
                result_message = "You observe the enemy from a safe distance. It's a Goblin with 3 health."
            
        elif cell_content == CellType.NPC:
            if action_choice == 1:  # Talk to the NPC
                result_message = "You talk to a local NPC. 'Greetings, traveler! The roads are dangerous these days.'"
            elif action_choice == 2:  # Ask for directions
                result_message = "'The nearest town is to the east, but beware of the goblins!'"
            elif action_choice == 3:  # Request a quest
                quest_reward = random.randint(3, 8)
                self.player.gold += quest_reward
                result_message = f"'I lost my ring nearby. Here's {quest_reward} gold for finding it!' (You pretend to find the ring)"
                
        elif cell_content == CellType.MERCHANT:
            if action_choice == 1:  # Buy health potion
                if self.player.gold >= 10:
                    self.player.gold -= 10
                    heal_amount = random.randint(3, 7)
                    self.player.health = min(self.player.max_health, self.player.health + heal_amount)
                    result_message = f"You buy a health potion and recover {heal_amount} health!"
                else:
                    result_message = "You don't have enough gold for a health potion."
            elif action_choice == 2:  # Buy weapon upgrade
                if self.player.gold >= 15:
                    self.player.gold -= 15
                    result_message = "You buy a weapon upgrade! Your attacks are now stronger!"
                else:
                    result_message = "You don't have enough gold for a weapon upgrade."
            elif action_choice == 3:  # Sell items
                gold_earned = random.randint(2, 6)
                self.player.gold += gold_earned
                result_message = f"You sell some old items for {gold_earned} gold."
                
        elif cell_content == CellType.TREASURE:
            if action_choice == 1:  # Search the treasure
                gold_found = random.randint(8, 15)
                self.player.gold += gold_found
                result_message = f"You search the treasure and find {gold_found} gold!"
            elif action_choice == 2:  # Check for traps first
                if random.random() < 0.3:
                    gold_found = random.randint(12, 20)
                    self.player.gold += gold_found
                    result_message = f"You find a trap! You carefully disarm it. Safe treasure yields {gold_found} gold!"
                else:
                    gold_found = random.randint(8, 15)
                    self.player.gold += gold_found
                    result_message = f"No traps detected. You find {gold_found} gold!"
            elif action_choice == 3:  # Take only what you need
                gold_found = random.randint(5, 10)
                self.player.gold += gold_found
                result_message = f"You take {gold_found} gold and leave the rest. Your restraint is noted..."
            
            # Remove treasure from this location
            current_map = self.world.get_current_map()
            current_map.grid[self.world.player_x][self.world.player_y] = CellType.EMPTY
            
        elif cell_content == CellType.PORTAL:
            if action_choice == 1:  # Step through portal
                result_message = "You step through the mysterious portal... The world swirls around you, but nothing happens yet."
            elif action_choice == 2:  # Examine closely
                result_message = "You examine the portal closely. Ancient runes glow with otherworldly energy."
            elif action_choice == 3:  # Touch cautiously
                heal_amount = random.randint(1, 3)
                self.player.health = min(self.player.max_health, self.player.health + heal_amount)
                result_message = f"You cautiously touch the portal. A warm energy flows through you. Recovered {heal_amount} health."
                
        else:  # Empty location
            if action_choice == 1:  # Rest and recover
                heal_amount = random.randint(1, 3)
                self.player.health = min(self.player.max_health, self.player.health + heal_amount)
                result_message = f"You rest and recover {heal_amount} health."
            elif action_choice == 2:  # Search the area
                if random.random() < 0.3:
                    gold_found = random.randint(1, 4)
                    self.player.gold += gold_found
                    result_message = f"You search the area and find {gold_found} gold!"
                else:
                    result_message = "You search the area but find nothing."
            elif action_choice == 3:  # Set up camp
                heal_amount = random.randint(2, 5)
                self.player.health = min(self.player.max_health, self.player.health + heal_amount)
                result_message = f"You set up camp and rest well. Recovered {heal_amount} health."
        
        self.action_taken()
        return result_message
    
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