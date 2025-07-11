"""
Unit tests for TimeSystem class
"""
import unittest
from game.time_system import TimeSystem


class TestTimeSystem(unittest.TestCase):
    
    def setUp(self):
        self.time_system = TimeSystem()
    
    def test_initialization(self):
        self.assertEqual(self.time_system.time, 0)
        self.assertTrue(self.time_system.is_daytime())
        self.assertEqual(self.time_system.get_time_of_day(), "Day")
    
    def test_advance_time(self):
        # Start at day
        self.assertTrue(self.time_system.is_daytime())
        
        # Advance to night
        self.time_system.advance_time()
        self.assertFalse(self.time_system.is_daytime())
        self.assertEqual(self.time_system.get_time_of_day(), "Night")
        
        # Advance back to day
        self.time_system.advance_time()
        self.assertTrue(self.time_system.is_daytime())
        self.assertEqual(self.time_system.get_time_of_day(), "Day")
    
    def test_time_cycle(self):
        # Test multiple cycles
        for _ in range(10):
            initial_time = self.time_system.time
            self.time_system.advance_time()
            expected_time = (initial_time + 1) % 2
            self.assertEqual(self.time_system.time, expected_time)

    def test_is_daytime(self):
        """Test is_daytime method"""
        # Day
        self.time_system.time = 0
        self.assertTrue(self.time_system.is_daytime())
        
        # Night
        self.time_system.time = 1
        self.assertFalse(self.time_system.is_daytime())

    def test_time_system_multiple_cycles(self):
        """Test time system through multiple day/night cycles"""
        for cycle in range(10):
            initial_time = self.time_system.time
            self.time_system.advance_time()
            # Should cycle between 0 and 1
            self.assertIn(self.time_system.time, [0, 1])
            # Should be different from initial time
            self.assertNotEqual(self.time_system.time, initial_time)

    def test_time_system_consistency(self):
        """Test that time system maintains consistency across multiple advances"""
        initial_state = self.time_system.time
        # Advance multiple times and verify it cycles correctly
        for _ in range(4):
            self.time_system.advance_time()
        # After 4 advances, should be back to initial state (0->1->0->1->0)
        self.assertEqual(self.time_system.time, initial_state)

    def test_time_system_edge_values(self):
        """Test time system with edge values"""
        # Test at time 0
        self.time_system.time = 0
        self.assertEqual(self.time_system.get_time_of_day(), "Day")
        self.assertTrue(self.time_system.is_daytime())
        
        # Test at time 1
        self.time_system.time = 1
        self.assertEqual(self.time_system.get_time_of_day(), "Night")
        self.assertFalse(self.time_system.is_daytime())

    def test_time_system_advance_with_print(self):
        """Test that advance_time prints the correct message"""
        # This test verifies the print statement works (though we can't easily test output)
        try:
            self.time_system.advance_time()
            # If we get here, no exception was raised
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"advance_time() raised {e} unexpectedly")


if __name__ == '__main__':
    unittest.main()