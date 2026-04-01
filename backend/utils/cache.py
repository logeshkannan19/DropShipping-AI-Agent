"""Caching utilities with optional Redis support."""

import json
import hashlib
from typing import Any, Callable, Optional, TypeVar
from functools import wraps
from datetime import datetime, timedelta
import pickle
from pathlib import Path
import asyncio

from backend.config import get_config

T = TypeVar("T")


class InMemoryCache:
    """Simple in-memory cache implementation."""
    
    def __init__(self):
        self._cache: dict = {}
        self._expiry: dict = {}
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        if key in self._cache:
            if key in self._expiry and datetime.now() > self._expiry[key]:
                del self._cache[key]
                del self._expiry[key]
                return None
            return self._cache[key]
        return None
    
    def set(self, key: str, value: Any, ttl: int = 3600):
        """Set value in cache with TTL in seconds."""
        self._cache[key] = value
        if ttl > 0:
            self._expiry[key] = datetime.now() + timedelta(seconds=ttl)
    
    def delete(self, key: str):
        """Delete value from cache."""
        self._cache.pop(key, None)
        self._expiry.pop(key, None)
    
    def clear(self):
        """Clear all cache."""
        self._cache.clear()
        self._expiry.clear()
    
    def keys(self) -> list:
        """Get all cache keys."""
        return list(self._cache.keys())


class RedisCache:
    """Redis cache implementation."""
    
    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0, ttl: int = 3600):
        self.host = host
        self.port = port
        self.db = db
        self.default_ttl = ttl
        self._client = None
        self._connect()
    
    def _connect(self):
        """Connect to Redis server."""
        try:
            import redis
            self._client = redis.Redis(
                host=self.host,
                port=self.port,
                db=self.db,
                decode_responses=False
            )
            self._client.ping()
        except Exception as e:
            self._client = None
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from Redis cache."""
        if not self._client:
            return None
        try:
            value = self._client.get(key)
            if value:
                return pickle.loads(value)
        except Exception:
            pass
        return None
    
    def set(self, key: str, value: Any, ttl: int = None):
        """Set value in Redis cache."""
        if not self._client:
            return
        try:
            ttl = ttl or self.default_ttl
            self._client.setex(key, ttl, pickle.dumps(value))
        except Exception:
            pass
    
    def delete(self, key: str):
        """Delete value from Redis cache."""
        if not self._client:
            return
        try:
            self._client.delete(key)
        except Exception:
            pass
    
    def clear(self):
        """Clear all cache."""
        if not self._client:
            return
        try:
            self._client.flushdb()
        except Exception:
            pass


class CacheManager:
    """Unified cache manager that can use Redis or in-memory cache."""
    
    def __init__(self, use_redis: bool = False, redis_config: dict = None):
        if use_redis and redis_config:
            self.cache = RedisCache(**redis_config)
        else:
            self.cache = InMemoryCache()
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        return self.cache.get(key)
    
    def set(self, key: str, value: Any, ttl: int = 3600):
        """Set value in cache."""
        self.cache.set(key, value, ttl)
    
    def delete(self, key: str):
        """Delete value from cache."""
        self.cache.delete(key)
    
    def clear(self):
        """Clear all cache."""
        self.cache.clear()


def generate_cache_key(*args, **kwargs) -> str:
    """Generate a cache key from arguments."""
    key_data = json.dumps({"args": args, "kwargs": kwargs}, sort_keys=True, default=str)
    return hashlib.md5(key_data.encode()).hexdigest()


def cached(ttl: int = 3600, key_prefix: str = ""):
    """
    Decorator to cache function results.
    
    Args:
        ttl: Time to live in seconds
        key_prefix: Prefix for cache key
    """
    config = get_config()
    cache = CacheManager(
        use_redis=config.redis.enabled,
        redis_config={
            "host": config.redis.host,
            "port": config.redis.port,
            "db": config.redis.db,
            "ttl": config.redis.ttl
        }
    )
    
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            cache_key = f"{key_prefix}:{func.__name__}:{generate_cache_key(*args, **kwargs)}"
            
            cached_value = cache.get(cache_key)
            if cached_value is not None:
                return cached_value
            
            result = func(*args, **kwargs)
            cache.set(cache_key, result, ttl)
            return result
        
        @wraps(func)
        async def async_wrapper(*args, **kwargs) -> T:
            cache_key = f"{key_prefix}:{func.__name__}:{generate_cache_key(*args, **kwargs)}"
            
            cached_value = cache.get(cache_key)
            if cached_value is not None:
                return cached_value
            
            result = await func(*args, **kwargs)
            cache.set(cache_key, result, ttl)
            return result
        
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return wrapper
    
    return decorator
