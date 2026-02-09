#!/usr/bin/env python3
"""
API Caching Layer
"""

import time
from typing import Any, Optional, Dict
from collections import OrderedDict
import threading


class APICache:
    """
    Thread-safe LRU cache with TTL support for API responses
    """
    
    def __init__(self, maxsize: int = 500, ttl: int = 3600):
        """
        Initialize cache
        
        Args:
            maxsize: Maximum number of cache entries
            ttl: Time-to-live in seconds (default: 1 hour)
        """
        self.maxsize = maxsize
        self.ttl = ttl
        self.cache = OrderedDict()
        self.lock = threading.Lock()
        self.hits = 0
        self.misses = 0
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found/expired
        """
        with self.lock:
            if key not in self.cache:
                self.misses += 1
                return None
            
            value, timestamp = self.cache[key]
            
            # Check if expired
            if time.time() - timestamp > self.ttl:
                del self.cache[key]
                self.misses += 1
                return None
            
            # Move to end (most recently used)
            self.cache.move_to_end(key)
            self.hits += 1
            return value
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """
        Set value in cache
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Optional custom TTL for this entry
        """
        with self.lock:
            # Remove oldest entry if at capacity
            if len(self.cache) >= self.maxsize and key not in self.cache:
                self.cache.popitem(last=False)
            
            # Use custom TTL or default
            entry_ttl = ttl if ttl is not None else self.ttl
            self.cache[key] = (value, time.time())
    
    def clear(self):
        """Clear all cache entries"""
        with self.lock:
            self.cache.clear()
            self.hits = 0
            self.misses = 0
    
    def get_stats(self) -> Dict:
        """
        Get cache statistics
        
        Returns:
            Dict with hits, misses, size, hit_rate
        """
        with self.lock:
            total = self.hits + self.misses
            hit_rate = self.hits / total if total > 0 else 0.0
            
            return {
                'hits': self.hits,
                'misses': self.misses,
                'size': len(self.cache),
                'maxsize': self.maxsize,
                'hit_rate': round(hit_rate, 3)
            }
    
    def cleanup_expired(self):
        """Remove expired entries from cache"""
        with self.lock:
            current_time = time.time()
            expired_keys = [
                key for key, (value, timestamp) in self.cache.items()
                if current_time - timestamp > self.ttl
            ]
            
            for key in expired_keys:
                del self.cache[key]
            
            return len(expired_keys)


# Example usage
if __name__ == "__main__":
    cache = APICache(maxsize=100, ttl=10)
    
    # Test set/get
    cache.set("test_key", {"data": "value"})
    result = cache.get("test_key")
    print(f"Cached value: {result}")
    
    # Test expiration
    cache.set("expire_key", "will_expire", ttl=1)
    print(f"Before expiry: {cache.get('expire_key')}")
    time.sleep(2)
    print(f"After expiry: {cache.get('expire_key')}")
    
    # Test stats
    stats = cache.get_stats()
    print(f"Cache stats: {stats}")
