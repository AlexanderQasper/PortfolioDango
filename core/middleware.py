from django.core.cache import cache
from django.http import HttpResponseForbidden
from django.conf import settings
import time

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
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
        
        # Get current request count
        current = cache.get(key, 0)
        
        # Check if rate limit exceeded
        if current >= settings.RATE_LIMIT_REQUESTS:
            return HttpResponseForbidden('Rate limit exceeded. Please try again later.')
        
        # Increment request count
        cache.set(key, current + 1, settings.RATE_LIMIT_WINDOW)
        
        return self.get_response(request) 