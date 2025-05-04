from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class FirstAPI(APIView):
    def get(self, request):
        return Response({"message": "Everything working perfectly!!!"},
                        status=status.HTTP_200_OK)
