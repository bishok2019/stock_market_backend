from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from ..serializers import LogoutSerializer


class LogoutView(GenericAPIView):
    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return Response(
                {"message": "Logged out successfully."}, status=status.HTTP_200_OK
            )
        return Response(
            {"message": "Logout failed.", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )
