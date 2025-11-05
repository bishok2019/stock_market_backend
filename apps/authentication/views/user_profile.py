from base.views import (
    CustomGenericCreateView,
    CustomGenericListView,
    CustomGenericRetrieveView,
    CustomGenericUpdateView,
)

from ..models import UserProfile
from ..serializers import UserProfileGetSerializer, UserProfileUpdateSerializer


class UserProfileGetAPIView(CustomGenericRetrieveView):
    serializer_class = UserProfileGetSerializer

    def get_object(self):
        return UserProfile.objects.filter(user=self.request.user).first()


class UserProfileUpdateAPIView(CustomGenericUpdateView):
    serializer_class = UserProfileGetSerializer
    queryset = UserProfile.objects.all()
