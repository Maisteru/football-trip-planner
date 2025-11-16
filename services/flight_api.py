import requests
from datetime import datetime, timedelta

class FlightAPIService:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://test.api.amadeus.com/v2"
        self.token = None
        
        self.city_airports = {
            'London': 'LON',
            'Madrid': 'MAD',
            'Barcelona': 'BCN',
            'Rome': 'ROM',
            'Milan': 'MIL',
            'Munich': 'MUC',
            'Berlin': 'BER',
            'Paris': 'PAR',
            'Manchester': 'MAN',
            'Liverpool': 'LPL'
        }
    
    def get_access_token(self):
        url = "https://test.api.amadeus.com/v1/security/oauth2/token"
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.api_key,
            'client_secret': self.api_secret
        }
        
        try:
            response = requests.post(url, data=data)
            response.raise_for_status()
            self.token = response.json()['access_token']
        except Exception as e:
            print(f"Error getting access token: {e}")
    
    def get_flight_price(self, origin_city, destination_city, match_date):
        if not self.token:
            self.get_access_token()
        
        origin_code = self.city_airports.get(origin_city, 'LON')
        destination_code = self.city_airports.get(destination_city, 'MAD')
        
        match_datetime = datetime.fromisoformat(match_date.replace('Z', '+00:00'))
        departure_date = (match_datetime - timedelta(days=1)).strftime('%Y-%m-%d')
        return_date = (match_datetime + timedelta(days=1)).strftime('%Y-%m-%d')
        
        url = f"{self.base_url}/shopping/flight-offers"
        headers = {'Authorization': f'Bearer {self.token}'}
        params = {
            'originLocationCode': origin_code,
            'destinationLocationCode': destination_code,
            'departureDate': departure_date,
            'returnDate': return_date,
            'adults': 1,
            'currencyCode': 'EUR'
        }
        
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get('data'):
                prices = [float(offer['price']['total']) for offer in data['data']]
                return min(prices) if prices else 200
        except Exception as e:
            print(f"Error fetching flight prices: {e}")
        
        return self._estimate_flight_price(origin_city, destination_city)
    
    def _estimate_flight_price(self, origin, destination):
        base_prices = {
            'short': 100,
            'medium': 200,
            'long': 400
        }
        return base_prices['medium']