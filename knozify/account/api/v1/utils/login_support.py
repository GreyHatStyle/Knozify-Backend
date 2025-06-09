import logging

from django.core.cache import cache


class Login_Support:
    
    def __init__(self):
        self.ip_address = ""
        self._logger = logging.getLogger(__name__)
        
    # TODO: Build a way to deal with request other than ipv4 and ipv6 address
    def get_client_ipv6(self, request) -> str:
        """
        Extract the IPv6 address from the request.\n
        Check with: `uv run manage.py runserver [::]:8000`\n
        If not IPv6 address found, return IPv4 address, else unknown (for now)
        """
        
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        
        if x_forwarded_for:
            self._logger.debug(f"X_forwarded for: {x_forwarded_for}")
            ip = x_forwarded_for.split(',')[0].strip()
            self._logger.debug(f"X_forwarded IP: {ip}")

            if ':' in ip:
                return ip
        
        # Check for specific IPv6 headers, if any
        ipv6 = request.META.get('HTTP_X_REAL_IPV6')
        self._logger.debug(f"HTTP specific IPv6 header: {ipv6}")
        if ipv6:
            return ipv6
        
        # Finally check for remote client
        remote_addr = request.META.get('REMOTE_ADDR')
        self._logger.debug(f"Remote Address: {remote_addr}")
        if remote_addr and ':' in remote_addr:
            return remote_addr
        
        
        return remote_addr or "Unknown"
    
    
    def get_attempts_left(self, request) -> str:
        """Gets attempts left from redis cache

        Returns:
            str: attempts left before throttle
        """
        
        self.ip_address = self.get_client_ipv6(request)
        attempts_left_key = f"login_attempt_{self.ip_address}_attempt_left"
        
        attempts_left = cache.get(attempts_left_key)
        return attempts_left
        