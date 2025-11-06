from django.shortcuts import render

from base.views import (
    CustomGenericCreateView,
    CustomGenericListView,
    CustomGenericRetrieveView,
    CustomGenericUpdateView,
)

from .models import Notification

# Create your views here.
from .serializers import (
    SystemNotificationRetrieveSerializer,
    SystemNotificationSerializer,
    UserNotificationListSerializer,
    UserNotificationRetrieveSerializer,
)


class SystemNotificationListAPIView(CustomGenericListView):
    queryset = Notification.objects.all()
    serializer_class = SystemNotificationSerializer
    success_response_message = "Notification Fetched Successfully"


class SystemNotificationRetrieveAPIView(CustomGenericListView):
    queryset = Notification.objects.all()
    serializer_class = SystemNotificationRetrieveSerializer
    success_response_message = "Notification Retrieved Successfully"


class UserNotificationListAPIView(CustomGenericListView):
    serializer_class = UserNotificationListSerializer
    success_response_message = "Notification Fetched Successfully"
    # queryset = Notification.objects.all()

    def get_queryset(self):
        user = self.request.user
        return Notification.objects.filter(user=user)


class UserNotificationRetrieveAPIView(CustomGenericRetrieveView):
    serializer_class = UserNotificationRetrieveSerializer
    queryset = Notification.objects.all()
    success_response_message = "Notification Retrieved Successfully"

    def get_queryset(self):
        user = self.request.user
        return Notification.objects.filter(user=user)
