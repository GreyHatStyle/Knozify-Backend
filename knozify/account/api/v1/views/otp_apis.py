import re

from pydantic import BaseModel, Field, field_validator

from ..utils import OTP_Handler
from ._base import AllowAny, BaseAPIView, Response, api_exception_handler, status


class PhoneNumber_Validation(BaseModel):
    phone_no: str = Field(..., description="Phone number with country code")
    
    @field_validator("phone_no")
    def validate_phone_number(cls, v):
        pattern = r'^\+([1-9]{1,3})-([0-9]{10})$'
        
        if not re.match(pattern, v):
            raise ValueError('Invalid Phone number format, please ensure country code is correct, eg: "+9190812334xx".')   
    
        return v

class Send_OTP_to_Number_API(BaseAPIView):
    """
    This API will send OTP to number, and then return back its expiration time left (in seconds).
    """
    permission_classes = [AllowAny]

    @api_exception_handler
    def post(self, request):
        phone_no = PhoneNumber_Validation(phone_no=request.data.get("phone_no")).phone_no

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
            "time_left_seconds": time_left, 
        })
        

class OTP_Validator_API(BaseAPIView):
    """
    This API will receive the User provided OTP, and verify it with Original OTP, then return response in boolean.
    """
    permission_classes = [AllowAny]

    @api_exception_handler
    def post(self, request):
        
        otp = request.data.get("otp")
        phone_no = PhoneNumber_Validation(phone_no=request.data.get("phone_no")).phone_no
        
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
        