from django.core.cache import cache
from django.http import HttpResponseForbidden
from django.conf import settings
from django_redis import get_redis_connection
from django_redis.exceptions import ConnectionInterrupted
import time
import logging
from functools import wraps

logger = logging.getLogger(__name__)

def handle_redis_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ConnectionInterrupted, Exception) as e:
            logger.error(f"Redis error in {func.__name__}: {str(e)}")
            return None
    return wrapper

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self._local_cache = {}
        
    @handle_redis_error
    def _get_from_redis(self, key):
        return cache.get(key, 0)
        
    @handle_redis_error
    def _set_to_redis(self, key, value, timeout):
        cache.set(key, value, timeout)
        
    def _get_from_local(self, key):
        current_time = time.time()
        if key in self._local_cache:
            count, timestamp = self._local_cache[key]
            if current_time - timestamp < settings.RATE_LIMIT_WINDOW:
                return count
        return 0
        
    def _set_to_local(self, key, value):
        self._local_cache[key] = (value, time.time())
        
    def __call__(self, request):
        # Skip rate limiting for admin and staff users
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
            return self.get_response(request)
        
        # Get client IP
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        
        # Rate limit key
        key = f'ratelimit:{ip}'
        
        # Try Redis first, fall back to local cache if Redis fails
        current = self._get_from_redis(key)
        if current is None:
            current = self._get_from_local(key)
        
        # Check if rate limit exceeded
        if current >= settings.RATE_LIMIT_REQUESTS:
            return HttpResponseForbidden('Rate limit exceeded. Please try again later.')
        
        # Increment request count
        new_count = current + 1
        if not self._set_to_redis(key, new_count, settings.RATE_LIMIT_WINDOW):
            self._set_to_local(key, new_count)
        
        return self.get_response(request) 