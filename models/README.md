# Models

Database models for the Football Trip Planner application using SQLAlchemy ORM.

## Overview

The models folder contains SQLAlchemy database models for caching API responses and logging requests. Currently implements two active models for performance optimization and analytics.

## Models

### APICache (`cache.py`)

Stores cached API responses with automatic expiration management.

**Table:** `api_cache`

**Columns:**
- `id` (Integer, Primary Key): Auto-incrementing identifier
- `cache_key` (String(500), Unique, Indexed): Unique cache identifier
- `cache_type` (String(50)): Type of cached data (teams/matches/flight/hotel)
- `response_data` (Text): Serialized JSON response data
- `created_at` (DateTime): Cache creation timestamp (UTC)
- `expires_at` (DateTime): Cache expiration timestamp (UTC)

**Methods:**

#### `get_cached(cache_key)` (static)
Retrieves cached data if valid, auto-deletes if expired.

```python
data = APICache.get_cached('teams_league_39')
