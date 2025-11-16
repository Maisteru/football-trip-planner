import requests
from datetime import datetime, timedelta

class HotelAPIService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://booking-com.p.rapidapi.com/v1"
    
    def get_hotel_price(self, city, match_date, nights=2):
        match_datetime = datetime.fromisoformat(match_date.replace('Z', '+00:00'))
        current_year = datetime.now().year
        future_match_datetime = match_datetime.replace(year=current_year)
        checkin = (future_match_datetime - timedelta(days=1)).strftime('%Y-%m-%d')
        checkout = (future_match_datetime + timedelta(days=1)).strftime('%Y-%m-%d')
        
        headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": "booking-com.p.rapidapi.com"
        }
        
        try:
            locations_url = f"{self.base_url}/hotels/locations"
            location_params = {
                "name": city,
                "locale": "en-gb"
            }
            
            location_response = requests.get(locations_url, headers=headers, params=location_params)
            location_response.raise_for_status()
            location_data = location_response.json()
            
            if not location_data:
                price = self._estimate_hotel_price(city, nights)
                link = f"https://www.booking.com/searchresults.html?ss={city}&checkin={checkin}&checkout={checkout}"
                return {'price': price, 'link': link}
            
            dest_id = location_data[0].get('dest_id')
            
            search_url = f"{self.base_url}/hotels/search"
            params = {
                "checkout_date": checkout,
                "units": "metric",
                "dest_id": dest_id,
                "dest_type": "city",
                "locale": "en-gb",
                "adults_number": "1",
                "order_by": "popularity",
                "filter_by_currency": "EUR",
                "checkin_date": checkin,
                "room_number": "1",
                "page_number": "0"
            }
            
            response = requests.get(search_url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get('result'):
                prices = [hotel.get('min_total_price', 0) for hotel in data['result'][:5]]
                prices = [p for p in prices if p > 0]
                if prices:
                    price = min(prices)
                    link = f"https://www.booking.com/searchresults.html?ss={city}&checkin={checkin}&checkout={checkout}"
                    return {'price': price, 'link': link}
        except Exception as e:
            print(f"Error fetching hotel prices: {e}")
        
        price = self._estimate_hotel_price(city, nights)
        link = f"https://www.booking.com/searchresults.html?ss={city}&checkin={checkin}&checkout={checkout}"
        return {'price': price, 'link': link}
    
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