"""
World module - Manages the game world and map
"""
import random
from enum import Enum

class WorldType(Enum):
    EARTH = "Earth"
    HEAVENLY_MOUNTAINS = "Heavenly Mountains"
    STONE_CAVERNS = "Stone Caverns"
    FUTURE_CITY = "Future City"
    PREHISTORIC_JUNGLE = "Prehistoric Jungle"
    ATLANTIS = "Atlantis"

class CellType(Enum):
    EMPTY = "empty"
    ENEMY = "enemy"
    NPC = "npc"
    MERCHANT = "merchant"
    TREASURE = "treasure"
    PORTAL = "portal"

class MajorEventType(Enum):
    DRAGON = "dragon"
    TREASURE_VAULT = "treasure_vault"
    MASTER_MERCHANT = "master_merchant"
    ANCIENT_PORTAL = "ancient_portal"
    BOSS_ENEMY = "boss_enemy"

class WorldMap:
    """Represents a single world map"""
    
    def __init__(self, world_type, size=50):
        self.world_type = world_type
        self.size = size
        self.grid = [[CellType.EMPTY for _ in range(size)] for _ in range(size)]
        self.major_events = {}  # {(x, y): MajorEventType}
        self.generate_map()
    
    def generate_map(self):
        """Generate only major events on the map"""
        # Generate 5-10 major events per world
        num_events = random.randint(5, 10)
        
        # Major event distributions by world type
        event_weights = {
            WorldType.EARTH: [MajorEventType.BOSS_ENEMY, MajorEventType.TREASURE_VAULT, MajorEventType.MASTER_MERCHANT],
            WorldType.HEAVENLY_MOUNTAINS: [MajorEventType.DRAGON, MajorEventType.ANCIENT_PORTAL, MajorEventType.TREASURE_VAULT],
            WorldType.STONE_CAVERNS: [MajorEventType.BOSS_ENEMY, MajorEventType.TREASURE_VAULT, MajorEventType.DRAGON],
            WorldType.FUTURE_CITY: [MajorEventType.MASTER_MERCHANT, MajorEventType.ANCIENT_PORTAL, MajorEventType.BOSS_ENEMY],
            WorldType.PREHISTORIC_JUNGLE: [MajorEventType.DRAGON, MajorEventType.BOSS_ENEMY, MajorEventType.TREASURE_VAULT],
            WorldType.ATLANTIS: [MajorEventType.ANCIENT_PORTAL, MajorEventType.TREASURE_VAULT, MajorEventType.DRAGON]
        }
        
        available_events = event_weights[self.world_type]
        
        # Place major events randomly across the map
        for _ in range(num_events):
            # Find empty location
            while True:
                x = random.randint(5, self.size-6)  # Keep away from edges
                y = random.randint(5, self.size-6)
                if (x, y) not in self.major_events:
                    break
            
            # Choose random major event type
            event_type = random.choice(available_events)
            self.major_events[(x, y)] = event_type
    
    def get_cell(self, x, y):
        """Get the content of a cell"""
        if 0 <= x < self.size and 0 <= y < self.size:
            # Check for major events first
            if (x, y) in self.major_events:
                return self.major_events[(x, y)]
            return self.grid[x][y]
        return None
    
    def has_major_event_at(self, x, y):
        """Check if there's a major event at coordinates"""
        return (x, y) in self.major_events

