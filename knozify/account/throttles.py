import time

from django.core.cache import cache
from rest_framework.throttling import BaseThrottle


class LoginRateThrottle(BaseThrottle):
    """
    ### Login attempt rate limiting:
    - First 5 (extra) attempts: no delay
    - After 5 attempts: 60 second break
    - Next 3 attempts: continuous
    - After 8 attempts: 5 minute break
    - After 11 attempts: 10 minute break
    - After 12 attempts: 1 hour break
    - After 13 attempts: 24 hour break
    """
    scope = 'login_scope'

    def get_cache_key(self, request, view):
        ident = self.get_ident(request)
        return f'login_attempt_{ident}'
    
    def allow_request(self, request, view):
        if request.method != "POST":
            return True
        
        key = self.get_cache_key(request, view)
        attempts = cache.get(key, 0)
        key_la = f"{key}_last_attempt"
        key_user_la = f"{key}_attempt_left"
        current_time = int(time.time())
        last_attempt = cache.get(key_la, 0)

        if attempts == 0:
            cache.set(key, 1, 86400)
            cache.set(key_la, current_time, 86400)
            cache.set(key_user_la, 5, 86400)
            return True


        if attempts < 5:
            cache.set(key, attempts + 1, 86400)
            cache.set(key_la, current_time, 86400)
            cache.set(key_user_la, 5 - attempts, 86400)
            return True
            
        elif attempts == 5:
            time_elapsed = current_time - last_attempt
            cache.set(key_user_la, 3, 86400) # Attempts left set for next phase
            if time_elapsed < 60:
                self.wait_time = 60 - time_elapsed
                return False
        
        # Next 3 attempts - continuous
        elif attempts < 8:
            cache.set(key, attempts + 1, 86400)
            cache.set(key_user_la, 8 - attempts, 86400)
            cache.set(key_la, current_time, 86400)
            return True
            
        elif attempts <= 11:
            time_elapsed = current_time - last_attempt
            cache.set(key_user_la, 1, 86400)
            if time_elapsed < 300: 
                self.wait_time = 300 - time_elapsed
                return False
                
        elif attempts == 12:
            time_elapsed = current_time - last_attempt
            cache.set(key_user_la, 1, 86400)
            if time_elapsed < 600:
                self.wait_time = 600 - time_elapsed
                return False
                
        elif attempts == 13:
            time_elapsed = current_time - last_attempt
            cache.set(key_user_la, 1, 86400)
            if time_elapsed < 3600:
                self.wait_time = 3600 - time_elapsed
                return False
                
        elif attempts > 13:
            time_elapsed = current_time - last_attempt
            cache.set(key_user_la, 1, 86400)
            if time_elapsed < 86400:
                self.wait_time = 86400 - time_elapsed
                return False

        cache.set(key, attempts + 1, 86400)
        cache.set(key_la, current_time, 86400)
        return True

    def wait(self):
        """
        Returns the recommended next request time in seconds.
        """
        return self.wait_time

