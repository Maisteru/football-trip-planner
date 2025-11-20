import unittest
import json
import sys
import os
from datetime import datetime, timedelta
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from models.cache import db, APICache, RequestLog


class TestCache(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_set_cache(self):
        APICache.set_cache('test_key', 'test_type', 'test_data', ttl_hours=1)
        cached = APICache.query.filter_by(cache_key='test_key').first()
        self.assertIsNotNone(cached)
        self.assertEqual(cached.cache_type, 'test_type')
        self.assertEqual(cached.response_data, 'test_data')
    
    def test_get_cached_valid(self):
        APICache.set_cache('test_key', 'test_type', 'test_data', ttl_hours=1)
        result = APICache.get_cached('test_key')
        self.assertEqual(result, 'test_data')
    
    def test_get_cached_expired(self):
        cache_entry = APICache(
            cache_key='expired_key',
            cache_type='test',
            response_data='old_data',
            expires_at=datetime.utcnow() - timedelta(hours=1)
        )
        db.session.add(cache_entry)
        db.session.commit()
        
        result = APICache.get_cached('expired_key')
        self.assertIsNone(result)
        
        cached = APICache.query.filter_by(cache_key='expired_key').first()
        self.assertIsNone(cached)
    
    def test_get_cached_not_exists(self):
        result = APICache.get_cached('nonexistent_key')
        self.assertIsNone(result)
    
    def test_update_existing_cache(self):
        APICache.set_cache('test_key', 'test_type', 'old_data', ttl_hours=1)
        APICache.set_cache('test_key', 'test_type', 'new_data', ttl_hours=2)
        
        result = APICache.get_cached('test_key')
        self.assertEqual(result, 'new_data')
        
        count = APICache.query.filter_by(cache_key='test_key').count()
        self.assertEqual(count, 1)
    
    def test_clear_expired(self):
        APICache.set_cache('valid_key', 'test', 'valid_data', ttl_hours=1)
        
        expired_entry = APICache(
            cache_key='expired_key',
            cache_type='test',
            response_data='expired_data',
            expires_at=datetime.utcnow() - timedelta(hours=1)
        )
        db.session.add(expired_entry)
        db.session.commit()
        
        count = APICache.clear_expired()
        self.assertEqual(count, 1)
        
        self.assertIsNone(APICache.query.filter_by(cache_key='expired_key').first())
        self.assertIsNotNone(APICache.query.filter_by(cache_key='valid_key').first())
    
    def test_clear_all(self):
        APICache.set_cache('key1', 'test', 'data1', ttl_hours=1)
        APICache.set_cache('key2', 'test', 'data2', ttl_hours=1)
        APICache.set_cache('key3', 'test', 'data3', ttl_hours=1)
        
        count = APICache.clear_all()
        self.assertEqual(count, 3)
        
        total = APICache.query.count()
        self.assertEqual(total, 0)
    
    def test_cache_with_json_data(self):
        data = {'teams': [{'id': 1, 'name': 'Team A'}]}
        json_data = json.dumps(data)
        
        APICache.set_cache('teams_key', 'teams', json_data, ttl_hours=24)
        result = APICache.get_cached('teams_key')
        
        self.assertEqual(result, json_data)
        parsed = json.loads(result)
        self.assertEqual(parsed['teams'][0]['name'], 'Team A')


class TestRequestLog(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_log_request(self):
        RequestLog.log_request('/api/leagues', 'admin', cache_hit=False)
        log = RequestLog.query.first()
        
        self.assertIsNotNone(log)
        self.assertEqual(log.endpoint, '/api/leagues')
        self.assertEqual(log.username, 'admin')
        self.assertFalse(log.cache_hit)
    
    def test_log_request_without_username(self):
        RequestLog.log_request('/api/teams/39')
        log = RequestLog.query.first()
        
        self.assertIsNotNone(log)
        self.assertIsNone(log.username)
    
    def test_get_stats_empty(self):
        stats = RequestLog.get_stats()
        
        self.assertEqual(stats['total_requests'], 0)
        self.assertEqual(stats['cache_hits'], 0)
        self.assertEqual(stats['cache_misses'], 0)
        self.assertEqual(stats['cache_hit_rate'], 0)
    
    def test_get_stats_with_data(self):
        RequestLog.log_request('/api/leagues', 'admin', cache_hit=True)
        RequestLog.log_request('/api/teams/39', 'admin', cache_hit=True)
        RequestLog.log_request('/api/matches', 'admin', cache_hit=False)
        RequestLog.log_request('/api/calculate-trip', 'user', cache_hit=False)
        
        stats = RequestLog.get_stats()
        
        self.assertEqual(stats['total_requests'], 4)
        self.assertEqual(stats['cache_hits'], 2)
        self.assertEqual(stats['cache_misses'], 2)
        self.assertEqual(stats['cache_hit_rate'], 50.0)
    
    def test_get_stats_all_cache_hits(self):
        RequestLog.log_request('/api/leagues', 'admin', cache_hit=True)
        RequestLog.log_request('/api/teams/39', 'admin', cache_hit=True)
        
        stats = RequestLog.get_stats()
        
        self.assertEqual(stats['total_requests'], 2)
        self.assertEqual(stats['cache_hits'], 2)
        self.assertEqual(stats['cache_misses'], 0)
        self.assertEqual(stats['cache_hit_rate'], 100.0)
    
    def test_multiple_users_logging(self):
        RequestLog.log_request('/api/leagues', 'admin', cache_hit=True)
        RequestLog.log_request('/api/leagues', 'user', cache_hit=False)
        RequestLog.log_request('/api/teams/39', 'admin', cache_hit=True)
        
        total = RequestLog.query.count()
        self.assertEqual(total, 3)
        
        admin_logs = RequestLog.query.filter_by(username='admin').count()
        self.assertEqual(admin_logs, 2)


class TestCachedServices(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_cache_key_uniqueness(self):
        APICache.set_cache('teams_39', 'teams', '["team1"]', ttl_hours=24)
        APICache.set_cache('teams_140', 'teams', '["team2"]', ttl_hours=24)
        
        result1 = APICache.get_cached('teams_39')
        result2 = APICache.get_cached('teams_140')
        
        self.assertEqual(result1, '["team1"]')
        self.assertEqual(result2, '["team2"]')
    
    def test_cache_ttl_different_values(self):
        APICache.set_cache('short_ttl', 'test', 'data1', ttl_hours=1)
        APICache.set_cache('long_ttl', 'test', 'data2', ttl_hours=168)
        
        short = APICache.query.filter_by(cache_key='short_ttl').first()
        long = APICache.query.filter_by(cache_key='long_ttl').first()
        
        time_diff = (long.expires_at - short.expires_at).total_seconds() / 3600
        self.assertAlmostEqual(time_diff, 167, delta=1)


if __name__ == '__main__':
    unittest.main()