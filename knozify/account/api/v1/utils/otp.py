import json
import logging
import os
import subprocess
from random import randint
from urllib.parse import unquote

import requests
from django.conf import settings
from django.core.cache import caches
from rest_framework import status


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
        self.__phone_no = phone_number
        self.__time_left_seconds = 120

        # will give user 10 seconds more after expiration time to complete otp request
        # Considering API request delay
        self.__buffer_time = 10

        self.__cache_obj = caches["otp"]
        self.__otp_length = 6

        self.__logger = logging.getLogger(__name__)

    def __generate_otp(self) -> str:
        """
        Generate a random otp of `self.__otp_length` size.
        """
        
        start_limit = 10 ** (self.__otp_length - 1) # in case of (6), 100000
        end_limit = (10 ** self.__otp_length) - 1   # in case of (6), 999999

        random_number = randint(start_limit, end_limit)
        otp = str(random_number)

        return otp
    
    def __store_otp_in_redis(self, otp):
        """
        Will new store otp in redis cache, for designated expiration time.\n
        If person ask for new otp, the it will over-write old otp.
        """

        self.__cache_obj.set(
            key=self.__phone_no,
            value=otp,
            timeout=(self.__time_left_seconds + self.__buffer_time),
        )

    def send_otp(self) -> int:
        """
        Send OTP to User's phone number Via TextBee Open source API
        """
        otp = self.__generate_otp()

        # BUG: For some reason this api isn't working when called with backend, but with frontend it is
        # api_url = os.environ.get("SMS_SENDER_API")
        # api_key = os.environ.get("TEXTBEE_API_KEY")

        # api_url = f"https://{api_url}"
        # print("API URL: ", api_url)

        
        # # headers = {
        # #     "Content-Type": "application/json",
        # #     "x-api-key": api_key,
        # # }

        # payload = {
        #     "recipients": [self.__phone_no],
        #     "message": f"Thanks for using Knozify!!\nYour OTP is: {otp}."
        # }

        # node_js_file = settings.BASE_DIR / "account" / "sms-sender.js"
        # print("NODE JS FILE: ", node_js_file)
        # # # Convert to properly escaped JSON string
        # # json_payload = json.dumps(payload)

        # # # Build the command with the properly formatted JSON
        # # command = f"""curl -X POST "{api_url}" -H "x-api-key: {api_key}" -H "Content-Type: application/json" -d '{json_payload}'"""
        # # node_command = f""" node {node_js_file} "{api_url}" "{api_key}" "{self.__phone_no}" "Thanks for using Knozify!!\nYour OTP is: {otp}." """

        # command_parts = [
        #     "node",
        #     str(node_js_file),  # Ensure the Path object is converted to a string
        #     api_url,
        #     api_key,
        #     self.__phone_no,
        #     f"Thanks for using Knozify!!\nYour OTP is: {otp}."
        # ]

        # try:
        #     result = subprocess.run(
        #         command_parts,
        #         capture_output=True,  # Equivalent to stdout=subprocess.PIPE, stderr=subprocess.PIPE
        #         text=True,            # Decode stdout/stderr as text
        #         check=False           # Manually check returncode, so don't raise error on non-zero exit
        #     )
        # except FileNotFoundError:
        #     self.__logger.error("Error: 'node' executable not found. Make sure Node.js is installed and in your PATH.")
        #     return False
        # except Exception as e: # Catch other potential subprocess errors
        #     self.__logger.error(f"Subprocess execution failed: {e}, STDOUT: {getattr(e, 'stdout', '')}, STDERR: {getattr(e, 'stderr', '')}")
        #     return False


        self.__store_otp_in_redis(otp=otp)

        # Some loggings for debugging
        # TODO I know its trash way to log, I will fix it soon
        # if result.returncode == status.HTTP_201_CREATED:
        #     self.__logger.info(f"API HAS BEEN SENT: BODY: {result.stdout}")
        #     return True
        
        # else:
        #     self.__logger.error(f"Some error occurred, BODY: {result.stderr}")
        #     return False
        
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
        server_generated_otp = c.get(phone_no)

        if user_provided_otp != server_generated_otp:
            print("Server generated OTP: ", server_generated_otp)
            return False
        
        return True




