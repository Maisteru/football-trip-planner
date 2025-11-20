from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class APICache(db.Model):
    __tablename__ = 'api_cache'
    
    id = db.Column(db.Integer, primary_key=True)
    cache_key = db.Column(db.String(500), unique=True, nullable=False, index=True)
    cache_type = db.Column(db.String(50), nullable=False)
    response_data = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    
    @staticmethod
    def get_cached(cache_key):
        cached = APICache.query.filter_by(cache_key=cache_key).first()
        if cached and cached.expires_at > datetime.utcnow():
            return cached.response_data
        elif cached:
            db.session.delete(cached)
            db.session.commit()
        return None
    
    @staticmethod
    def set_cache(cache_key, cache_type, response_data, ttl_hours=24):
        existing = APICache.query.filter_by(cache_key=cache_key).first()
        if existing:
            existing.response_data = response_data
            existing.expires_at = datetime.utcnow() + timedelta(hours=ttl_hours)
            existing.created_at = datetime.utcnow()
        else:
            cache_entry = APICache(
                cache_key=cache_key,
                cache_type=cache_type,
                response_data=response_data,
                expires_at=datetime.utcnow() + timedelta(hours=ttl_hours)
            )
            db.session.add(cache_entry)
        db.session.commit()
    
    @staticmethod
    def clear_expired():
        expired = APICache.query.filter(APICache.expires_at < datetime.utcnow()).all()
        for entry in expired:
            db.session.delete(entry)
        db.session.commit()
        return len(expired)
    
    @staticmethod
    def clear_all():
        count = APICache.query.delete()
        db.session.commit()
        return count


class RequestLog(db.Model):
    __tablename__ = 'request_log'
    
    id = db.Column(db.Integer, primary_key=True)
    endpoint = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(100))
    cache_hit = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    @staticmethod
    def log_request(endpoint, username=None, cache_hit=False):
        log = RequestLog(endpoint=endpoint, username=username, cache_hit=cache_hit)
        db.session.add(log)
        db.session.commit()
    
    @staticmethod
    def get_stats():
        total = RequestLog.query.count()
        cache_hits = RequestLog.query.filter_by(cache_hit=True).count()
        cache_rate = (cache_hits / total * 100) if total > 0 else 0
        return {
            'total_requests': total,
            'cache_hits': cache_hits,
            'cache_misses': total - cache_hits,
            'cache_hit_rate': round(cache_rate, 2)
        }