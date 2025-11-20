import unittest
import json
from unittest.mock import patch, Mock
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, football_service, calculator
from flask_login import login_user
from auth.users import User


class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['LOGIN_DISABLED'] = False
        self.client = self.app.test_client()
    
    def login(self, username='admin', password='admin123'):
        return self.client.post('/login', data={
            'username': username,
            'password': password
        }, follow_redirects=True)
    
    def test_login_page_loads(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login to Continue', response.data)
    
    def test_login_success(self):
        response = self.login('admin', 'admin123')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Football Trip Planner', response.data)
    
    def test_login_invalid_credentials(self):
        response = self.login('admin', 'wrongpassword')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid username or password', response.data)
    
    def test_login_nonexistent_user(self):
        response = self.login('nonexistent', 'password')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid username or password', response.data)
    
    def test_logout(self):
        self.login()
        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login to Continue', response.data)
    
    def test_index_requires_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.location)
    
    def test_index_with_login(self):
        self.login()
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Football Trip Planner', response.data)
    
    @patch('app.football_service')
    def test_get_leagues_requires_login(self, mock_service):
        response = self.client.get('/api/leagues')
        self.assertEqual(response.status_code, 302)
    
    @patch('app.football_service')
    def test_get_leagues_with_login(self, mock_service):
        mock_service.get_top_leagues.return_value = [
            {'id': 39, 'name': 'Premier League', 'country': 'England'}
        ]
        
        self.login()
        response = self.client.get('/api/leagues')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
    
    @patch('app.football_service')
    def test_get_teams_requires_login(self, mock_service):
        response = self.client.get('/api/teams/39')
        self.assertEqual(response.status_code, 302)
    
    @patch('app.football_service')
    def test_get_teams_with_login(self, mock_service):
        mock_service.get_teams_by_league.return_value = [
            {'id': 1, 'name': 'Test Team', 'logo': 'logo.png', 'city': 'City'}
        ]
        
        self.login()
        response = self.client.get('/api/teams/39')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
    
    @patch('app.football_service')
    def test_get_matches_requires_login(self, mock_service):
        payload = {'team_id': 100, 'match_type': 'all'}
        response = self.client.post('/api/matches',
                                   data=json.dumps(payload),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 302)
    
    @patch('app.football_service')
    def test_get_matches_with_login(self, mock_service):
        mock_service.get_upcoming_matches.return_value = [
            {'id': 1, 'date': '2023-12-01', 'home_team': 'Team A', 'away_team': 'Team B'}
        ]
        
        self.login()
        payload = {'team_id': 100, 'match_type': 'all'}
        response = self.client.post('/api/matches',
                                   data=json.dumps(payload),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
    
    @patch('app.hotel_service')
    @patch('app.flight_service')
    @patch('app.football_service')
    @patch('app.calculator')
    def test_calculate_trip_requires_login(self, mock_calc, mock_football, mock_flight, mock_hotel):
        payload = {'match_id': 1, 'origin_city': 'London'}
        response = self.client.post('/api/calculate-trip',
                                   data=json.dumps(payload),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 302)
    
    @patch('app.hotel_service')
    @patch('app.flight_service')
    @patch('app.football_service')
    @patch('app.calculator')
    def test_calculate_trip_with_login(self, mock_calc, mock_football, mock_flight, mock_hotel):
        mock_football.get_match_details.return_value = {
            'league': 'Premier League',
            'home_team': 'Manchester City',
            'away_team': 'Liverpool',
            'city': 'Manchester',
            'date': '2023-12-01'
        }
        mock_flight.get_flight_price.return_value = {'price': 200, 'link': 'http://flight.com'}
        mock_hotel.get_hotel_price.return_value = {'price': 150, 'link': 'http://hotel.com'}
        mock_calc.estimate_ticket_price.return_value = 80
        mock_calc.calculate_total.return_value = 430
        
        self.login()
        payload = {'match_id': 1, 'origin_city': 'London'}
        response = self.client.post('/api/calculate-trip',
                                   data=json.dumps(payload),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('match', data)
        self.assertIn('costs', data)


if __name__ == '__main__':
    unittest.main()