import unittest
import json
from unittest.mock import patch, Mock
from app import app


class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_health_check(self):
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
    
    @patch('app.football_api')
    def test_get_leagues(self, mock_api):
        mock_api.get_top_leagues.return_value = [
            {'id': 39, 'name': 'Premier League', 'country': 'England'}
        ]
        
        response = self.client.get('/api/leagues')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
    
    @patch('app.football_api')
    def test_get_teams(self, mock_api):
        mock_api.get_teams_by_league.return_value = [
            {'id': 1, 'name': 'Test Team', 'logo': 'logo.png', 'city': 'City'}
        ]
        
        response = self.client.get('/api/teams/39')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
    
    def test_calculate_cost(self):
        payload = {
            'league': 'Premier League',
            'home_team': 'Manchester City',
            'away_team': 'Liverpool',
            'flight_cost': 200,
            'hotel_cost': 150
        }
        
        response = self.client.post('/api/calculate',
                                   data=json.dumps(payload),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('ticket_price', data)
        self.assertIn('total_cost', data)


if __name__ == '__main__':
    unittest.main()