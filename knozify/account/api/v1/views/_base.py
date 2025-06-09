"""
This file will have all imports I need in this view
"""
import logging

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger(__name__)

class BaseAPIView(APIView):
    """
    This DRF BaseAPIView will help me to not add logger in every file.
    """
    permission_classes = [AllowAny]
    renderer_classes = [JSONRenderer]
    logger = logger
    
    
    def http_method_not_allowed(self, request, *args, **kwargs):
        return Response({
            "detail": "It doesn't support this request sir, kindly check documentation.",
        }, 
        status=status.HTTP_405_METHOD_NOT_ALLOWED,
        content_type="application/json")


def api_exception_handler(api_view_method):
    """Wraps the "try/except" block, So that I don't have to write it again and again

    Args:
        api_view_method (def method): API view method/function.
    """
    def wrapper(self, request, *args, **kwargs):
        try:
            return api_view_method(self, request, *args, **kwargs)
        
        except ValueError as ve:
            ve = str(ve)
            detail_for_user = ""
            
            if ("pydantic" in ve) and ("Value error, " in ve):
                start_index = ve.find("Value error, ") + len("Value error, ")
                end_index = ve.find(" [type=value_error")
                
                detail_for_user = ve[start_index:end_index]
            
            else:
                detail_for_user = ""
                
            return Response({
                "status": "error",
                "reason": ve,
                "detail_for_user": detail_for_user,
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({
                "status": "exception",
                "reason": str(e),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    return wrapper