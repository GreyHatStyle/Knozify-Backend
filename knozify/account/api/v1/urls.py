from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

urlpatterns = [
    path('first/', views.FirstAPI.as_view(), name='first'),
    path('token/', views.TokenObtainPairViewForLogin.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/google/', views.GoogleAPIview.as_view(), name='google-auth'),
    path('get-user/', views.GetUserDataAPIView.as_view(), name='get-user'),
]
