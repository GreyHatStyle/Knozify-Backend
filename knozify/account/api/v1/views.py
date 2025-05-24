from account.models import User
from account.throttles import LoginRateThrottle

from django.contrib.auth import get_user_model

from google.oauth2 import id_token
from google.auth.transport import requests

import logging

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
    UserNameSerializer,
    UserRegistrationSerializer
)

from .user_name_gen import Generate_Username
from watson import search

logger = logging.getLogger(__name__)

class FirstAPI(APIView):
    """
    Testing api, to check if django is working or not.
    """
    def get(self, request):
        logger.info("The First api service is working fine!!!")
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


class Suggest_Username_API(APIView):
    """
    This API, will work like this
    - The suggested username based on user's First and Last name.
    - Will use most common special characters.
    - Can also use birthday, if required.
    """
    def post(self, request):
        try:
            first_name = request.data.get("first_name")
            last_name = request.data.get("last_name")
            birth_date = request.data.get("birth_date")

            ng = Generate_Username(first_name, last_name, birth_date)
            generated_name = ng.generate_unique_name()

            return Response({
                "suggested_user_name": generated_name,
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "status": "exception",
                "reason": str(e),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class Check_Username_Exists_API(APIView):
    """
    Checks if username exists and return them\n
    Returns:
    - List of usernames
    - Boolean of existence
    """
    def post(self, request):
        try:
            user_name = request.data.get("username")
            query_set = search.filter(User, user_name)
            serializer = UserNameSerializer(query_set, many=True)
            check_set = User.objects.filter(username=user_name)
            
            available = False
            if not check_set.exists():
                available = True

            return Response({
                'available_to_use': available,
                'similar_existing_names': serializer.data,
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "status": "exception",
                "reason": str(e),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Registration_API(APIView):
    """
    Registers the user in Database
    """
    def post(self, request):
        try:
            serializer = UserRegistrationSerializer(data=request.data)

            if serializer.is_valid():
                user = serializer.save()
                refresh = RefreshToken.for_user(user)

                logger.info(f"User {user.username} is successfully created!!!")

                return Response({
                    "status": "success",
                    "reason": f"User, {user.username} created successfully!!",
                    "tokens": {
                        "refresh":str(refresh),
                        "access":str(refresh.access_token),
                    }
                }, status=status.HTTP_201_CREATED) 

            return Response({
                "status": "error",
                "reason": serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)

    
        except Exception as e:
            return Response({
                "status": "exception",
                "reason": str(e),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)