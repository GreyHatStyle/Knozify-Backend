from ._base import AllowAny, BaseAPIView, Response, status


class FirstAPI(BaseAPIView):
    """
    Testing api, to check if django is working or not.
    """
    permission_classes = [AllowAny]
    def get(self, request):
        # error = 3/0
        # print(error)
        self.logger.info("The First api service is working fine!!!")
        return Response({"message": "Everything working perfectly!!!"},
                        status=status.HTTP_200_OK)