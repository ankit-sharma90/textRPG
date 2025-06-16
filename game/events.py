"""
Events module - Defines game events and encounters
"""
import random
from game.items import STICK

class Event:
    """Base class for all game events"""
    
    def __init__(self, game_manager=None):
        self.game_manager = game_manager
        
    def run(self):
        """Run the event"""
        pass


class FirstEncounter(Event):
    """First NPC encounter at the start of the game"""
    
    def run(self):
        print("\nAn old man approaches you.")
        print("'Hello traveler! You look like you could use some help.'")
        print("'Take these, they might help you on your journey.'")
        print("\nThe old man offers you 10 gold and a stick.")
        
        print("\nChoose your action:")
        print("1. Reject the offering and move on")
        print("2. Take the goods and move on")
        print("3. Take the goods and fight the NPC")
        
        choice = input("> ")
        
        if choice == "1":
            print("\nYou reject the offering and move on.")
            print("The old man looks disappointed as you walk away.")
        elif choice == "2":
            print("\nYou accept the offering and thank the old man.")
            self.game_manager.player.add_gold(10)
            self.game_manager.player.add_item(STICK)
            self.game_manager.player.equip_weapon(STICK)
            print("The old man smiles and wishes you good luck on your journey.")
        elif choice == "3":
            print("\nYou take the offering and then attack the old man!")
            self.game_manager.player.add_gold(10)
            self.game_manager.player.add_item(STICK)
            self.game_manager.player.equip_weapon(STICK)
            
            # Start battle with NPC
            battle = BattleEvent("Old Man")
            battle.run()
        else:
            print("\nInvalid choice. You hesitate and the old man walks away.")


class BattleEvent(Event):
    """Battle encounter with an enemy"""
    
    def __init__(self, enemy_type):
        super().__init__()
        self.enemy_type = enemy_type
        
        # Set enemy stats based on type
        if enemy_type == "Goblin":
            self.enemy_health = 3
            self.enemy_attack = 1
            self.enemy_name = "Goblin"
        elif enemy_type == "Old Man":
            self.enemy_health = 5
            self.enemy_attack = 1
            self.enemy_name = "Old Man"
        else:
            # Default enemy
            self.enemy_health = 2
            self.enemy_attack = 1
            self.enemy_name = enemy_type
    
    def run(self):
        """Run the battle encounter"""
        print(f"\n===== BATTLE: {self.enemy_name} =====")
        print(f"Enemy Health: {self.enemy_health}")
        
        # Battle loop
        while self.enemy_health > 0:
            # Player's turn
            print("\nYour turn:")
            print("1. Attack")
            print("2. Defend")
            
            choice = input("> ")
            
            if choice == "1":
                # Player attacks
                damage = 1  # Default damage
                if hasattr(self, 'game_manager') and self.game_manager and self.game_manager.player.equipped_weapon:
                    damage = self.game_manager.player.get_attack_damage()
                
                print(f"You attack the {self.enemy_name} for {damage} damage!")
                self.enemy_health -= damage
                
                if self.enemy_health <= 0:
                    print(f"You defeated the {self.enemy_name}!")
                    self.give_rewards()
                    break
            elif choice == "2":
                # Player defends
                print("You take a defensive stance.")
                # Reduce incoming damage for this turn
                enemy_damage_reduction = 1
            else:
                print("Invalid choice. You hesitate.")
                enemy_damage_reduction = 0
            
            # Enemy's turn
            if self.enemy_health > 0:
                print(f"\n{self.enemy_name}'s turn:")
                damage = max(1, self.enemy_attack - enemy_damage_reduction if 'enemy_damage_reduction' in locals() else self.enemy_attack)
                print(f"The {self.enemy_name} attacks you for {damage} damage!")
                
                if hasattr(self, 'game_manager') and self.game_manager:
                    self.game_manager.player.take_damage(damage)
                    print(f"Your health: {self.game_manager.player.health}/{self.game_manager.player.max_health}")
                    
                    if self.game_manager.player.health <= 0:
                        print("You have been defeated!")
                        self.game_manager.handle_player_death()
                        break
    
    def give_rewards(self):
        """Give rewards to the player after winning a battle"""
        # Roll for loot
        roll = random.random()
        
        if hasattr(self, 'game_manager') and self.game_manager:
            # 90% chance for gold, 10% chance for equipment
            if roll < 0.9:
                gold_amount = random.randint(1, 5)
                print(f"You found {gold_amount} gold!")
                self.game_manager.player.add_gold(gold_amount)
            else:
                print("You found a better weapon!")
                # In V1, we only have the stick weapon
                # This would be expanded in future versions