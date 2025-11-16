import requests
from datetime import datetime, timedelta

class FootballAPIService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://v3.football.api-sports.io"
        self.headers = {
            'x-apisports-key': api_key
        }
        
        self.top_leagues = {
            39: {'name': 'Premier League', 'country': 'England'},
            140: {'name': 'La Liga', 'country': 'Spain'},
            135: {'name': 'Serie A', 'country': 'Italy'},
            78: {'name': 'Bundesliga', 'country': 'Germany'},
            61: {'name': 'Ligue 1', 'country': 'France'}
        }
    
    def get_top_leagues(self):
        return [{'id': k, **v} for k, v in self.top_leagues.items()]
    
    def get_teams_by_league(self, league_id):
        url = f"{self.base_url}/teams"
        params = {
            'league': league_id,
            'season': 2023
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            teams = []
            for team in data.get('response', []):
                teams.append({
                    'id': team['team']['id'],
                    'name': team['team']['name'],
                    'logo': team['team']['logo'],
                    'city': team['venue']['city']
                })
            return teams
        except Exception as e:
            print(f"Error fetching teams: {e}")
            return []
    
    def get_upcoming_matches(self, team_id, match_type='all'):
        url = f"{self.base_url}/fixtures"
        
        today = datetime.now()
        today_2023 = today.replace(year=2023).strftime('%Y-%m-%d')
        future_2023 = (today.replace(year=2023) + timedelta(days=90)).strftime('%Y-%m-%d')
        
        params = {
            'team': team_id,
            'from': today_2023,
            'to': future_2023,
            'status': 'FT'
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            matches = []
            for fixture in data.get('response', []):
                is_home = fixture['teams']['home']['id'] == team_id
                
                if match_type == 'home' and not is_home:
                    continue
                if match_type == 'away' and is_home:
                    continue
                
                matches.append({
                    'id': fixture['fixture']['id'],
                    'date': fixture['fixture']['date'],
                    'home_team': fixture['teams']['home']['name'],
                    'away_team': fixture['teams']['away']['name'],
                    'venue': fixture['fixture']['venue']['name'],
                    'city': fixture['fixture']['venue']['city'],
                    'is_home': is_home
                })
            
            return matches
        except Exception as e:
            print(f"Error fetching matches: {e}")
            return []
    
    def get_match_details(self, match_id):
        url = f"{self.base_url}/fixtures"
        params = {'id': match_id}
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get('response'):
                fixture = data['response'][0]
                return {
                    'id': fixture['fixture']['id'],
                    'date': fixture['fixture']['date'],
                    'home_team': fixture['teams']['home']['name'],
                    'away_team': fixture['teams']['away']['name'],
                    'venue': fixture['fixture']['venue']['name'],
                    'city': fixture['fixture']['venue']['city'],
                    'league': fixture['league']['name']
                }
        except Exception as e:
            print(f"Error fetching match details: {e}")
        
        return None