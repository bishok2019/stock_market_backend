from django.shortcuts import render

from base.views import (
    CustomGenericCreateView,
    CustomGenericListView,
    CustomGenericRetrieveView,
    CustomGenericUpdateView,
)

from .models import Notification

# Create your views here.
from .serializers import NotificationSerializer


class NotificationListAPIView(CustomGenericListView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer


class NotificationRetrieveAPIView(CustomGenericListView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
