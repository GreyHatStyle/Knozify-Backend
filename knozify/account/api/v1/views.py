from account.models import User

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from account.throttles import LoginRateThrottle

from django.contrib.auth import get_user_model
from google.oauth2 import id_token
from google.auth.transport import requests


from .serializers import (
    GoogleAuthSerializer,
    GetUserInfoSerializer,
)
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


class GetUserDataAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            query_set = User.objects.get(id=request.user.id)
            serializer = GetUserInfoSerializer(query_set)

            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'status': 'exception',
                'data': str(e),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
