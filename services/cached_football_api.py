import json
from services.football_api import FootballAPIService
from models.cache import APICache

class CachedFootballAPIService(FootballAPIService):
    def __init__(self, api_key):
        super().__init__(api_key)
        self.cache_enabled = True
    
    def get_teams_by_league(self, league_id):
        cache_key = f"teams_league_{league_id}"
        
        if self.cache_enabled:
            cached = APICache.get_cached(cache_key)
            if cached:
                return json.loads(cached)
        
        teams = super().get_teams_by_league(league_id)
        
        if self.cache_enabled and teams:
            APICache.set_cache(cache_key, 'teams', json.dumps(teams), ttl_hours=168)
        
        return teams
    
    def get_upcoming_matches(self, team_id, match_type='all'):
        cache_key = f"matches_{team_id}_{match_type}"
        
        if self.cache_enabled:
            cached = APICache.get_cached(cache_key)
            if cached:
                return json.loads(cached)
        
        matches = super().get_upcoming_matches(team_id, match_type)
        
        if self.cache_enabled and matches:
            APICache.set_cache(cache_key, 'matches', json.dumps(matches), ttl_hours=24)
        
        return matches
    
    def get_match_details(self, match_id):
        cache_key = f"match_details_{match_id}"
        
        if self.cache_enabled:
            cached = APICache.get_cached(cache_key)
            if cached:
                return json.loads(cached)
        
        match_details = super().get_match_details(match_id)
        
        if self.cache_enabled and match_details:
            APICache.set_cache(cache_key, 'match_details', json.dumps(match_details), ttl_hours=24)
        
        return match_details