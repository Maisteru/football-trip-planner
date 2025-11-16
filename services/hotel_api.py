import requests
from datetime import datetime, timedelta

class HotelAPIService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://booking-com.p.rapidapi.com/v1"
    
    def get_hotel_price(self, city, match_date, nights=2):
        match_datetime = datetime.fromisoformat(match_date.replace('Z', '+00:00'))
        checkin = (match_datetime - timedelta(days=1)).strftime('%Y-%m-%d')
        checkout = (match_datetime + timedelta(days=1)).strftime('%Y-%m-%d')
        
        return self._estimate_hotel_price(city, nights)
    
    def _estimate_hotel_price(self, city, nights=2):
        city_prices = {
            'London': 150,
            'Madrid': 100,
            'Barcelona': 120,
            'Rome': 110,
            'Milan': 130,
            'Munich': 120,
            'Berlin': 100,
            'Paris': 140,
            'Manchester': 90,
            'Liverpool': 85
        }
        
        base_price = city_prices.get(city, 100)
        return base_price * nights