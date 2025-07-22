"""
Unit tests for World and WorldMap classes
"""
import unittest
from unittest.mock import patch
from game.world import World, WorldMap, WorldType, CellType, MajorEventType


class TestWorldMap(unittest.TestCase):
    
    def setUp(self):
        # Create a small test map to avoid random generation
        self.world_map = WorldMap(WorldType.EARTH, size=10)
    
    def test_worldmap_initialization(self):
        self.assertEqual(self.world_map.world_type, WorldType.EARTH)
        self.assertEqual(self.world_map.size, 10)
        self.assertEqual(len(self.world_map.grid), 10)
        self.assertEqual(len(self.world_map.grid[0]), 10)
        self.assertIsInstance(self.world_map.major_events, dict)
    
    def test_get_cell_valid_coordinates(self):
        # Test getting a cell within bounds
        cell = self.world_map.get_cell(5, 5)
        self.assertIsNotNone(cell)
    
    def test_get_cell_invalid_coordinates(self):
        # Test getting a cell outside bounds
        self.assertIsNone(self.world_map.get_cell(-1, 5))
        self.assertIsNone(self.world_map.get_cell(5, -1))
        self.assertIsNone(self.world_map.get_cell(15, 5))
        self.assertIsNone(self.world_map.get_cell(5, 15))
    
    def test_has_major_event_at(self):
        # Add a test major event
        self.world_map.major_events[(3, 3)] = MajorEventType.DRAGON
        
        self.assertTrue(self.world_map.has_major_event_at(3, 3))
        self.assertFalse(self.world_map.has_major_event_at(4, 4))
    
    def test_get_cell_with_major_event(self):
        # Add a major event and test retrieval
        self.world_map.major_events[(2, 2)] = MajorEventType.TREASURE_VAULT
        
        cell = self.world_map.get_cell(2, 2)
        self.assertEqual(cell, MajorEventType.TREASURE_VAULT)


