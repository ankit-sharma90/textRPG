"""
Unit tests for Web API endpoints
"""
import unittest
from unittest.mock import patch, MagicMock
import json
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app


class TestWebAPI(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_index_route(self):
        """Test the main index route"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Medieval Text RPG', response.data)
    
    def test_start_game_endpoint(self):
        """Test starting a new game"""
        response = self.app.post('/api/start_game')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('message', data)
        self.assertIn('player', data)
        self.assertIn('options', data)
        self.assertIn('event', data)
    
    def test_process_action_endpoint(self):
        """Test processing an action"""
        # Start a game first
        self.app.post('/api/start_game')
        
        # Process an action
        response = self.app.post('/api/action', 
                                json={'action': 'first_encounter', 'event': 'first_encounter', 'choice': 1})
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('message', data)
    
    def test_invalid_action(self):
        """Test handling invalid actions"""
        # Start a game first
        self.app.post('/api/start_game')
        
        # Send invalid action
        response = self.app.post('/api/action', 
                                json={'action': 'invalid', 'event': 'first_encounter', 'choice': 999})
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        # Should still return a valid response structure
        self.assertIn('message', data)
    
    def test_game_state_persistence(self):
        """Test that game state persists across requests"""
        # Start a game
        response1 = self.app.post('/api/start_game')
        data1 = json.loads(response1.data)
        initial_health = data1['player']['health']
        
        # Process an action that might change state
        response2 = self.app.post('/api/action', 
                                 json={'action': 'first_encounter', 'event': 'first_encounter', 'choice': 2})
        self.assertEqual(response2.status_code, 200)
        
        # Check status to verify state persistence
        response3 = self.app.get('/api/status')
        data3 = json.loads(response3.data)
        self.assertIsNotNone(data3.get('player', {}).get('health'))
    
    def test_battle_endpoint(self):
        """Test battle-specific endpoints"""
        # Start a game first
        self.app.post('/api/start_game')
        
        # Start a battle by taking goods and fighting
        response = self.app.post('/api/action', 
                                json={'action': 'first_encounter', 'event': 'first_encounter', 'choice': 3})
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data.get('event'), 'battle')
    
    def test_error_handling(self):
        """Test API error handling"""
        # Test malformed JSON
        response = self.app.post('/api/action', 
                                data='invalid json',
                                content_type='application/json')
        self.assertEqual(response.status_code, 400)
    
    def test_session_management(self):
        """Test session-based game management"""
        with self.app.session_transaction() as sess:
            # Test that sessions work
            sess['test'] = 'value'
        
        # Start game should create session data
        response = self.app.post('/api/start_game')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()