from account.models import User
from watson import search

from ..serializers import UserNameSerializer
from ..utils import Generate_Username
from ._base import AllowAny, APIView, Response, status


class Suggest_Username_API(APIView):
    """
    This API, will work like this
    - The suggested username based on user's First and Last name.
    - Will use most common special characters.
    - Can also use birthday, if required.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        birth_date = request.data.get("birth_date")

        ng = Generate_Username(first_name, last_name, birth_date)
        generated_name = ng.generate_unique_name()

        return Response({
            "suggested_user_name": generated_name,
        }, status=status.HTTP_200_OK)



class Check_Username_Exists_API(APIView):
    """
    Checks if username exists and return them\n
    Returns:
    - List of usernames
    - Boolean of existence
    """
    permission_classes = [AllowAny]

    def post(self, request):

        user_name = request.data.get("username")
        query_set = search.filter(User, user_name)
        serializer = UserNameSerializer(query_set, many=True)
        check_set = User.objects.filter(username=user_name)
        
        available = False
        if not check_set.exists():
            available = True

        return Response({
            'available_to_use': available,
            'similar_existing_names': serializer.data,
        }, status=status.HTTP_200_OK)


