import re

from account.throttles import LoginRateThrottle
from django.contrib.auth import authenticate
from pydantic import BaseModel, ConfigDict, Field, field_validator
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from utils.throttle_exception import TimeThrottleMix

from ..utils import Login_Support
from ._base import BaseAPIView, api_exception_handler


class Login_Validator(BaseModel):
    model_config = ConfigDict(extra='forbid')
    
    username: str = Field(..., description="Username of person")
    password: str
    
    @field_validator("username")
    def validate_username(cls, value):
        valid_username_characters = r'^[a-zA-z0-9_.-]+$'
        
        if not re.match(valid_username_characters, value):
            raise ValueError("Only excepted characters are hyphen (-), underscore (_) and dot (.)")
        
        return value
        
class LoginAPI(TimeThrottleMix, BaseAPIView):
    """
    API class to help user to login, and obtain JWT access and refresh tokens.
    """
    throttle_classes = [LoginRateThrottle]
    
    @api_exception_handler
    def post(self, request):
        validated_data = Login_Validator(**request.data)
        print("username: ", str(validated_data.username), "password: ", validated_data.password)
        user = authenticate(
            username=validated_data.username,
            password=validated_data.password,
        )
        
        attempts_left = Login_Support().get_attempts_left(request)
        
        if user:
            refresh = RefreshToken.for_user(user=user)
            
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_200_OK)
            
        return Response({
           "detail_for_user":f"Username or Password is Incorrect, {attempts_left} {"attempts" if attempts_left>1 else "attempt"} left",
        }, status=status.HTTP_401_UNAUTHORIZED)