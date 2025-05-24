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