class World:
    """Manages the game world and map system"""
    
    def __init__(self):
        self.maps = {}
        self.current_world = WorldType.EARTH
        self.player_x = 25  # Start in center of map
        self.player_y = 25
        self.generate_all_worlds()
        
    def generate_all_worlds(self):
        """Generate all world maps at game start"""
        for world_type in WorldType:
            self.maps[world_type] = WorldMap(world_type)
    
    def get_current_map(self):
        """Get the current world map"""
        return self.maps[self.current_world]
    
    def get_current_cell(self):
        """Get the content of the current cell"""
        current_map = self.get_current_map()
        cell_content = current_map.get_cell(self.player_x, self.player_y)
        
        # If it's a major event, return it; otherwise generate random encounter
        if isinstance(cell_content, MajorEventType):
            return cell_content
        
        # Generate random encounter (70% chance of enemy)
        if random.random() < 0.7:
            return CellType.ENEMY
        else:
            return CellType.EMPTY
    
    def move_player(self, direction):
        """Move the player in a direction (north, east, south, west)"""
        old_x, old_y = self.player_x, self.player_y
        
        if direction == "north" and self.player_y > 0:
            self.player_y -= 1
        elif direction == "east" and self.player_x < 49:
            self.player_x += 1
        elif direction == "south" and self.player_y < 49:
            self.player_y += 1
        elif direction == "west" and self.player_x > 0:
            self.player_x -= 1
        else:
            return False, "You can't move in that direction."
        
        # Check what's at the new location
        cell_content = self.get_current_cell()
        return True, self.get_location_description(cell_content)
    
    def get_location_description(self, cell_content):
        """Get description of current location"""
        world_descriptions = {
            WorldType.EARTH: "a modern landscape",
            WorldType.HEAVENLY_MOUNTAINS: "ethereal mountain peaks",
            WorldType.STONE_CAVERNS: "dark stone caverns",
            WorldType.FUTURE_CITY: "a futuristic cityscape",
            WorldType.PREHISTORIC_JUNGLE: "a dense prehistoric jungle",
            WorldType.ATLANTIS: "the underwater city of Atlantis"
        }
        
        base_desc = f"You are in {world_descriptions[self.current_world]}."
        
        # Handle major events
        if isinstance(cell_content, MajorEventType):
            major_descriptions = {
                MajorEventType.DRAGON: f"{base_desc} A massive dragon blocks your path, its eyes glowing with ancient fury!",
                MajorEventType.TREASURE_VAULT: f"{base_desc} You discover a legendary treasure vault, sealed with ancient magic.",
                MajorEventType.MASTER_MERCHANT: f"{base_desc} A renowned master merchant has set up an exclusive trading post here.",
                MajorEventType.ANCIENT_PORTAL: f"{base_desc} An ancient portal radiates immense power, connecting to other realms.",
                MajorEventType.BOSS_ENEMY: f"{base_desc} A fearsome boss creature emerges, ready for battle!"
            }
            return major_descriptions.get(cell_content, f"{base_desc} Something extraordinary awaits.")
        
        # Handle regular encounters
        if cell_content == CellType.ENEMY:
            return f"{base_desc} You encounter a hostile creature!"
        else:
            return f"{base_desc} The area seems quiet."
    
    def get_location_actions(self, cell_content):
        """Get available actions for the current location"""
        # Handle major events
        if isinstance(cell_content, MajorEventType):
            if cell_content == MajorEventType.DRAGON:
                return [
                    "Challenge the dragon to combat",
                    "Attempt to negotiate",
                    "Try to sneak past"
                ]
            elif cell_content == MajorEventType.TREASURE_VAULT:
                return [
                    "Attempt to break the seal",
                    "Search for the key",
                    "Study the magical locks"
                ]
            elif cell_content == MajorEventType.MASTER_MERCHANT:
                return [
                    "Buy legendary weapon (50 gold)",
                    "Buy master health elixir (30 gold)",
                    "Trade rare items"
                ]
            elif cell_content == MajorEventType.ANCIENT_PORTAL:
                return [
                    "Activate the portal",
                    "Study the ancient runes",
                    "Channel your energy into it"
                ]
            elif cell_content == MajorEventType.BOSS_ENEMY:
                return [
                    "Engage in epic battle",
                    "Try to find weakness",
                    "Attempt tactical retreat"
                ]
        
        # Handle regular encounters
        if cell_content == CellType.ENEMY:
            return [
                "Attack the enemy",
                "Try to sneak past",
                "Observe from distance"
            ]
        else:
            return [
                "Rest and recover",
                "Search the area",
                "Set up camp"
            ]
    
    def get_available_directions(self):
        """Get list of available movement directions"""
        directions = []
        if self.player_y > 0:
            directions.append("north")
        if self.player_x < 49:
            directions.append("east")
        if self.player_y < 49:
            directions.append("south")
        if self.player_x > 0:
            directions.append("west")
        return directions
    
    def get_direction_hint(self, direction):
        """Get hint about major events in a specific direction (only if close)"""
        current_map = self.get_current_map()
        target_x, target_y = self.player_x, self.player_y
        
        if direction == "north" and self.player_y > 0:
            target_y -= 1
        elif direction == "east" and self.player_x < 49:
            target_x += 1
        elif direction == "south" and self.player_y < 49:
            target_y += 1
        elif direction == "west" and self.player_x > 0:
            target_x -= 1
        else:
            return None
        
        # Check for major events within 2 steps in that direction
        for distance in range(1, 3):
            check_x, check_y = target_x, target_y
            
            if direction == "north":
                check_y = target_y - distance + 1
            elif direction == "east":
                check_x = target_x + distance - 1
            elif direction == "south":
                check_y = target_y + distance - 1
            elif direction == "west":
                check_x = target_x - distance + 1
            
            if 0 <= check_x < 50 and 0 <= check_y < 50:
                if current_map.has_major_event_at(check_x, check_y):
                    event_type = current_map.major_events[(check_x, check_y)]
                    hints = {
                        MajorEventType.DRAGON: "ancient power stirs",
                        MajorEventType.TREASURE_VAULT: "great riches await",
                        MajorEventType.MASTER_MERCHANT: "legendary trader nearby",
                        MajorEventType.ANCIENT_PORTAL: "otherworldly energy pulses",
                        MajorEventType.BOSS_ENEMY: "terrible danger approaches"
                    }
                    return hints.get(event_type, "something significant")
        
        return None
    
    def get_directional_options_with_hints(self):
        """Get movement options with hints only for major events nearby"""
        directions = self.get_available_directions()
        options = []
        
        for direction in directions:
            hint = self.get_direction_hint(direction)
            direction_name = direction.capitalize()
            
            if hint:
                options.append(f"Move {direction_name} ({hint})")
            else:
                options.append(f"Move {direction_name}")
        
        return options
    
    def change_world(self, new_world):
        """Change to a different world"""
        if new_world in self.maps:
            self.current_world = new_world
            # Start at a random location in the new world
            self.player_x = random.randint(5, 44)
            self.player_y = random.randint(5, 44)
            return True
        return False