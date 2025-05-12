from account.models import User
from account.throttles import LoginRateThrottle

from django.contrib.auth import get_user_model

from google.oauth2 import id_token
from google.auth.transport import requests

from .otp import OTP_Handler

from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

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


# TODO: This api sending every details... change it as soon as frontend dev is done with his work.
class GetUserDataAPIView(APIView):
    """
    Sends all the user information for now, will update it soon.
    """
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
        

class Send_OTP_to_Number_API(APIView):
    """
    This API will send OTP to number, and then return back its expiration time left (in seconds).
    """
    permission_classes = [AllowAny]

    def post(self, request):

        try:
            phone_no = request.data.get("phone_no")

            if phone_no is None:
                return Response({
                    "status":"error",
                    "reason": "No Phone number provided", 
                }, status=status.HTTP_400_BAD_REQUEST)

            otp_handle = OTP_Handler(phone_number=phone_no)
            
            otp = otp_handle.send_otp()
            if otp is None:
                return Response({
                    "status":"error",
                    "reason":"Couldn't send OTP, something wrong with API",
                })
            
            time_left = otp_handle.time_left()

            return Response({
                "status": "success",
                "otp": otp,
                "time_left_seconds": time_left, 
            })
        
        except Exception as e:
            return Response({
                "status": "exception",
                "reason": str(e),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class OTP_Validator_API(APIView):
    """
    This API will receive the User provided OTP, and verify it with Original OTP, then return response in boolean.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            otp = request.data.get("otp")
            phone_no = request.data.get("phone_no")

            if otp is None:
                return Response({
                    "status":"error",
                    "reason":"No OTP provided",
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if phone_no is None:
                return Response({
                    "status":"error",
                    "reason":"No Phone Number provided",
                }, status=status.HTTP_400_BAD_REQUEST)

            if OTP_Handler.verify_otp(otp=otp, phone_no=phone_no):
                return Response({
                    "status":"success",
                    "otp": "verified",
                }, status=status.HTTP_202_ACCEPTED)
            
            
            return Response({
                "status":"error",
                "reason":"OTP is wrong or Expired",
            }, status=status.HTTP_401_UNAUTHORIZED)
        

        except Exception as e:
            return Response({
                "status": "exception",
                "reason": str(e),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

