import json
import logging
import os
import subprocess
from random import randint

from django.core.cache import caches


class OTP_Handler:
    """
    This class will manage OTP:
    - Generation
    - Regeneration
    - Rate limits
    - Expiration time
    - Validation
    """

    def __init__(self, phone_number: str):
        self.__phone_no = phone_number.replace("-", "") # making it compatible for (textbee api)
        self.__time_left_seconds = 120

        # will give user 10 seconds more after expiration time to complete otp request
        # Considering API request delay
        self._buffer_time = 10

        self._cache_obj = caches["otp"]
        self._otp_length = 6

        self._logger = logging.getLogger(__name__)

    def _generate_otp(self) -> str:
        """
        Generate a random otp of `self.__otp_length` size.
        """
        
        start_limit = 10 ** (self._otp_length - 1) # in case of (6), 100000
        end_limit = (10 ** self._otp_length) - 1   # in case of (6), 999999

        random_number = randint(start_limit, end_limit)
        otp = str(random_number)

        return otp
    
    def _store_otp_in_redis(self, otp):
        """
        Will new store otp in redis cache, for designated expiration time.\n
        If person ask for new otp, the it will over-write old otp.
        """

        self._cache_obj.set(
            key=self.__phone_no,
            value=otp,
            timeout=(self.__time_left_seconds + self._buffer_time),
        )

    def send_otp(self) -> int:
        """
        Send OTP to User's phone number Via TextBee Open source API
        """
        otp = self._generate_otp()
    
        api_url = os.environ.get("SMS_SENDER_API")
        api_key = os.environ.get("TEXTBEE_API_KEY")
    
        payload = json.dumps({"recipients": [self.__phone_no], "message": f"Your Knozify OTP is {otp}."})

        # using subprocess, because for some reason 'requests.post' method is not working with textbee api (for django only)
        cmd = [
            "curl",
            "-X", "POST", api_url,
            "-H", f"x-api-key: {api_key}",
            "-H", "Content-Type: application/json",
            "-d", payload
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        self._logger.debug(f"stdout: {result.stdout}")
        self._logger.debug(f"stderr: {result.stderr}")
        
        self._store_otp_in_redis(otp=otp)
        return otp

    def time_left(self):
        """
        Returns Time left (in seconds) for OTP to expire.
        """
        return self.__time_left_seconds

        
    @staticmethod
    def verify_otp(phone_no: str, otp: str) -> bool:
        """
        Returns boolean condition for OTP validity.
        """
        c = caches['otp']

        user_provided_otp = otp
        server_generated_otp = c.get(phone_no.replace("-", ""))

        if user_provided_otp != server_generated_otp:
            print("Server generated OTP: ", server_generated_otp)
            return False
        
        return True




