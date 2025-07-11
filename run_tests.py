#!/usr/bin/env python3
"""
Test runner for the Text RPG game
"""
import unittest
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def run_tests(verbosity=1):
    """Run all tests in the tests directory"""
    # Discover and run tests
    loader = unittest.TestLoader()
    start_dir = 'tests'
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)
    
    # Return True if all tests passed
    return result.wasSuccessful()

if __name__ == '__main__':
    # Check for verbose flag
    verbose = '-v' in sys.argv or '--verbose' in sys.argv
    verbosity = 2 if verbose else 1
    
    print("Running Text RPG Game Tests...")
    print("=" * 50)
    
    success = run_tests(verbosity)
    
    if success:
        print("\n" + "=" * 50)
        print("All tests passed! ✅")
        sys.exit(0)
    else:
        print("\n" + "=" * 50)
        print("Some tests failed! ❌")
        sys.exit(1)