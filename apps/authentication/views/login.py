from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from ..serializers import LoginSerializer


class LoginView(GenericAPIView):
    permission_classes = []
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "status": "success",
                    "message": "Login successful",
                    "data": {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    },
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"status": "error", "message": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class RefreshTokenView(TokenRefreshView):
    permission_classes = []
