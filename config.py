import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    FOOTBALL_API_KEY = os.getenv('FOOTBALL_API_KEY')
    AMADEUS_API_KEY = os.getenv('AMADEUS_API_KEY')
    AMADEUS_API_SECRET = os.getenv('AMADEUS_API_SECRET')
    BOOKING_API_KEY = os.getenv('BOOKING_API_KEY')