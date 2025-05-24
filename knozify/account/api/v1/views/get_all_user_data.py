from account.models import User

from ..serializers import GetUserInfoSerializer
from ._base import BaseAPIView, IsAuthenticated, Response, status


# TODO: This api sending every details... change it as soon as frontend dev is done with his work.
class GetUserDataAPIView(BaseAPIView):
    """
    Sends all the user information for now, will update it soon.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query_set = User.objects.get(id=request.user.id)
        serializer = GetUserInfoSerializer(query_set)

        return Response(serializer.data, status=status.HTTP_200_OK)
            
        