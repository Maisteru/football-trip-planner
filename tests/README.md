# Tests

Unit tests for the Football Trip Planner application using Python's `unittest` framework.

## Overview

Comprehensive test suite covering authentication, API services, caching, cost calculations, and Flask application routes.

## Test Files

### test_auth.py
**Authentication & User Management Tests**
- User database existence and password hashing
- Password verification (correct/incorrect/nonexistent users)
- User retrieval and attributes (is_authenticated, is_active, is_anonymous)
- User ID generation

### test_app.py
**Flask Application & Route Tests**
- Login/logout functionality
- Authentication requirements for protected routes
- API endpoints (/api/leagues, /api/teams, /api/matches, /api/calculate-trip)
- Request validation and error handling
- Integration with mocked services

### test_cache.py
**Caching System Tests**
- **APICache**: Set/get cache, expiration handling, cache updates
- **RequestLog**: Logging API requests, retrieving logs by type/date
- **CachedServices**: Football/Flight/Hotel API caching behavior

### test_calculator.py
**Cost Calculator Tests**
- Ticket price estimation (top/mid/low tier teams)
- League-specific pricing
- Total cost calculation

### test_football_api.py
**Football API Service Tests**
- Top leagues retrieval
- Teams by league (success/error scenarios)
- Upcoming matches (success/error scenarios)
- API response parsing with mocked requests

## Running Tests

```bash
# Run all tests
python -m unittest discover tests

# Run specific test file
python -m unittest tests.test_auth
python -m unittest tests.test_app
python -m unittest tests.test_cache
python -m unittest tests.test_calculator
python -m unittest tests.test_football_api

# Run with verbose output
python -m unittest discover tests -v