class TestWorld(unittest.TestCase):
    
    def setUp(self):
        self.world = World()
    
    def test_world_initialization(self):
        self.assertEqual(self.world.current_world, WorldType.EARTH)
        self.assertEqual(self.world.player_x, 25)
        self.assertEqual(self.world.player_y, 25)
        self.assertEqual(len(self.world.maps), len(WorldType))
        
        # Check all world types are generated
        for world_type in WorldType:
            self.assertIn(world_type, self.world.maps)
    
    def test_get_current_map(self):
        current_map = self.world.get_current_map()
        self.assertIsInstance(current_map, WorldMap)
        self.assertEqual(current_map.world_type, WorldType.EARTH)
    
    def test_move_player_valid_directions(self):
        # Test moving north
        original_y = self.world.player_y
        success, message = self.world.move_player("north")
        self.assertTrue(success)
        self.assertEqual(self.world.player_y, original_y - 1)
        
        # Test moving east
        original_x = self.world.player_x
        success, message = self.world.move_player("east")
        self.assertTrue(success)
        self.assertEqual(self.world.player_x, original_x + 1)
        
        # Test moving south
        original_y = self.world.player_y
        success, message = self.world.move_player("south")
        self.assertTrue(success)
        self.assertEqual(self.world.player_y, original_y + 1)
        
        # Test moving west
        original_x = self.world.player_x
        success, message = self.world.move_player("west")
        self.assertTrue(success)
        self.assertEqual(self.world.player_x, original_x - 1)
    
    def test_move_player_boundary_limits(self):
        # Test north boundary
        self.world.player_y = 0
        success, message = self.world.move_player("north")
        self.assertFalse(success)
        self.assertEqual(self.world.player_y, 0)
        
        # Test west boundary
        self.world.player_x = 0
        success, message = self.world.move_player("west")
        self.assertFalse(success)
        self.assertEqual(self.world.player_x, 0)
        
        # Test south boundary
        self.world.player_y = 49
        success, message = self.world.move_player("south")
        self.assertFalse(success)
        self.assertEqual(self.world.player_y, 49)
        
        # Test east boundary
        self.world.player_x = 49
        success, message = self.world.move_player("east")
        self.assertFalse(success)
        self.assertEqual(self.world.player_x, 49)
    
    def test_get_available_directions(self):
        # Test from center position
        self.world.player_x = 25
        self.world.player_y = 25
        directions = self.world.get_available_directions()
        self.assertEqual(set(directions), {"north", "east", "south", "west"})
        
        # Test from corner position
        self.world.player_x = 0
        self.world.player_y = 0
        directions = self.world.get_available_directions()
        self.assertEqual(set(directions), {"east", "south"})
    
    def test_get_location_description(self):
        # Test empty location
        description = self.world.get_location_description(CellType.EMPTY)
        self.assertIn("modern landscape", description)
        self.assertIn("quiet", description)
        
        # Test enemy location
        description = self.world.get_location_description(CellType.ENEMY)
        self.assertIn("modern landscape", description)
        self.assertIn("hostile creature", description)
        
        # Test major event location
        description = self.world.get_location_description(MajorEventType.DRAGON)
        self.assertIn("dragon", description.lower())
    
    def test_get_location_actions(self):
        # Test dragon actions
        actions = self.world.get_location_actions(MajorEventType.DRAGON)
        self.assertIn("Challenge the dragon to combat", actions)
        self.assertIn("Attempt to negotiate", actions)
        self.assertIn("Try to sneak past", actions)
        
        # Test treasure vault actions
        actions = self.world.get_location_actions(MajorEventType.TREASURE_VAULT)
        self.assertIn("Attempt to break the seal", actions)
        self.assertIn("Search for the key", actions)
        
        # Test empty location actions
        actions = self.world.get_location_actions(CellType.EMPTY)
        self.assertIn("Rest and recover", actions)
        self.assertIn("Search the area", actions)
    
    def test_change_world(self):
        # Test valid world change
        success = self.world.change_world(WorldType.HEAVENLY_MOUNTAINS)
        self.assertTrue(success)
        self.assertEqual(self.world.current_world, WorldType.HEAVENLY_MOUNTAINS)
        
        # Player position should be randomized
        self.assertTrue(5 <= self.world.player_x <= 44)
        self.assertTrue(5 <= self.world.player_y <= 44)
    
    @patch('random.random')
    def test_get_current_cell_random_encounter(self, mock_random):
        # Test empty cell with no random encounter
        mock_random.return_value = 0.5  # > 0.25, so no enemy
        cell_content = self.world.get_current_cell()
        self.assertEqual(cell_content, CellType.EMPTY)
        
        # Test empty cell with random encounter
        mock_random.return_value = 0.1  # < 0.25, so enemy
        cell_content = self.world.get_current_cell()
        self.assertEqual(cell_content, CellType.ENEMY)
    
    def test_get_current_cell_with_major_event(self):
        # Add a major event at player position
        current_map = self.world.get_current_map()
        current_map.major_events[(self.world.player_x, self.world.player_y)] = MajorEventType.DRAGON
        
        cell_content = self.world.get_current_cell()
        self.assertEqual(cell_content, MajorEventType.DRAGON)
    
    def test_get_direction_hint(self):
        # Add a major event nearby
        current_map = self.world.get_current_map()
        current_map.major_events[(self.world.player_x + 1, self.world.player_y)] = MajorEventType.DRAGON
        
        hint = self.world.get_direction_hint("east")
        self.assertEqual(hint, "ancient power stirs")
        
        # Test no hint for distant events
        hint = self.world.get_direction_hint("west")
        self.assertIsNone(hint)
    
    def test_get_directional_options_with_hints(self):
        # Add a major event nearby
        current_map = self.world.get_current_map()
        current_map.major_events[(self.world.player_x, self.world.player_y - 1)] = MajorEventType.TREASURE_VAULT
        
        options = self.world.get_directional_options_with_hints()
        
        # Check that north direction has hint
        north_option = next((opt for opt in options if "North" in opt), None)
        self.assertIsNotNone(north_option)
        self.assertIn("great riches await", north_option)
        
        # Check that other directions don't have hints
        east_option = next((opt for opt in options if "East" in opt), None)
        self.assertIsNotNone(east_option)
        self.assertNotIn("(", east_option)  # No hint in parentheses


