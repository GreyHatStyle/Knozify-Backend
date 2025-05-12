from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

urlpatterns = [
    path('first/', views.FirstAPI.as_view(), name='first'),

    # Authentications
    path('token/', views.TokenObtainPairViewForLogin.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/google/', views.GoogleAPIview.as_view(), name='google-auth'),
    path('get-user/', views.GetUserDataAPIView.as_view(), name='get-user'),

    # OTP Managers
    path('otp/receiver/', views.Send_OTP_to_Number_API.as_view(), name='send-otp'),
    path('otp/validate/', views.OTP_Validator_API.as_view(), name='validate-otp'),
]
