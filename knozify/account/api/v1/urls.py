from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

urlpatterns = [
    path('first/', views.FirstAPI.as_view(), name='first'),

    # Authentications
    path('token/', views.LoginAPI.as_view(), name='login-api'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('auth/google/', views.GoogleAPIview.as_view(), name='google-auth'),
    path('get-user/', views.GetUserDataAPIView.as_view(), name='get-user'),

    # OTP Managers
    path('otp/receiver/', views.Send_OTP_to_Number_API.as_view(), name='send-otp'),
    path('otp/validate/', views.OTP_Validator_API.as_view(), name='validate-otp'),

    # # User Managers
    path('username/suggest/', views.Suggest_Username_API.as_view(), name='suggest-username'),
    path('username/check/', views.Check_Username_Exists_API.as_view(), name='suggest-username'),
    
    # Register
    path('register/', views.Registration_API.as_view(), name='register'),
]
