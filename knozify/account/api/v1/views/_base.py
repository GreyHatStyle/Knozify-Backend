"""
This file will have all imports I need in this view
"""
import logging

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger(__name__)

class BaseAPIView(APIView):
    """
    This DRF BaseAPIView will help me to not add logger in every file.
    """
    permission_classes = [AllowAny]
    logger = logger


def api_exception_handler(api_view_method):
    """Wraps the "try/except" block, So that I don't have to write it again and again

    Args:
        api_view_method (def method): API view method/function.
    """
    def wrapper(self, request, *args, **kwargs):
        try:
            return api_view_method(self, request, *args, **kwargs)
        
        except Exception as e:
            return Response({
                "status": "exception",
                "reason": str(e),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    return wrapper