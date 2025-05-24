from account.throttles import LoginRateThrottle
from rest_framework_simplejwt.views import TokenObtainPairView
from utils.throttle_exception import TimeThrottleMix


class LoginAPI(TimeThrottleMix, TokenObtainPairView):
    """
    API class to help user to login, and obtain JWT access and refresh tokens.
    """
    throttle_classes = [LoginRateThrottle]