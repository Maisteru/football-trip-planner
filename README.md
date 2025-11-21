DONE:
    1. Base of application code
    2. Unit tests
    3. Integration tests
    4. Contenarization
    5. CI in GitHub workflows


TODO:
    1. Improve credentials safeness
    2.



# ⚽ Football Trip Planner

A Flask web application that helps users plan trips to European football matches by calculating total costs including flights, accommodation, and match tickets.

## Overview

Football Trip Planner integrates with multiple APIs to provide real-time pricing for football match trips across Europe's top 5 leagues. Users can select their favorite team, view upcoming matches, and get instant cost estimates with booking links.

## Features

- **Match Discovery**: Browse upcoming matches from Premier League, La Liga, Serie A, Bundesliga, and Ligue 1
- **Cost Calculator**: Automatic calculation of flights, hotels, and ticket prices
- **Smart Caching**: Database-backed caching system to reduce API calls and improve performance
- **User Authentication**: Secure login system with password hashing
- **Booking Links**: Direct links to flight and hotel booking platforms
- **Responsive Design**: Bootstrap 5 UI with gradient theme

## Project Structure

football-trip-planner/ 
├── app.py # Main Flask application 
├── config.py # Configuration settings 
├── requirements.txt # Python dependencies 
├── Dockerfile # Docker container configuration 
├── docker-compose.yaml # Docker Compose setup │ 
├── auth/ # Authentication module 
│ ├── users.py # User model and password verification │ └── README.md │ 
├── models/ # Database models 
│ ├── cache.py # APICache and RequestLog models 
│ ├── team.py # (Reserved for future use) 
│ ├── match.py # (Reserved for future use) 
│ └── README.md │ 
├── services/ # External API integrations
│ ├── football_api.py # Football API service
│ ├── flight_api.py # Amadeus Flight API service
│ ├── hotel_api.py # Booking.com API service │ 
├──  cached_football_api.py # Cached football service
│ ├── cached_flight_api.py # Cached flight service
│ ├── cached_hotel_api.py # Cached hotel service 
│ ├── calculator.py # Cost calculation logic 
│ └── README.md │ 
├── templates/ # Jinja2 HTML templates │ 
├── index.html # Main application page │ 
├── login.html # Login page 
│ └── README.md │ 
├── static/ # Static assets 
│ │ ├──css/ 
│ │ └── style.css # Custom styles 
│ ├── js/ 
│ │ └── main.js # Client-side JavaScript  
| └── README.md 
├── tests/ #Unit tests 
│ ├── test_app.py # Flask application tests 
│ ├── test_auth.py # Authentication tests
│ ├── test_cache.py # Caching system tests 
│ ├── test_calculator.py # Calculator tests 
│ ├── test_football_api.py # API service tests 
│ └── README.md

## Quick Start

### Prerequisites

- Python 3.8+
- API Keys:
  - API-Sports (Football data)
  - Amadeus (Flight prices)
  - RapidAPI (Hotel prices via Booking.com)

### Installation

```bash
# Clone repository
git clone <repository-url>
cd football-trip-planner

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Run application
python app.py