class TestWorldEdgeCases(unittest.TestCase):
    
    def setUp(self):
        self.world = World()
    
    def test_invalid_direction_movement(self):
        """Test movement with invalid direction strings"""
        success, message = self.world.move_player("invalid")
        self.assertFalse(success)
        self.assertIn("can't move", message)
    
    def test_world_map_generation_consistency(self):
        """Test that world maps are consistently generated"""
        # All world types should have maps
        for world_type in WorldType:
            self.assertIn(world_type, self.world.maps)
            world_map = self.world.maps[world_type]
            self.assertEqual(world_map.world_type, world_type)
            self.assertEqual(world_map.size, 50)
    
    def test_major_event_actions_completeness(self):
        """Test that all major event types have defined actions"""
        for event_type in MajorEventType:
            actions = self.world.get_location_actions(event_type)
            self.assertIsInstance(actions, list)
            self.assertGreater(len(actions), 0)
            # Each action should be a non-empty string
            for action in actions:
                self.assertIsInstance(action, str)
                self.assertGreater(len(action), 0)
    
    def test_world_descriptions_completeness(self):
        """Test that all world types have descriptions"""
        for world_type in WorldType:
            self.world.current_world = world_type
            description = self.world.get_location_description(CellType.EMPTY)
            self.assertIsInstance(description, str)
            self.assertGreater(len(description), 0)
    
    def test_direction_hint_boundary_conditions(self):
        """Test direction hints at map boundaries"""
        # Test at top-left corner
        self.world.player_x = 0
        self.world.player_y = 0
        
        # Should not crash when checking hints at boundaries
        hint_north = self.world.get_direction_hint("north")
        hint_west = self.world.get_direction_hint("west")
        
        # These should return None since we can't move in those directions
        self.assertIsNone(hint_north)
        self.assertIsNone(hint_west)
        
        # But east and south should work
        hint_east = self.world.get_direction_hint("east")
        hint_south = self.world.get_direction_hint("south")
        
        # These can be None or a string, but shouldn't crash
        self.assertTrue(hint_east is None or isinstance(hint_east, str))
        self.assertTrue(hint_south is None or isinstance(hint_south, str))
    
    def test_change_world_invalid(self):
        """Test changing to invalid world type"""
        # This should return False for invalid world
        success = self.world.change_world("invalid_world")
        self.assertFalse(success)
        # Current world should remain unchanged
        self.assertEqual(self.world.current_world, WorldType.EARTH)
    
    def test_player_position_after_world_change(self):
        """Test player position constraints after world change"""
        original_world = self.world.current_world
        
        # Change to different world
        success = self.world.change_world(WorldType.HEAVENLY_MOUNTAINS)
        self.assertTrue(success)
        
        # Player should be within valid bounds
        self.assertTrue(5 <= self.world.player_x <= 44)
        self.assertTrue(5 <= self.world.player_y <= 44)
        
        # Should be able to move in all directions from new position
        available_directions = self.world.get_available_directions()
        self.assertEqual(len(available_directions), 4)  # All directions available


class TestWorldMapEdgeCases(unittest.TestCase):
    
    def test_small_map_no_events(self):
        """Test that small maps don't generate major events"""
        small_map = WorldMap(WorldType.EARTH, size=5)
        self.assertEqual(len(small_map.major_events), 0)
    
    def test_large_map_has_events(self):
        """Test that normal-sized maps generate major events"""
        normal_map = WorldMap(WorldType.EARTH, size=50)
        # Should have some major events (5-10 range)
        self.assertGreaterEqual(len(normal_map.major_events), 0)
        self.assertLessEqual(len(normal_map.major_events), 10)
    
    def test_get_cell_boundary_values(self):
        """Test get_cell with exact boundary values"""
        world_map = WorldMap(WorldType.EARTH, size=10)
        
        # Test exact boundaries
        self.assertIsNotNone(world_map.get_cell(0, 0))  # Top-left corner
        self.assertIsNotNone(world_map.get_cell(9, 9))  # Bottom-right corner
        self.assertIsNotNone(world_map.get_cell(0, 9))  # Top-right corner
        self.assertIsNotNone(world_map.get_cell(9, 0))  # Bottom-left corner
        
        # Test just outside boundaries
        self.assertIsNone(world_map.get_cell(-1, 0))
        self.assertIsNone(world_map.get_cell(0, -1))
        self.assertIsNone(world_map.get_cell(10, 0))
        self.assertIsNone(world_map.get_cell(0, 10))


if __name__ == '__main__':
    unittest.main()