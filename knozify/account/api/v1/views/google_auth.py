from ..serializers import GoogleAuthSerializer
from ._base import AllowAny, BaseAPIView, Response, status


class GoogleAPIview(BaseAPIView):
    """
    Logins `user` if already exists, otherwise register them.
    """
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = GoogleAuthSerializer(data=request.data)
        
        if serializer.is_valid():
            data = serializer.save()
            return Response(data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)