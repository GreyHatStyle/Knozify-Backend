from rest_framework_simplejwt.tokens import RefreshToken

from ..serializers import UserRegistrationSerializer
from ._base import AllowAny, BaseAPIView, Response, api_exception_handler, status


class Registration_API(BaseAPIView):
    """
    Registers the user in Database
    """
    permission_classes = [AllowAny]

    @api_exception_handler
    def post(self, request):

        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)

            self.logger.info(f"User {user.username} is successfully created!!!")

            return Response({
                "status": "success",
                "reason": f"User, {user.username} created successfully!!",
                "tokens": {
                    "refresh":str(refresh),
                    "access":str(refresh.access_token),
                },
                "detail_for_user": "successful!!",
            }, status=status.HTTP_201_CREATED) 

        error_for_user = next(iter(serializer.errors.values()))[0] # just getting first error from all errors
        return Response({
            "status": "error",
            "reason": serializer.errors,
            "detail_for_user": error_for_user,
        }, status=status.HTTP_400_BAD_REQUEST)