import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)

def global_exception_handler(exception, context):
    """
    This function provides a "general exception handling" for all api's I am going to use.\n
    It will handle the unknown exceptions for all the API Classes, without me adding try/except in each API
    """
    response = exception_handler(exc=exception, context=context)

    if response is not None:
        return response
    
    logger.exception(f"Exception Arrived in: {context.get("view")}")

    return Response({
        "status":"exception",
        "reason": str(exception),
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)