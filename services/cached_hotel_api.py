import json
from services.hotel_api import HotelAPIService
from models.cache import APICache

class CachedHotelAPIService(HotelAPIService):
    def __init__(self, api_key):
        super().__init__(api_key)
        self.cache_enabled = True
    
    def get_hotel_price(self, city, date):
        cache_key = f"hotel_{city}_{date}"
        
        if self.cache_enabled:
            cached = APICache.get_cached(cache_key)
            if cached:
                return json.loads(cached)
        
        hotel_data = super().get_hotel_price(city, date)
        
        if self.cache_enabled and hotel_data:
            APICache.set_cache(cache_key, 'hotel', json.dumps(hotel_data), ttl_hours=6)
        
        return hotel_data