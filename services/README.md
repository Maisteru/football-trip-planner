# Services

This folder contains service classes that handle external API integrations and business logic for the Football Trip Planner application.

## Overview

The services are organized into three main categories:
- **API Services**: Direct integrations with external APIs (Football, Flight, Hotel)
- **Cached Services**: Wrapper services that add caching functionality to API services
- **Utility Services**: Helper services for calculations and business logic

## Services

### FootballAPIService (`football_api.py`)

Integrates with the API-Sports Football API to fetch football match data.

**Key Methods:**
- `get_top_leagues()` - Returns list of top European leagues (Premier League, La Liga, Serie A, Bundesliga, Ligue 1)
- `get_teams_by_league(league_id)` - Fetches all teams in a specific league
- `get_upcoming_matches(team_id, match_type='all')` - Gets upcoming matches for a team (home/away/all)
- `get_match_details(match_id)` - Retrieves detailed information about a specific match

**API:** https://v3.football.api-sports.io

### FlightAPIService (`flight_api.py`)

Integrates with the Amadeus Flight API to fetch flight prices and availability.

**Key Methods:**
- `get_access_token()` - Authenticates with Amadeus API using OAuth2
- `get_flight_price(origin_city, destination_city, match_date)` - Fetches flight prices for round trips
- `_estimate_flight_price(origin, destination)` - Provides fallback price estimates

**Features:**
- Supports major European city airports
- Calculates departure (day before match) and return (day after match) dates
- Returns price and booking link

**API:** https://test.api.amadeus.com/v2

### HotelAPIService (`hotel_api.py`)

Integrates with the Booking.com API via RapidAPI to fetch hotel prices.

**Key Methods:**
- `get_hotel_price(city, match_date, nights=2)` - Fetches hotel prices for match dates
- `_estimate_hotel_price(city, nights=2)` - Provides fallback price estimates for major cities

**Features:**
- Searches for hotels in match city
- Calculates check-in (day before match) and check-out (day after match) dates
- Returns minimum price from top 5 hotels and booking link
- Fallback estimates for 10 major European cities

**API:** https://booking-com.p.rapidapi.com/v1

### CostCalculator (`calculator.py`)

Calculates estimated ticket prices and total trip costs.

**Key Methods:**
- `estimate_ticket_price(league, home_team, away_team)` - Estimates match ticket price based on league and teams
- `calculate_total(flight, hotel, ticket)` - Calculates total trip cost

**Features:**
- League-specific pricing tiers (top/mid/low)
- Premium pricing for matches involving top teams
- Covers all 5 major European leagues

### Cached Services

Wrapper services that add caching functionality to reduce API calls and improve performance.

#### CachedFootballAPIService (`cached_football_api.py`)
- Extends `FootballAPIService`
- Cache TTL: 168 hours (7 days) for teams, 24 hours for matches
- Cache keys: `teams_league_{id}`, `matches_{team_id}_{type}`, `match_details_{id}`

#### CachedFlightAPIService (`cached_flight_api.py`)
- Extends `FlightAPIService`
- Cache TTL: 6 hours
- Cache key: `flight_{origin}_{destination}_{date}`

#### CachedHotelAPIService (`cached_hotel_api.py`)
- Extends `HotelAPIService`
- Cache TTL: 6 hours
- Cache key: `hotel_{city}_{date}`

**Caching Features:**
- All cached services use the `APICache` model for storage
- Cache can be enabled/disabled via `cache_enabled` flag
- Automatic cache invalidation based on TTL

**API Keys Required:**
- Football API: API-Sports key (https://www.api-football.com/)
- Flight API: Amadeus API key and secret (https://developers.amadeus.com/)
- Hotel API: RapidAPI key for Booking.com API (https://rapidapi.com/)