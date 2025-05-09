from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from account.throttles import LoginRateThrottle

from django.contrib.auth import get_user_model
from google.oauth2 import id_token
from google.auth.transport import requests

from .serializers import GoogleAuthSerializer
class FirstAPI(APIView):
    """
    Testing api, to check if django is working or not.
    """
    def get(self, request):
        return Response({"message": "Everything working perfectly!!!"},
                        status=status.HTTP_200_OK)


class TokenObtainPairViewForLogin(TokenObtainPairView):
    """
    API class to help user to login, and obtain JWT access and refresh tokens.
    """
    throttle_classes = [LoginRateThrottle]


class GoogleAPIview(APIView):
    """
    Logins `user` if already exists, otherwise register them.
    """
    def post(self, request):
        serializer = GoogleAuthSerializer(data=request.data)
        
        if serializer.is_valid():
            data = serializer.save()
            return Response(data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
