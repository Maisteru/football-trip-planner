import unittest
from unittest.mock import Mock, patch
from services.football_api import FootballAPIService


class TestFootballAPIService(unittest.TestCase):
    def setUp(self):
        self.api_service = FootballAPIService('test_api_key')
    
    def test_get_top_leagues(self):
        leagues = self.api_service.get_top_leagues()
        self.assertEqual(len(leagues), 5)
        self.assertIn('name', leagues[0])
        self.assertIn('country', leagues[0])
    
    @patch('services.football_api.requests.get')
    def test_get_teams_by_league_success(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {
            'response': [
                {
                    'team': {'id': 1, 'name': 'Test Team', 'logo': 'logo.png'},
                    'venue': {'city': 'Test City'}
                }
            ]
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        teams = self.api_service.get_teams_by_league(39)
        self.assertEqual(len(teams), 1)
        self.assertEqual(teams[0]['name'], 'Test Team')
    
    @patch('services.football_api.requests.get')
    def test_get_teams_by_league_error(self, mock_get):
        mock_get.side_effect = Exception('API Error')
        teams = self.api_service.get_teams_by_league(39)
        self.assertEqual(teams, [])
    
    @patch('services.football_api.requests.get')
    def test_get_upcoming_matches_success(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {
            'response': [
                {
                    'fixture': {
                        'id': 1,
                        'date': '2023-12-01',
                        'venue': {'name': 'Stadium', 'city': 'City'}
                    },
                    'teams': {
                        'home': {'id': 100, 'name': 'Home Team'},
                        'away': {'id': 200, 'name': 'Away Team'}
                    }
                }
            ]
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        matches = self.api_service.get_upcoming_matches(100)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]['home_team'], 'Home Team')
        self.assertTrue(matches[0]['is_home'])
    
    @patch('services.football_api.requests.get')
    def test_get_upcoming_matches_filter_home(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {
            'response': [
                {
                    'fixture': {
                        'id': 1,
                        'date': '2023-12-01',
                        'venue': {'name': 'Stadium', 'city': 'City'}
                    },
                    'teams': {
                        'home': {'id': 100, 'name': 'Home Team'},
                        'away': {'id': 200, 'name': 'Away Team'}
                    }
                }
            ]
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        matches = self.api_service.get_upcoming_matches(200, match_type='home')
        self.assertEqual(len(matches), 0)


if __name__ == '__main__':
    unittest.main()