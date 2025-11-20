import json
from services.flight_api import FlightAPIService
from models.cache import APICache

class CachedFlightAPIService(FlightAPIService):
    def __init__(self, api_key, api_secret):
        super().__init__(api_key, api_secret)
        self.cache_enabled = True
    
    def get_flight_price(self, origin, destination, date):
        cache_key = f"flight_{origin}_{destination}_{date}"
        
        if self.cache_enabled:
            cached = APICache.get_cached(cache_key)
            if cached:
                return json.loads(cached)
        
        flight_data = super().get_flight_price(origin, destination, date)
        
        if self.cache_enabled and flight_data:
            APICache.set_cache(cache_key, 'flight', json.dumps(flight_data), ttl_hours=6)
        
        return flight_data