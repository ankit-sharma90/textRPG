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

class WorldMap:
    """Represents a single world map"""
    
    def __init__(self, world_type, size=50):
        self.world_type = world_type
        self.size = size
        self.grid = [[CellType.EMPTY for _ in range(size)] for _ in range(size)]
        self.generate_map()
    
    def generate_map(self):
        """Generate the world map with random content"""
        total_cells = self.size * self.size
        
        # Distribution of content based on world type
        distributions = {
            WorldType.EARTH: {"enemy": 0.15, "npc": 0.08, "merchant": 0.03, "treasure": 0.05},
            WorldType.HEAVENLY_MOUNTAINS: {"enemy": 0.12, "npc": 0.10, "merchant": 0.02, "treasure": 0.08},
            WorldType.STONE_CAVERNS: {"enemy": 0.20, "npc": 0.05, "merchant": 0.02, "treasure": 0.10},
            WorldType.FUTURE_CITY: {"enemy": 0.10, "npc": 0.12, "merchant": 0.08, "treasure": 0.03},
            WorldType.PREHISTORIC_JUNGLE: {"enemy": 0.25, "npc": 0.03, "merchant": 0.01, "treasure": 0.06},
            WorldType.ATLANTIS: {"enemy": 0.18, "npc": 0.07, "merchant": 0.04, "treasure": 0.12}
        }
        
        dist = distributions[self.world_type]
        
        # Place content randomly
        for x in range(self.size):
            for y in range(self.size):
                rand = random.random()
                if rand < dist["enemy"]:
                    self.grid[x][y] = CellType.ENEMY
                elif rand < dist["enemy"] + dist["npc"]:
                    self.grid[x][y] = CellType.NPC
                elif rand < dist["enemy"] + dist["npc"] + dist["merchant"]:
                    self.grid[x][y] = CellType.MERCHANT
                elif rand < dist["enemy"] + dist["npc"] + dist["merchant"] + dist["treasure"]:
                    self.grid[x][y] = CellType.TREASURE
        
        # Add a few portals to other worlds (except starting world)
        if self.world_type != WorldType.EARTH:
            portal_count = random.randint(1, 3)
            for _ in range(portal_count):
                x, y = random.randint(0, self.size-1), random.randint(0, self.size-1)
                self.grid[x][y] = CellType.PORTAL
    
    def get_cell(self, x, y):
        """Get the content of a cell"""
        if 0 <= x < self.size and 0 <= y < self.size:
            return self.grid[x][y]
        return None

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
        return current_map.get_cell(self.player_x, self.player_y)
    
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
        
        if cell_content == CellType.ENEMY:
            return f"{base_desc} You sense danger nearby..."
        elif cell_content == CellType.NPC:
            return f"{base_desc} You see someone who might want to talk."
        elif cell_content == CellType.MERCHANT:
            return f"{base_desc} You spot a merchant's stall."
        elif cell_content == CellType.TREASURE:
            return f"{base_desc} Something glints in the distance."
        elif cell_content == CellType.PORTAL:
            return f"{base_desc} A mysterious portal shimmers before you."
        else:
            return f"{base_desc} The area seems quiet."
    
    def get_location_actions(self, cell_content):
        """Get available actions for the current location"""
        if cell_content == CellType.ENEMY:
            return [
                "Attack the enemy",
                "Try to sneak past",
                "Observe from distance"
            ]
        elif cell_content == CellType.NPC:
            return [
                "Talk to the NPC",
                "Ask for directions",
                "Request a quest"
            ]
        elif cell_content == CellType.MERCHANT:
            return [
                "Buy health potion (10 gold)",
                "Buy weapon upgrade (15 gold)",
                "Sell items for gold"
            ]
        elif cell_content == CellType.TREASURE:
            return [
                "Search the treasure",
                "Check for traps first",
                "Take only what you need"
            ]
        elif cell_content == CellType.PORTAL:
            return [
                "Step through the portal",
                "Examine the portal closely",
                "Touch the portal cautiously"
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
        """Get hint about what's in a specific direction"""
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
            return "blocked"
        
        cell_content = current_map.get_cell(target_x, target_y)
        
        hints = {
            CellType.ENEMY: "danger lurks",
            CellType.NPC: "someone waits",
            CellType.MERCHANT: "trade awaits",
            CellType.TREASURE: "riches glint",
            CellType.PORTAL: "magic shimmers",
            CellType.EMPTY: "path is clear"
        }
        
        return hints.get(cell_content, "unknown")
    
    def get_directional_options_with_hints(self):
        """Get movement options with hints about each direction"""
        directions = self.get_available_directions()
        options = []
        
        for direction in directions:
            hint = self.get_direction_hint(direction)
            direction_name = direction.capitalize()
            options.append(f"Move {direction_name} ({hint})")
        
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